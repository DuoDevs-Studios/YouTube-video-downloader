import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import yt_dlp
import json
import os

save_location_file_path = os.path.join("C:/youtube_downloader", "last_save_location.txt")

if not os.path.exists("C:/youtube_downloader"):
    os.makedirs("C:/youtube_downloader")

try:
    with open(save_location_file_path, "r") as file:
        last_save_location = file.read()
except FileNotFoundError:
    last_save_location = ""

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Video Downloader")

        self.url_label = ttk.Label(master, text="Video URL:")
        self.url_label.grid(row=0, column=0)
        self.url_entry = ttk.Entry(master, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5)

        self.save_label = ttk.Label(master, text="Save Location:")
        self.save_label.grid(row=1, column=0)
        self.save_entry = ttk.Entry(master, width=50)
        self.save_entry.grid(row=1, column=1, padx=10, pady=5)

        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_save_location)
        self.browse_button.grid(row=1, column=2, padx=10, pady=5)

        self.save_entry.insert(0, last_save_location)

        self.download_button = ttk.Button(master, text="Download", command=self.download_video)
        self.download_button.grid(row=2, column=1, padx=10, pady=10)

        self.status_label = ttk.Label(master, text="")
        self.status_label.grid(row=3, column=0, columnspan=2)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
