from io import BytesIO

import requests
from mutagen.id3 import APIC, ID3, TIT2, TPE1
from mutagen.mp3 import MP3
from PIL import Image


def add_metadate(file_path, title, artist="Unknown Artist", cover_url=None):
    try:
        audio = MP3(file_path, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()
        audio.tags.add(TPE1(encoding=3, text=artist))
        audio.tags.add(TIT2(encoding=3, text=title))

        if cover_url:
            response = requests.get(cover_url)
            img = Image.open(BytesIO(response.content))
            img_byte_arr = BytesIO()
            img.convert("RGB").save(img_byte_arr, format="JPEG")

            audio.tags.add(
                APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc="Cover",
                    data=img_byte_arr.getvalue(),
                )
            )
        audio.save()
        print(f"Metadata added to {file_path}")
    except Exception as e:
        print(f"Error adding metadata to {file_path}: {e}")


edit_tags = add_metadate
