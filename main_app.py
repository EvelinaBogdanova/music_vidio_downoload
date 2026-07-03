import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

from downloader import download_audio


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Downloader")
        self.root.geometry("600x400")

        tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
        self.url_entry = tk.Entry(root, width=70)
        self.url_entry.pack(pady=5)

        self.download_btn = tk.Button(root, text="Download", command=self.start_download)
        self.download_btn.pack(pady=5)

        self.log_text = scrolledtext.ScrolledText(root, height=15, state="normal")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        self.download_btn.config(state=tk.DISABLED)
        self.log("Downloading...")

        thread = threading.Thread(target=self.run_download, args=(url,))
        thread.start()

    def run_download(self, url):
        result = download_audio(url)
        if not result:
            self.log("Download failed. Please check the URL and try again.")
        else:
            self.log(f"Download successful: {result['title']}")
        self.download_btn.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    YouTubeDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
