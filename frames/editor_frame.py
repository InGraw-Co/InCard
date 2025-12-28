# ================== BIBLIOTEKI ==================
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import json, os
from paths import *
from config import *

# ================== SESJA 3 ==================
class EditorFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.icon_selected = False
        self.editing_id = None
        self.current_icon_tk = None
        self.orig_icon_img = None
        self.icon_zoom = 1.0
        self.icon_offset = [0, 0]
        self.drag_start = None
        L = self.app.L

        self.title = ttk.Label(self, font=("Segoe UI", 18))
        self.title.pack(pady=20)

        # Pola edycyjne
        self.name = self.field(L["field.name"])
        self.rarity = self.combo(L["field.rarity"], self.app.rarity)
        self.type_ = self.combo(L["field.type"], self.app.types)
        self.prop = self.combo(L["field.property"], self.app.properties)
        self.accuracy = self.field(L["field.accuracy"])

        # Podgląd ikony na Canvasie
        self.icon_canvas = tk.Canvas(self, width=ICON_SIZE, height=ICON_SIZE, bg="gray")
        self.icon_canvas.pack(pady=10)
        self.icon_canvas.bind("<B1-Motion>", self.drag_icon)
        self.icon_canvas.bind("<ButtonPress-1>", self.start_drag_icon)
        self.icon_canvas.bind("<MouseWheel>", self.zoom_icon)  # Windows
        self.icon_canvas.bind("<Button-4>", lambda e: self.zoom_icon(e, 1.1))  # Linux scroll up
        self.icon_canvas.bind("<Button-5>", lambda e: self.zoom_icon(e, 0.9))  # Linux scroll down

        # Podgląd ikony na Canvasie
        ttk.Label(self, text=L["icon.instruction"], wraplength=ICON_SIZE, foreground="blue").pack(pady=5)

        ttk.Button(self, text=L["button.pick_icon"], command=self.pick_icon).pack(pady=10)
        ttk.Button(self, text=L["button.save_next"], command=self.save).pack(pady=20)

        self.error = ttk.Label(self, text="", foreground="red")
        self.error.pack(pady=5)

    # ================= ADVANCED =================
    def show_advanced_window(self):
        L = self.app.L
        win = tk.Toplevel(self)
        win.title(L["advanced.title"])
        win.geometry("800x800")
        win.transient(self.app)
        win.grab_set()
        win.focus()

        # Środkowanie
        w, h = 600, 400
        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")

        # Canvas + scrollbar
        canvas = tk.Canvas(win)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Wczytaj karty
        cards_exist = False
        if os.path.exists(CARDS_TMP):
            with open(CARDS_TMP, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        card = json.loads(line)
                        cards_exist = True

                        frame = ttk.Frame(scroll_frame, padding=5)
                        frame.pack(fill="x", pady=2)

                        # ID
                        ttk.Label(frame, text=f"{card['id']:03}").pack(side="left", padx=5)

                        # Ikona
                        img_path = os.path.join(ICON_DIR, f"{card['id']}.png")
                        if os.path.exists(img_path):
                            img = Image.open(img_path).resize((40, 40))
                            img_tk = ImageTk.PhotoImage(img)
                            lbl = ttk.Label(frame, image=img_tk)
                            lbl.image = img_tk
                            lbl.pack(side="left", padx=5)

                        # Nazwa
                        ttk.Label(frame, text=card['n']).pack(side="left", padx=5)

                        # Kliknięcie ładuje kartę
                        def make_edit(c=card):
                            win.grab_release()
                            win.destroy()
                            self.load_card(c["id"])

                        frame.bind("<Button-1>", lambda e, c=card: make_edit(c))
                        for child in frame.winfo_children():
                            child.bind("<Button-1>", lambda e, c=card: make_edit(c))
                    except:
                        pass

        if not cards_exist:
            ttk.Label(scroll_frame, text=L["advanced.no_cards"], foreground="orange", font=("Segoe UI", 14)).pack(pady=20)

        def on_close():
            win.grab_release()
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", on_close)

    # ================= LOAD CARD =================
    def load_card(self, card_id):
        if not os.path.exists(CARDS_TMP):
            return
        card_data = None
        with open(CARDS_TMP, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            try:
                c = json.loads(line)
                if c["id"] == card_id:
                    card_data = c
                    break
            except:
                pass
        if not card_data:
            return

        # Wczytanie pól
        self.name.delete(0, "end")
        self.name.insert(0, card_data["n"])
        self.rarity.set(card_data["r"])
        self.type_.set(card_data["t"])
        self.prop.set(card_data["p"])
        self.accuracy.delete(0, "end")
        self.accuracy.insert(0, str(card_data["a"]))

        # Wczytanie oryginalnej ikony
        img_path = os.path.join(ICON_DIR, f"{card_id}.png")
        if os.path.exists(img_path):
            self.orig_icon_img = Image.open(img_path).convert("RGBA")
            self.icon_zoom = 1.0
            self.icon_offset = [ICON_SIZE//2, ICON_SIZE//2]
            self.display_icon_canvas()
            self.icon_selected = True

        self.editing_id = card_id
        self.update_title(card_id)

    # ================= ICON CANVAS =================
    def display_icon_canvas(self):
        self.icon_canvas.delete("IMG")
        if not self.icon_selected or not self.orig_icon_img:
            return
        w, h = self.orig_icon_img.size
        scale = ICON_SIZE / max(w, h)
        preview_w, preview_h = int(w*scale*self.icon_zoom), int(h*scale*self.icon_zoom)
        img = self.orig_icon_img.resize((preview_w, preview_h), Image.Resampling.LANCZOS)
        self.current_icon_tk = ImageTk.PhotoImage(img)
        self.icon_canvas.delete("IMG")
        x = self.icon_offset[0]
        y = self.icon_offset[1]
        self.icon_canvas.create_image(x, y, image=self.current_icon_tk, anchor="center", tags="IMG")

    def start_drag_icon(self, event):
        self.drag_start = (event.x, event.y)

    def drag_icon(self, event):
        if self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            self.icon_offset[0] += dx
            self.icon_offset[1] += dy
            self.drag_start = (event.x, event.y)
            self.display_icon_canvas()

    def zoom_icon(self, event, factor=None):
        if factor is None:
            factor = 1.0 + (event.delta / 1200)
        self.icon_zoom *= factor
        self.display_icon_canvas()

    # =================== MAIN =================
    def on_show(self):
        self.update_title()
        if self.editing_id:
            self.load_card(self.editing_id)
        else:
            # reset dla nowych kart
            self.icon_canvas.delete("IMG")
            self.name.delete(0, "end")
            self.accuracy.delete(0, "end")
            self.rarity.current(0)
            self.type_.current(0)
            self.prop.current(0)
            self.icon_selected = False

    def field(self, label):
        ttk.Label(self, text=label).pack(anchor="w", padx=250)
        e = ttk.Entry(self, width=40)
        e.pack()
        return e

    def combo(self, label, values):
        ttk.Label(self, text=label).pack(anchor="w", padx=250)
        c = ttk.Combobox(self, values=values, state="readonly", width=37)
        c.pack()
        c.current(0)
        return c

    def update_title(self, show_id=None):
        L = self.app.L
        if show_id is None:
            show_id = self.app.current_id
        self.title.config(text=L["editor.title"].format(
            current=show_id,
            total=self.app.cards_total
        ))

    def pick_icon(self):
        L = self.app.L
        path = filedialog.askopenfilename(
            filetypes=[
                (L["filetypes.raster"], "*.png *.jpg *.jpeg *.bmp *.webp *.gif *.tiff *.tif *.ico *.tga"),
                ("PNG", "*.png"),
                ("JPG/JPEG", "*.jpg *.jpeg"),
                ("BMP", "*.bmp"),
                ("WebP", "*.webp"),
                (L["filetypes.all"], "*.*")
            ]
        )

        if path:
            dst_id = self.editing_id if self.editing_id else self.app.current_id
            dst = os.path.join(ICON_DIR, f"{dst_id}.png")
            img = Image.open(path).convert("RGBA")
            img.save(dst)
            self.orig_icon_img = img
            self.icon_zoom = 1.0
            self.icon_offset = [ICON_SIZE//2, ICON_SIZE//2]
            self.icon_selected = True
            self.display_icon_canvas()
        self.clear_error()

    def show_error(self, msg):
        self.error.config(text=msg)

    def clear_error(self):
        self.error.config(text="")


    # ================= SAVE =================
    def save(self):
        self.clear_error()
        L = self.app.L
        if not self.icon_selected:
            self.show_error(L["error.icon_required"])
            return
        if not self.name.get().strip():
            self.show_error(L["error.name_required"])
            return

        # Walidacja trafności
        try:
            accuracy = float(self.accuracy.get())
        except:
            self.show_error(L["error.accuracy_number"])
            return

        # Walidacja nazwy max 20 znaków
        name_str = self.name.get().strip()
        if len(name_str) > 25:
            self.show_error(L["error.name_length"])
            return

        # Trafność: max 3 cyfry przed i po przecinku
        acc_str = f"{accuracy:.3f}"
        parts = acc_str.split(".")
        if len(parts[0]) > 3:
            self.show_error(L["error.accuracy_int"])
            return
        accuracy = float(acc_str)

        record = {
            "id": self.editing_id if self.editing_id else self.app.current_id,
            "n": name_str,
            "r": self.rarity.get(),
            "t": self.type_.get(),
            "p": self.prop.get(),
            "a": accuracy
        }

        # nadpisanie lub dodanie nowej karty
        cards = []
        if os.path.exists(CARDS_TMP):
            with open(CARDS_TMP, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        c = json.loads(line)
                        cards.append(c)
                    except:
                        pass

        found = False
        for i, c in enumerate(cards):
            if c["id"] == record["id"]:
                cards[i] = record
                found = True
                break
        if not found:
            cards.append(record)

        with open(CARDS_TMP, "w", encoding="utf-8") as f:
            for c in cards:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")

        # zapis ikony z przycięciem wg offsetu i zoomu (dokładnie jak w canvasie)
        if self.icon_selected and self.orig_icon_img:
            w, h = self.orig_icon_img.size
            scale = ICON_SIZE / max(w, h)
            preview_w, preview_h = int(w * scale * self.icon_zoom), int(h * scale * self.icon_zoom)
            img = self.orig_icon_img.resize((preview_w, preview_h), Image.Resampling.LANCZOS)

            final_img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0,0,0,0))
            x = self.icon_offset[0] - preview_w // 2
            y = self.icon_offset[1] - preview_h // 2

            final_img.paste(img, (x, y), img)

            dst_id = self.editing_id if self.editing_id else self.app.current_id
            final_img.save(os.path.join(ICON_DIR, f"{dst_id}.png"))

        # reset po zapisaniu nowej karty (jeśli nie edytujemy)
        if not self.editing_id:
            self.app.current_id += 1
            self.name.delete(0, "end")
            self.accuracy.delete(0, "end")
            self.rarity.current(0)
            self.type_.current(0)
            self.prop.current(0)
            self.icon_canvas.delete("IMG")
            self.icon_selected = False

        self.editing_id = None
        if self.app.current_id > self.app.cards_total:
            self.app.show("FinishFrame")
        else:
            self.update_title()
