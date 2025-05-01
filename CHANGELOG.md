# 📋 CHANGELOG.md

## 🐺 Wolfscribe — Changelog

---

### v1.1 – Drag-and-Drop Release (2025-04-30)
**This update adds a major UX upgrade:** drag-and-drop file loading!

#### ✨ Added
- 📥 Drag-and-drop support for `.txt`, `.pdf`, and `.epub` files
- Auto-updates file label when file is dropped
- Full support for Windows; fallback-friendly on macOS/Linux

#### ✅ Improved
- Confirmed compatibility with Wolfkit staging workflow
- Updated `README.md` and `requirements.txt` to reflect changes

#### 🔧 Internal
- Replaced `ttkb.Window` with `TkinterDnD.Tk` in `main.py`
- Registered `DND_FILES` on `AppFrame` and bound `<<Drop>>` event
- Added `tkinterdnd2` as a new dependency

---

### v1.0 – Initial Launch (2025-04-XX)
The first working version of Wolfscribe — a local app that converts long-form books into clean, token-counted `.txt` or `.csv` datasets.

#### 🚀 Core Features
- Import `.epub`, `.pdf`, and `.txt` files
- Clean and chunk text by paragraph, sentence, or custom delimiter
- View preview chunks with token count warnings
- Export as `.txt` or `.csv`
- Fully local: no tracking, no cloud

---

_You write the story. Wolfscribe makes it trainable._
