from PIL import Image
import pillow_heif
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def convert_heic_to_jpg(heic_path, jpg_path):
    try:
        heif_file = pillow_heif.open_heif(heic_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(jpg_path, "JPEG")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert {heic_path} to JPG.\n{e}")

def open_files():
    global files
    files = filedialog.askopenfilenames(filetypes=[("HEIC files", "*.heic")])
    if files:
        progress_bar["maximum"] = len(files)
        convert_button.config(state=tk.NORMAL)
        listbox.delete(0, tk.END)
        for file in files:
            listbox.insert(tk.END, file)

def convert_files():
    for file in files:
        if file.lower().endswith('.heic'):
            jpg_path = file.rsplit('.', 1)[0] + '.jpg'
            convert_heic_to_jpg(file, jpg_path)
            progress_bar.step()
    messagebox.showinfo("Info", "Conversion completed!")
    convert_button.config(state=tk.DISABLED)

root = tk.Tk()
root.title("HEIC to JPG Converter")

frame = tk.Frame(root, width=400, height=200, bg='white')
frame.pack_propagate(False)
frame.pack(fill=tk.BOTH, expand=True)

open_button = tk.Button(frame, text="Open HEIC Files", command=open_files)
open_button.pack(pady=20)

convert_button = tk.Button(frame, text="Convert to JPG", command=convert_files, state=tk.DISABLED)
convert_button.pack(pady=20)

listbox = tk.Listbox(frame)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
progress_bar.pack(fill=tk.X, padx=10, pady=10)

root.mainloop()
