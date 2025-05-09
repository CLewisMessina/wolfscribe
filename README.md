# 🐺 Wolfscribe

**Convert books into clean, training-ready datasets — with just a few clicks.**  
Part of the [Wolflow](https://wolflow.ai) ecosystem • Built by [@CLewisMessina](https://github.com/CLewisMessina)

> Now with a cleaner, icon-driven interface built on Wolflow’s visual system.

---

## ✨ What is Wolfscribe?

Wolfscribe is a local desktop tool that turns long-form documents (PDFs, EPUBs, and TXT files) into `.txt` or `.csv` datasets — ready for LLM fine-tuning.

Built for indie AI developers, educators, and writers, it’s the fastest way to go from "I have a book" to "I have a dataset."

> **No CLI. No scripts. Just results.**

---

## 📸 Demo Video (Press Play)


https://github.com/user-attachments/assets/2596b35e-6202-4c86-91e9-e9df729f6a18


---

## 📦 Features

- 🧠 **Supports EPUB, PDF, and TXT**
- ✂️ **Smart text chunking** (paragraph, sentence, or custom)
- 🮢 **Drag-and-drop file loading**
- 🔍 **Chunk preview with token counts**
- ⚠️ **Warnings for overlong training chunks (512+ tokens)**
- 📂 **Export as `.txt` or `.csv`** with fully quoted formatting
- 🖥️ **Built with Python + Tkinter + ttkbootstrap**
- 💾 **Session save/load support** (.wsession files)
- 🖱️ **Mousewheel scrolling + tabbed layout**
- 🎨 **Red-hover button style** inspired by Wolfkit
- ❌ **No cloud, no tracking — fully local**

---

## 🥚 Why Use It?

| Use Case | Example |
|----------|---------|
| Fine-tuning your own model | “Train GPT on Moby Dick” |
| Creating flashcards or tutors | “Split a textbook into prompts” |
| Feeding data into RAG/chat pipelines | “Index a reference manual” |
| Building stylistic AI writers | “Clone your writing tone” |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/CLewisMessina/wolfscribe.git
cd wolfscribe
```

### 2. Set up your virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate   # or `source venv/bin/activate` on Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py
```

---

## 📁 Input Support

- `.txt` (plain text)
- `.pdf` (text-based only)
- `.epub` (most standard formats)

---

## 📊 Output Format

- `.txt` — one chunk per line
- `.csv` — one chunk per `"text"` row, fully quoted and Excel-safe

---

## ⚙️ Requirements

- Python 3.10+
- Packages:
  - `transformers`
  - `ebooklib`
  - `beautifulsoup4`
  - `pdfminer.six`
  - `ttkbootstrap`
  - `tkinterdnd2`

---

## ✅ Recently Completed

- [x] Session save/load system
- [x] Scrollable layout with mouse support
- [x] Hover-only red button style
- [x] Custom delimiter toggle logic

## 🗐 Roadmap

- [x] Drag-and-drop file loading
- [x] Grid layout and structured UI
- [ ] Token length visualizer + tokenizer selector
- [ ] Export as `.jsonl`
- [ ] Hugging Face integration ("Send to Wolftrain")
- [ ] Save/load config profiles
- [ ] Export metadata/stats

---


## 🧙‍♂️ Part of the Wolflow Ecosystem

- [🥚 Wolfkit](https://github.com/CLewisMessina/wolfkit) – Test harness for LLM-generated code
- [🐺 Wolftrain](https://github.com/CLewisMessina/wolftrain) – Local LoRA fine-tuning app
- [📈 Wolftrack](https://github.com/CLewisMessina) – Token usage + metrics tracker *(coming soon)*

---

## 🤖 License

Creative Commons CC BY-NC 4.0  
No cloud. No gatekeeping. Just tools.

---

_You write the story. Wolfscribe makes it trainable._
