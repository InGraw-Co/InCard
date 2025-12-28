# ================== BIBLIOTEKI ==================
import os

# ================== PODSTAWOWE ŚCIEŻKI ==================
WIN_W, WIN_H = 1500, 1200
ICON_SIZE = 512

SETTINGS_FILE = "settings/settings.json"
LANG_DIR = "settings/lang"
CONFIG_DIR = "settings/config_sample/"

ASSETS_DIR = "assets"
CACHE_DIR = "cache"
ICON_DIR = os.path.join(CACHE_DIR, "icons")
CARDS_TMP = os.path.join(CACHE_DIR, "cards.ndjson")
META_FILE = os.path.join(CACHE_DIR, "cards.meta.json")
ICON = os.path.join(ASSETS_DIR, "logo.png")
MAIN_CONFIG = os.path.join("settings", "config.json")

os.makedirs(ICON_DIR, exist_ok=True)
