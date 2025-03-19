import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

UNPACK_DIR = "gamedata"
CONVERTER = "converter.exe"

MODE_DESCRIPTIONS = {
    "-2947ru": "Русская релизная версия Тень Чернобыля",
    "-2947ww": "Мировая релизная версия Тень Чернобыля",
    "-xdb": "Релизные версии Чистое Небо и Зов Припяти"
}

class DBUnpackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Распаковщик db/xdb файлов")
        self.root.geometry("800x500")
        self.file_var = ttk.StringVar()
        self.mode_var = ttk.StringVar(value="-2947ru")
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        file_frame = ttk.LabelFrame(main_frame, text="Выбор файлов", padding=5)
        file_frame.pack(fill=X, pady=5)
        ttk.Label(file_frame, text="Выберите файлы игры (путь не должен содержать кириллицу):").pack(side=LEFT, padx=5)
        ttk.Entry(file_frame, textvariable=self.file_var, width=40, state="readonly").pack(side=LEFT, padx=5, fill=X, expand=True)
        ttk.Button(file_frame, text="Обзор", command=self.select_files, bootstyle=SUCCESS).pack(side=LEFT, padx=5)

        mode_frame = ttk.LabelFrame(main_frame, text="Режим распаковки", padding=5)
        mode_frame.pack(fill=X, pady=5)
        ttk.Label(mode_frame, text="Выберите режим:").pack(side=LEFT, padx=5)
        mode_combobox = ttk.Combobox(mode_frame, textvariable=self.mode_var, values=list(MODE_DESCRIPTIONS.keys()), bootstyle=PRIMARY)
        mode_combobox.pack(side=LEFT, padx=5, fill=X, expand=True)
        mode_combobox.bind("<<ComboboxSelected>>", self.update_mode_description)

        self.mode_description = ttk.Label(main_frame, text=MODE_DESCRIPTIONS[self.mode_var.get()])
        self.mode_description.pack(fill=X, pady=5)

        self.run_button = ttk.Button(main_frame, text="Начать распаковку", command=self.run_unpacking, bootstyle=(PRIMARY, OUTLINE))
        self.run_button.pack(pady=10)

        self.progress_bar = ttk.Progressbar(main_frame, length=300, mode="determinate", bootstyle=SUCCESS)
        self.progress_bar.pack(fill=X, pady=5)

        self.status_label = ttk.Label(main_frame, text="Ожидание...")
        self.status_label.pack(pady=5)

        log_frame = ttk.LabelFrame(main_frame, text="Лог", padding=5)
        log_frame.pack(fill=BOTH, expand=True, pady=5)
        self.log_text = ScrolledText(log_frame, height=10, width=50, autohide=True)
        self.log_text.pack(fill=BOTH, expand=True)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("db и xdb файлы", "*.db*;*.xdb*")])
        if files:
            self.file_var.set("; ".join(files))

    def update_mode_description(self, *args):
        self.mode_description.config(text=MODE_DESCRIPTIONS.get(self.mode_var.get(), ""))

    def run_unpacking(self):
        mode = self.mode_var.get()
        files = self.file_var.get().split("; ")

        if not files or files == [""]:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите файлы.")
            return

        os.makedirs(UNPACK_DIR, exist_ok=True)

        self.progress_bar["value"] = 0
        progress_step = 100 / len(files)

        self.log_text.delete(1.0, END)

        for idx, file_path in enumerate(files, start=1):
            self.status_label.config(text=f"Распаковка {os.path.basename(file_path)} ({idx}/{len(files)})...")
            self.root.update_idletasks()

            result = subprocess.run(
                [CONVERTER, "-unpack", mode, file_path, "-dir", UNPACK_DIR],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:
                log_msg = f"[УСПЕХ] {os.path.basename(file_path)} успешно распакован!\n"
            else:
                log_msg = f"[ОШИБКА] Не удалось распаковать {os.path.basename(file_path)}!\n{result.stderr}\n"

            self.log_text.insert(END, log_msg)
            # Используем метод text для прокрутки вниз
            self.log_text.text.yview_moveto(1.0)  # Прокрутка к концу

            self.progress_bar["value"] += progress_step

        self.status_label.config(text="✅ Завершено!")
        messagebox.showinfo("Готово", "Все выбранные файлы успешно распакованы!")

def main():
    root = ttk.Window(themename="cosmo")
    app = DBUnpackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()