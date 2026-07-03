import os

import yt_dlp


def download_audio(url, output_folder="downoloads"):
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            base_path = ydl.prepare_filename(info)
            mp3_path = os.path.splitext(base_path)[0] + ".mp3"
            return {
                "title": info.get("title", "Unknown"),
                "path": mp3_path,
            }
    except Exception as e:
        print(f"error {e}")
        return None


def download_video(url, output_folder="downoloads"):
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return {
                "title": info.get("title", "Unknown"),
                "path": ydl.prepare_filename(info),
            }
    except Exception as e:
        print(f"error {e}")
        return None


if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    result = download_audio(url)
    if result:
        print(f"Downloaded: {result['title']}")
