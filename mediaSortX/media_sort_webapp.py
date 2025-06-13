import os
import shutil
import hashlib
import tempfile
from pathlib import Path
from zipfile import ZipFile

import streamlit as st

# 🌈 PRINCESSCORE THEME HEADER
st.set_page_config(page_title="📸💗 MediaSortX – PrincessCore Sorter", layout="centered")
st.markdown("""
<style>
    .stApp {
        background-image: linear-gradient(to bottom, #1a1a1a, #ff85c0);
        background-attachment: fixed;
    }
</style>
""", unsafe_allow_html=True)

st.title("📸💗 MediaSortX – PrincessCore Sorter")
st.caption("Your dirty little content bin? Fixed. Sorted. Cummed on. 💅")

# --- Constants ---
IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
GIF_EXTENSIONS = ['.gif']
VID_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
RENAME_PREFIXES = {'gif': '(G)-', 'pic': '(P)-', 'vid': '(V)-'}
CATEGORIES = ['GIFS', 'PICS', 'VIDS', 'DUPES']
HASH_DB = set()


def file_hash(path):
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def classify_file(path):
    ext = path.suffix.lower()
    if ext in GIF_EXTENSIONS:
        return 'gif'
    elif ext in IMG_EXTENSIONS:
        return 'pic'
    elif ext in VID_EXTENSIONS:
        return 'vid'
    return None


def prepare_output_folder(base):
    output_dirs = {}
    for cat in CATEGORIES:
        path = Path(base) / cat
        path.mkdir(parents=True, exist_ok=True)
        output_dirs[cat] = path
    return output_dirs


def sort_files(upload_dir, output_dir):
    global HASH_DB
    HASH_DB = set()
    output_dirs = prepare_output_folder(output_dir)

    for root, _, files in os.walk(upload_dir):
        for file in files:
            src = Path(root) / file
            if not src.is_file():
                continue

            category = classify_file(src)
            if not category:
                continue

            hash_val = file_hash(src)
            if hash_val in HASH_DB:
                shutil.copy2(src, output_dirs['DUPES'] / file)
                continue
            HASH_DB.add(hash_val)

            new_name = RENAME_PREFIXES[category] + src.name
            shutil.copy2(src, output_dirs[category.upper() + 'S'] / new_name)

    return output_dir


def zip_output_folder(output_path):
    zip_path = Path(tempfile.gettempdir()) / "sorted_media.zip"
    with ZipFile(zip_path, 'w') as zipf:
        for folder, _, files in os.walk(output_path):
            for file in files:
                file_path = Path(folder) / file
                arcname = file_path.relative_to(output_path)
                zipf.write(file_path, arcname)
    return zip_path


# --- Streamlit UI ---
uploaded_files = st.file_uploader("Drop your media here (multiple allowed)", type=None, accept_multiple_files=True)

if uploaded_files:
    with tempfile.TemporaryDirectory() as temp_upload:
        for file in uploaded_files:
            file_path = Path(temp_upload) / file.name
            with open(file_path, 'wb') as f:
                f.write(file.read())

        with st.spinner("Sorting and cleaning up your mess..."):
            output_folder = Path(tempfile.mkdtemp())
            sort_files(temp_upload, output_folder)
            zip_path = zip_output_folder(output_folder)

        st.success("Sorted and packed!")

        # 📁 Preview sorted folders
        st.subheader("💖 Sorted Preview")
        for category in sorted(os.listdir(output_folder)):
            st.markdown(f"### 📂 {category}")
            cat_path = Path(output_folder) / category
            files = os.listdir(cat_path)
            if not files:
                st.write("*(empty)*")
            else:
                for file in sorted(files):
                    st.markdown(f"• `{file}`")

        # 📦 Download
        with open(zip_path, "rb") as f:
            st.download_button("📥 Download Sorted Zip", f, file_name="sorted_media.zip")