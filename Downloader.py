import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import yt_dlp
import json

last_save_location = ""

def open_supported_websites():
    supported_websites_window = tk.Toplevel(root)
    supported_websites_window.title("Supported Websites")

    try:
        with open("supported_websites.json", "r") as json_file:
            supported_websites = json.load(json_file)
    except FileNotFoundError:
        supported_websites = []

    listbox = tk.Listbox(supported_websites_window, width=50)
    listbox.pack(padx=10, pady=10)

    for website in supported_websites:
        listbox.insert(tk.END, website)

    search_entry = ttk.Entry(supported_websites_window, width=30)
    search_entry.pack(padx=10, pady=5)

    search_button = ttk.Button(supported_websites_window, text="Search")
    search_button.pack(padx=10, pady=5)

def browse_save_location():
    global last_save_location  
    save_location = filedialog.askdirectory(initialdir=last_save_location)
    save_entry.delete(0, tk.END)
    save_entry.insert(0, save_location)
    last_save_location = save_location  

def download_video():
    video_url = url_entry.get()
    save_location = save_entry.get()
    ydl_opts = {
        'outtmpl': save_location + '/%(title)s.%(ext)s',
        'skip_unavailable_fragments': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        status_label.config(text="Download completed successfully!")
    except Exception as e:
        status_label.config(text="Error: " + str(e))

root = tk.Tk()
root.title("YouTube Video Downloader")

url_label = ttk.Label(root, text="Video URL:")
url_label.grid(row=0, column=0)
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

save_label = ttk.Label(root, text="Save Location:")
save_label.grid(row=1, column=0)
save_entry = ttk.Entry(root, width=50)
save_entry.grid(row=1, column=1, padx=10, pady=5)

browse_button = ttk.Button(root, text="Browse", command=browse_save_location)
browse_button.grid(row=1, column=2, padx=10, pady=5)

download_button = ttk.Button(root, text="Download", command=download_video)
download_button.grid(row=2, column=1, padx=10, pady=10)

status_label = ttk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=2)

root.mainloop()
