# ================== BIBLIOTEKI ==================
import tkinter as tk
from tkinter import ttk
from paths import *
from config import *

#================== SESJA 1.5 ==================
class ConfigFrame(ttk.Frame):
    BUTTON_SIZE = 200

    def __init__(self, parent, app):
        super().__init__(parent)


        # ================== ZMIENNE ==================
        self.app = app
        settings = load_settings()
        self.settings = app.settings
        current_theme = settings.get("theme", "light")
        self.current_theme = current_theme
        L = self.app.L


        # ================== TŁO ==================
        self.configure(padding=20)
        self.style = ttk.Style()
        self.style.configure(
            "Config.TFrame",
            background=self.app.bg_light
        )
        self.configure(style="Config.TFrame")

        # ================== TYTUŁ ==================
        self.title_lbl = ttk.Label(
            self,
            text=L["config.title"],
            font=("Segoe UI", 24)
        )
        self.title_lbl.pack(pady=(40, 60))
        self.style.configure(
            "ConfigTitle.TLabel",
            background=self.app.bg_light,
            foreground=self.app.fg_btn_light
        )
        self.title_lbl.configure(style="ConfigTitle.TLabel")
        self.animating = False

        # ================== RAMKA PRZYCISKÓW ==================
        self.style.configure(
            "ConfigButtons.TFrame",
            background=self.app.bg_light
        )
        self.button_frame = ttk.Frame(
            self,
            style="ConfigButtons.TFrame"
        )
        self.button_frame.pack(side="bottom", pady=20)

        # ================== PRZYCISK: RESETUJ WSZYSTKIE DANE ==================
        self.reset_btn = RoundedButton(
            self.button_frame,
            text=L["config.reset_all_data"],
            command=reset_all_data,
            width=440,
            height=60
        )
        self.reset_btn.pack()

        # ================== DARK MODE BUTTON ==================
        self.theme_btn = tk.Label(
            self,
            text="🌙",
            font=("Segoe UI", 14),
            bg=self.app.bg_light,
            fg=self.app.fg_btn_light,
            cursor="hand2"
        )
        self.theme_btn.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")
        self.theme_btn.bind("<Button-1>", lambda e: self.toggle_theme())
        
        # ============ USTAWIENIE MOTYWU ============
        if current_theme == "dark":
            self.theme_btn.config(text="☀")
            self.animate_theme(
                self.app.bg_btn_light, self.app.bg_btn_dark,
                self.app.fg_btn_light, self.app.fg_btn_dark,
                self.app.bg_light, self.app.bg_dark,
                step=30 
            )
        else:
            self.theme_btn.config(text="🌙")
            self.animate_theme(
                self.app.bg_btn_dark, self.app.bg_btn_light,
                self.app.fg_btn_dark, self.app.fg_btn_light,
                self.app.bg_dark, self.app.bg_light,
                step=30
            )
            
    # ================== DARK MODE ==================
    def toggle_theme(self):
        if self.animating:
            return  
        
        self.animating = True

        if self.current_theme == "light":
            print("switch to dark")
            self.app.theme = "dark"
            self.settings["theme"] = "dark"
            save_settings(self.settings)
            current_theme = self.settings.get("theme", "light")
            print(current_theme)
            self.current_theme = "dark"  
            self.theme_btn.config(text="☀")
            self.animate_theme(
                self.app.bg_btn_light, self.app.bg_btn_dark,
                self.app.fg_btn_light, self.app.fg_btn_dark,
                self.app.bg_light, self.app.bg_dark
            )
        else:
            print("switch to light")
            self.app.theme = "light"
            self.settings["theme"] = "light"
            save_settings(self.settings)
            current_theme = self.settings.get("theme", "light")
            print(current_theme)
            self.current_theme = "light"  
            self.theme_btn.config(text="🌙")
            self.animate_theme(
                self.app.bg_btn_dark, self.app.bg_btn_light,
                self.app.fg_btn_dark, self.app.fg_btn_light,
                self.app.bg_dark, self.app.bg_light
            )

    # ================== ANIMACJA MOTYWU ==================
    def animate_theme(self, bg_from, bg_to, fg_from, fg_to, bg_theme_f, bg_theme_t, step=0):
        steps = 30
        t = step / steps

        bgt = lerp_color(bg_theme_f, bg_theme_t, t)
        bg = lerp_color(bg_from, bg_to, t)
        fg = lerp_color(fg_from, fg_to, t)

        self.style.configure("Config.TFrame", background=bgt)
        self.style.configure("ConfigTitle.TLabel", background=bgt, foreground=fg)
        self.style.configure("ConfigButtons.TFrame", background=bgt)

        self.theme_btn.config(bg=bgt, fg=fg)

        self.reset_btn.set_colors(bg, fg)
        self.reset_btn.set_bg(bgt)

        if step < steps:
            self.after(16, lambda: self.animate_theme(
                bg_from, bg_to, fg_from, fg_to, bg_theme_f, bg_theme_t, step + 1
            ))
        else:
            self.animating = False


    # ================== MOTYW ==================
    def on_show(self):
        current_theme = self.settings.get("theme", "light")
        self.current_theme = current_theme

        if current_theme == "dark":
            self.theme_btn.config(text="☀")
            print("dark")
            self.animate_theme(
                self.app.bg_btn_light, self.app.bg_btn_dark,
                self.app.fg_btn_light, self.app.fg_btn_dark,
                self.app.bg_light, self.app.bg_dark,
                step=30
            )
        else:
            self.theme_btn.config(text="🌙")
            print("light")
            self.animate_theme(
                self.app.bg_btn_dark, self.app.bg_btn_light,
                self.app.fg_btn_dark, self.app.fg_btn_light,
                self.app.bg_dark, self.app.bg_light,
                step=30
            )
