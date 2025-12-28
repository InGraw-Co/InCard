#!/usr/bin/env bash
set -euo pipefail

# Move to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Install into .venv if present, otherwise use system Python
if [ -f ".venv/bin/activate" ]; then
  echo "Activating .venv and installing requirements..."
  # shellcheck disable=SC1091
  . .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "No .venv found; using system Python to install requirements..."
  if command -v python3 >/dev/null 2>&1; then
    PY=python3
  elif command -v python >/dev/null 2>&1; then
    PY=python
  else
    echo "Error: Python is not installed. Install Python 3 and try again." >&2
    exit 1
  fi
  "$PY" -m pip install --upgrade pip
  "$PY" -m pip install -r requirements.txt
fi

# Check for tkinter availability
if ! python -c "import tkinter" >/dev/null 2>&1; then
  cat <<'MSG'

⚠️  tkinter is not available in your Python environment.
- On Debian/Ubuntu: sudo apt-get install python3-tk
- On Fedora: sudo dnf install python3-tkinter
- On Arch: sudo pacman -S tk
- On macOS (Homebrew): brew install tcl-tk  (you may need to reinstall/rebuild Python to use Homebrew's tcl-tk)
- On Windows: ensure you installed the official Python installer with Tcl/Tk support

If the GUI fails to start after installing system packages, try creating a fresh virtualenv and running this script again.
MSG
fi

echo "All done."
