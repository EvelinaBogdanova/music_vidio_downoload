import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

from downloader import download_audio, download_video


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video / Audio Downloader")
        self.root.geometry("600x420")

        tk.Label(root, text="Enter YouTube URL:").pack(pady=5)
        self.url_entry = tk.Entry(root, width=70)
        self.url_entry.pack(pady=5)

        mode_frame = tk.Frame(root)
        mode_frame.pack(pady=5)
        self.download_mode = tk.StringVar(value="audio")
        tk.Radiobutton(
            mode_frame, text="Audio (MP3)", variable=self.download_mode, value="audio"
        ).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(
            mode_frame, text="Video (MP4)", variable=self.download_mode, value="video"
        ).pack(side=tk.LEFT, padx=10)

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
        mode = self.download_mode.get()
        self.log(f"Downloading {mode}...")

        thread = threading.Thread(target=self.run_download, args=(url, mode))
        thread.start()

    def run_download(self, url, mode):
        if mode == "video":
            result = download_video(url)
        else:
            result = download_audio(url)

        if not result:
            self.log("Download failed. Please check the URL and try again.")
        else:
            self.log(f"Download successful: {result['title']}")
            self.log(f"Saved to: {result['path']}")
        self.download_btn.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    YouTubeDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
