import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import shutil
from datetime import datetime
from PIL import Image

# データファイルと画像保存フォルダのパス
DATA_FILE = 'blog_data.json'
IMAGE_FOLDER = 'uploads'
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def resize_image(input_path, output_path, size=(300, 200)):
    with Image.open(input_path) as img:
        img = img.resize(size)
        img.save(output_path)

# 投稿データを保存する関数
def save_post():
    title = title_entry.get()
    author = author_entry.get()
    content = content_text.get("1.0", tk.END).strip()
    image_path = image_path_var.get()

    if not title or not content:
        messagebox.showerror("エラー", "タイトルと内容は必須です。")
        return

    # 画像を保存
    image_url = None
    if image_path:
        image_name = os.path.basename(image_path)
        target_path = os.path.join(IMAGE_FOLDER, image_name)
        resize_image(image_path, target_path)
        # shutil.copy(image_path, target_path)
        image_url = '/' + target_path.replace('\\', '/')

    # JSONファイルに保存
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            posts = json.load(f)
    else:
        posts = []

    posts.append({
        'title': title,
        'author': author,
        'content': content,
        'image': image_url,
        "timestamp": datetime.now().isoformat()
    })

    with open(DATA_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

    messagebox.showinfo("成功", "記事が投稿されました！")
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    image_path_var.set("")

# 画像ファイルを選択する関数
def select_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("画像ファイル", "*.jpg;*.jpeg;*.png;*.gif")]
    )
    if file_path:
        image_path_var.set(file_path)

# Tkinterウィンドウの設定
root = tk.Tk()
root.title("ブログ投稿アプリ")

# UI要素の配置
tk.Label(root, text="タイトル:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
title_entry = tk.Entry(root, width=50)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="文責:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
author_entry = tk.Entry(root, width=50)
author_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="内容:").grid(row=2, column=0, sticky="ne", padx=5, pady=5)
content_text = tk.Text(root, width=50, height=10)
content_text.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="画像:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
image_path_var = tk.StringVar()
image_entry = tk.Entry(root, textvariable=image_path_var, width=40, state="readonly")
image_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
tk.Button(root, text="参照", command=select_image).grid(row=3, column=2, padx=5, pady=5)

tk.Button(root, text="投稿", command=save_post).grid(row=4, column=1, pady=10)

root.mainloop()
