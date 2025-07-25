import os
import shutil
from tkinter import *
from tkinter import ttk, filedialog, messagebox, scrolledtext

def file_manage():
    managing_path = path_var.get().strip()
    if not managing_path or not os.path.exists(managing_path):
        messagebox.showerror("Error", "Invalid path provided!")
        return

    # File categories
    pdf_files, text_files, images, miscs, others = [], [], [], [], []

    if not os.path.exists("output.txt"):
        open("output.txt", "w").close()

    with open("output.txt", "a+") as f:
        for files in os.listdir(managing_path):
            file_path = os.path.join(managing_path, files)
            if not os.path.isdir(file_path):
                if files.endswith('.pdf'):
                    pdf_files.append(files)
                elif files.endswith(('.jpg', '.png')):
                    images.append(files)
                elif files.endswith(('.txt', '.html', '.c', '.py', '.docx')):
                    text_files.append(files)
                elif files.endswith(('.mp4', '.mkv', '.mp3')):
                    miscs.append(files)
                else:
                    others.append(files)

        folders = {
            "pdf_files": pdf_files,
            "text_files": text_files,
            "images": images,
            "miscs": miscs,
            "others": others
        }

        for folder_name, file_list in folders.items():
            dest_folder = os.path.join(managing_path, folder_name)
            os.makedirs(dest_folder, exist_ok=True)
            for file in file_list:
                source = os.path.join(managing_path, file)
                shutil.move(source, dest_folder)
                f.write(f"MOVED - {file}\n")

        f.write("Process Completed\n")

    status_label.config(text="✅ Files organized successfully!")
    update_output()

def update_output():
    if not os.path.exists("output.txt"):
        return
    with open("output.txt", "r") as w:
        data = w.read()
    output_box.delete(1.0, END)
    output_box.insert(END, data)

def browse_folder():
    selected_path = filedialog.askdirectory()
    if selected_path:
        path_var.set(selected_path)
        status_label.config(text="📂 Path selected. Click 'Organize' to continue.")

def show_instructions():
    messagebox.showinfo(
        "Instructions",
        "1. Click 'Browse' to select a folder.\n"
        "2. Click 'Organize' to sort files.\n"
        "3. Output shows moved files by type."
    )

# GUI Setup
root = Tk()
root.title("📁 File Organizer - DESTINII")
root.geometry("800x600")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TEntry", padding=5)

# Title Label
ttk.Label(root, text="🗂️ File Organizer", font=("Segoe UI", 20, "bold")).pack(pady=10)

# Frame for folder input
frame_path = Frame(root, padx=10, pady=10)
frame_path.pack(fill=X)

path_var = StringVar()
ttk.Label(frame_path, text="Select Folder:").pack(side=LEFT)
ttk.Entry(frame_path, textvariable=path_var, width=60).pack(side=LEFT, padx=10)
ttk.Button(frame_path, text="Browse", command=browse_folder).pack(side=LEFT)

# Button Frame
frame_buttons = Frame(root, pady=10)
frame_buttons.pack()

ttk.Button(frame_buttons, text="📜 Instructions", command=show_instructions).pack(side=LEFT, padx=10)
ttk.Button(frame_buttons, text="🚀 Organize", command=file_manage).pack(side=LEFT, padx=10)

# Output Text Area
ttk.Label(root, text="📄 Output Log:").pack(anchor=W, padx=20)

output_box = scrolledtext.ScrolledText(root, width=95, height=20, font=("Consolas", 10))
output_box.pack(padx=20, pady=5)

# Status Label
status_label = Label(root, text="Waiting for folder selection...", fg="blue", font=("Segoe UI", 10, "italic"))
status_label.pack(pady=5)

# Load any previous output
update_output()

root.mainloop()
