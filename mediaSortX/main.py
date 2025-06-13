import os
import shutil
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

from pathlib import Path
from mimetypes import guess_type

OUTPUT_DIRS = ['GIFS', 'PICS', 'VIDS', 'DUPES']
RENAME_PREFIXES = {
    'gif': '(G)-',
    'pic': '(P)-',
    'vid': '(V)-'
}
IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
GIF_EXTENSIONS = ['.gif']
VID_EXTENSIONS = ['.mp4', '.mov', '.avi', '.mkv', '.webm']

HASH_DB = set()


def file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
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


def prepare_output(base_output):
    for folder in OUTPUT_DIRS:
        Path(base_output, folder).mkdir(parents=True, exist_ok=True)


def move_file_clean(src_path, base_output):
    category = classify_file(src_path)
    if not category:
        return

    hash_val = file_hash(src_path)
    if hash_val in HASH_DB:
        shutil.copy2(src_path, Path(base_output, 'DUPES', src_path.name))
        return
    HASH_DB.add(hash_val)

    prefix = RENAME_PREFIXES[category]
    new_name = prefix + src_path.name
    target_dir = Path(base_output, category.upper() + 'S')
    shutil.copy2(src_path, target_dir / new_name)


def handle_input(paths, base_output):
    for item in paths:
        p = Path(item)
        if p.is_dir():
            for root, _, files in os.walk(p):
                for file in files:
                    move_file_clean(Path(root) / file, base_output)
        elif p.is_file():
            move_file_clean(p, base_output)


class MediaSorterApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("MEDIA-SORT-X")
        self.geometry("500x300")
        self.configure(bg='black')

        self.drop_zone = tk.Label(self, text="Drop Files or Folders Here\nOr Click Below to Browse",
                                   bg="#1e1e1e", fg="white", relief="ridge", bd=2,
                                   width=50, height=10)
        self.drop_zone.pack(pady=30)
        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind('<<Drop>>', self.drop_handler)

        browse_btn = tk.Button(self, text="Browse Files", command=self.browse_files)
        browse_btn.pack()

        self.output_dir = os.path.join(os.getcwd(), 'output')
        prepare_output(self.output_dir)

    def drop_handler(self, event):
        paths = self.split_drop_paths(event.data)
        handle_input(paths, self.output_dir)
        messagebox.showinfo("Done", "Sorting complete.")

    def browse_files(self):
        files = filedialog.askopenfilenames()
        handle_input(files, self.output_dir)
        messagebox.showinfo("Done", "Sorting complete.")

    def split_drop_paths(self, data):
        return self.tk.splitlist(data)


if __name__ == '__main__':
    app = MediaSorterApp()
    app.mainloop()
