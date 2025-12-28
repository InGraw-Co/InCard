# InCard Editor

**InCard Editor** — free, open-source collectible card editor.

I created this project to quickly and comfortably create, edit and export character cards with images, stats and simple template settings. The app is written in Python (with a modern GUI) and runs on Windows as well as on other systems that support Python.

> SEO: card editor, collectible card editor, card generator, card editor app, TCG card creator, RPG card maker, Python

---
<p align="center">
  <img src="assets/incard-gif.gif" alt="InCard Editor demo" width="500">
</p>

---

## ✅ Key features

- Easy to modify, split into frames/modules: `WelcomeFrame`, `IntermediateFrame`, `EditorFrame`, `FinishFrame`, `ConfigFrame` ⚙️
- Create a session with any number of cards (1–999) 💠
- Card fields (I plan to add more customization later): **Name**, **Rarity**, **Type**, **Property**, **Accuracy** 🔤
- Icon selection and editing:
  - Supports common formats (PNG, JPG, BMP, WebP, (SVG planned later)) 🖼️
  - Preview, drag to position and zoom (drag & zoom) ✔️
- List of saved cards with thumbnails and quick load for editing 📋
- Light and Dark themes and language files in `settings/lang/` — you can add your own translations 🌗
- Configurable values: `rarity`, `types`, `properties` in `settings/config.json` (I'm working on changing this in the app) 🔧
- Temporary NDJSON storage (`cache/cards.ndjson`) and final export to `cache/cards.json` with icons saved to `cache/icons/` 🗂️
- Restore an interrupted session (restore) ⚠️
- Compatibility with multiple systems: **Windows, Linux, macOS**

---

## 🔜 Project status — important

This project is **in progress** and not yet finished, but it is usable for testing and for quickly validating the card-creation workflow (alpha/beta). I plan to actively add features such as export to PNG/PDF and UX improvements. Right now the app exports `cards.json` and icons to an `icons/` folder; later it will be able to convert this data into ready-to-print card templates.

### 🌍 Language support

I plan to support **20 languages** — currently I use language files in `settings/lang/` (Polish), and I will add translations progressively. If you want to help, add a translation file and open an issue.

---

## 🚀 Quick start (how I run it)

1. Requirements:
   - Python 3.8+
   - Pillow (`pip install pillow`)
   - Tkinter (usually included with Python)
   - If you miss a dependency (I sometimes add new ones), install it with `pip install <package>`
   - You can install requirements library from file `install.bat` or `install.sh`
2. Run:
   - Windows: double-click `start.bat` or run `python main.py`
   - Other systems (Linux, macOS): `./start.sh` or run `python3 main.py`

3. Quick workflow:
   - `New project` → enter the number of cards → `Next`
   - In the editor pick an icon, set position/zoom, fill in information as needed and click **Save and next**
   - After saving all cards close the session — `cache/` will contain `cards.json` and an `icons/` folder with PNGs
   - To edit a saved card: open `All cards` (menu `All cards`), select the card you want to edit, make changes and save — you'll continue from where you left off.

---

## 📁 Project structure (important files)

- `main.py` — app launcher
- `config.py` — settings, languages, helper functions
- `paths.py` — constants and sizes
- `frames/` — app sections and editor UI
- `settings/` — config samples and translations
- `assets/` — images and templates
- `cache/` — temporary and output files

---

## 💡 Customization & development (how you can help)

- Edit `settings/config_sample/config.json` to add custom rarities, types and properties.
- Add translations in `settings/lang/` (JSON) — I welcome contributions.
- If you have ideas for new features, please suggest them via an issue.

---

## ⚠️ Limitations

- Currently the app saves data to JSON and icons as PNG; there is no automatic export to PDF/print sheets yet.

---

## 🤝 Contact & support

- YouTube channel: https://www.youtube.com/@InGraw
- To report bugs or suggest features: please open an issue on GitHub

