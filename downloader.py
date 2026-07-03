import os
import shutil
import subprocess

import yt_dlp

_FFMPEG_EXE = None


def get_ffmpeg_exe():
    """Return path to a real ffmpeg binary."""
    global _FFMPEG_EXE
    if _FFMPEG_EXE:
        return _FFMPEG_EXE

    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        _FFMPEG_EXE = system_ffmpeg
        return _FFMPEG_EXE

    try:
        import imageio_ffmpeg

        _FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None

    return _FFMPEG_EXE


def _base_ydl_opts(output_folder):
    return {
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "restrictfilenames": True,
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
    }


def _convert_to_mp3(source_path, output_folder):
    ffmpeg_exe = get_ffmpeg_exe()
    if not ffmpeg_exe:
        return source_path

    mp3_path = os.path.join(
        output_folder, os.path.splitext(os.path.basename(source_path))[0] + ".mp3"
    )
    result = subprocess.run(
        [
            ffmpeg_exe,
            "-y",
            "-i",
            source_path,
            "-vn",
            "-acodec",
            "libmp3lame",
            "-b:a",
            "192k",
            mp3_path,
        ],
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(stderr.strip() or "MP3 conversion failed")

    if source_path != mp3_path and os.path.exists(source_path):
        os.remove(source_path)

    return mp3_path


def _download(url, ydl_opts):
    def run(opts):
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info, ydl.prepare_filename(info)

    try:
        return run(ydl_opts)
    except Exception as first_error:
        if "not a bot" not in str(first_error).lower():
            raise

        for browser in ("edge", "chrome", "firefox"):
            browser_opts = dict(ydl_opts)
            browser_opts["cookiesfrombrowser"] = (browser,)
            try:
                return run(browser_opts)
            except Exception:
                continue
        raise first_error


def download_audio(url, output_folder="downoloads"):
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = _base_ydl_opts(output_folder)
    ydl_opts["format"] = "bestaudio/best"

    try:
        info, audio_path = _download(url, ydl_opts)
        mp3_path = _convert_to_mp3(audio_path, output_folder)
        return {
            "title": info.get("title", "Unknown"),
            "path": mp3_path,
        }
    except Exception as e:
        print(f"error {e}")
        return None


def download_video(url, output_folder="downoloads"):
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = _base_ydl_opts(output_folder)
    ydl_opts["format"] = "best[ext=mp4]/best"

    try:
        info, path = _download(url, ydl_opts)
        return {
            "title": info.get("title", "Unknown"),
            "path": path,
        }
    except Exception as e:
        print(f"error {e}")
        return None


if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    result = download_audio(url)
    if result:
        print(f"Downloaded: {result['title']}")
        print(f"Saved to: {result['path']}")
