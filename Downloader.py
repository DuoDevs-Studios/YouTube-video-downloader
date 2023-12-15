import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import yt_dlp
import json
import os

save_location_file_path = os.path.join("C:/youtube_downloader", "last_save_location.txt")
dark_mode_file_path = os.path.join("C:/youtube_downloader", "dark_mode.txt")

if not os.path.exists("C:/youtube_downloader"):
    os.makedirs("C:/youtube_downloader")

try:
    with open(save_location_file_path, "r") as file:
        last_save_location = file.read()
except FileNotFoundError:
    last_save_location = ""

dark_mode_enabled = False

try:
    with open(dark_mode_file_path, "r") as file:
        dark_mode_enabled = bool(int(file.read()))
except FileNotFoundError:
    pass

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Video Downloader")
        self.set_theme()

        self.create_main_page()

    def set_theme(self):
        theme = "clam"  

        if dark_mode_enabled:
            theme = "clam"  

        style = ttk.Style()
        style.theme_use(theme)

        if dark_mode_enabled:
            style.configure("TFrame", background="#2C2F33")
            style.configure("TLabel", background="#2C2F33", foreground="white")
            style.configure("TButton", background="#7289DA", foreground="white")
            style.configure("TEntry", fieldbackground="#4F5459", foreground="white")

        self.master.configure(bg="#2C2F33")

    def create_main_page(self):
        self.url_label = ttk.Label(self.master, text="Video URL:")
        self.url_label.grid(row=0, column=0)
        self.url_entry = ttk.Entry(self.master, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)

        self.save_label = ttk.Label(self.master, text="Save Location:")
        self.save_label.grid(row=1, column=0)
        self.save_entry = ttk.Entry(self.master, width=50)
        self.save_entry.grid(row=1, column=1, padx=10, pady=5)

        self.browse_button = ttk.Button(self.master, text="Browse", command=self.browse_save_location)
        self.browse_button.grid(row=1, column=2, padx=10, pady=5)

        self.save_entry.insert(0, last_save_location)

        self.download_button = ttk.Button(self.master, text="Download", command=self.download_video)
        self.download_button.grid(row=2, column=1, padx=10, pady=10)

        self.status_label = ttk.Label(self.master, text="")
        self.status_label.grid(row=3, column=0, columnspan=2)

        self.options_button = ttk.Button(self.master, text="Options", command=self.show_options)
        self.options_button.grid(row=4, column=0, columnspan=2, pady=10)

    def show_options(self):
        self.options_window = tk.Toplevel(self.master)
        self.options_window.title("Options")

        self.options_window.geometry("300x150")

        dark_mode_label = ttk.Label(self.options_window, text="Dark Mode:")
        dark_mode_label.grid(row=0, column=0, padx=10, pady=10)

        dark_mode_var = tk.BooleanVar(value=dark_mode_enabled)
        dark_mode_checkbox = ttk.Checkbutton(self.options_window, text="Enable Dark Mode", variable=dark_mode_var, command=self.toggle_dark_mode)
        dark_mode_checkbox.grid(row=0, column=1, padx=10, pady=10)

        self.options_window.protocol("WM_DELETE_WINDOW", self.show_main_page)

        self.hide_main_page()

    def toggle_dark_mode(self):
        global dark_mode_enabled
        dark_mode_enabled = not dark_mode_enabled

        with open(dark_mode_file_path, "w") as file:
            file.write(str(int(dark_mode_enabled)))

        self.set_theme()

    def browse_save_location(self):
        global last_save_location
        save_location = filedialog.askdirectory(initialdir=last_save_location)
        self.save_entry.delete(0, tk.END)
        self.save_entry.insert(0, save_location)

        with open(save_location_file_path, "w") as file:
            file.write(save_location)

        last_save_location = save_location

    def download_video(self):
        video_url = self.url_entry.get()
        save_location = self.save_entry.get()
        ydl_opts = {
            'outtmpl': save_location + '/%(title)s.%(ext)s',
            'skip_unavailable_fragments': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            self.status_label.config(text="Download completed successfully!")
        except Exception as e:
            self.status_label.config(text="Error: " + str(e))

    def hide_main_page(self):
        self.master.withdraw()

    def show_main_page(self):
        self.options_window.destroy() 
        self.master.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
