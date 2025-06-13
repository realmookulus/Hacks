# 👑 MediaSortX – Goon-Ready Content Sorter

**Organize your chaos.**  
Drag-n-drop your mess of gifs, pics, and vids — and MediaSortX will clean, sort, rename, and pack it into a princess-worthy download.

---

## 🖥️ Versions

- `main.py`: local GUI version (run with Tkinter)
- `media_sort_webapp.py`: Streamlit-based web version for remote use

---

## 🌐 Live on Streamlit Cloud

Deploy this via [Streamlit.io/cloud](https://streamlit.io/cloud) by pointing to:

- **Repo:** `yourusername/Hacks`
- **App File Path:** `mediaSortX/media_sort_webapp.py`

---

## 💖 Features

- Drag and drop files or folders
- Automatically sorts into:
  - 🌀 `GIFS/`
  - 📸 `PICS/`
  - 📹 `VIDS/`
  - 🗑 `DUPES/` (by hash)
- Adds prefix to filenames: `(G)-`, `(P)-`, `(V)-`
- Downloads output as a zip
- Princess-mode theme: baby pink + black gradient

---

## 🛠️ To Run Locally

```bash
# Create venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run GUI
python main.py

# Run WebApp
streamlit run media_sort_webapp.py