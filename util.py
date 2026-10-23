from pathlib import Path
import yt_dlp, json


def load_data(filepath="data/list.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def save_data(data, filepath="data.json"):
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def playlist(url: str):
    """
    Przyjmuje link do playlisty YouTube.
    Zwraca listę słowników zawierających ID i tytuł każdego filmu.
    """
    if "://" not in url:
        url = f"https://www.youtube.com/playlist?list={url}"

    options = {
        "extract_flat": True,
        "skip_download": True,
        "quiet": True,
        "ignoreerrors": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)

    if not info:
        raise ValueError("Nie udało się pobrać informacji o playliście.")

    return [
        {
            "id": entry["id"],
            "title": entry.get("title"),
        }
        for entry in (info.get("entries") or [])
        if entry and entry.get("id")
    ]


def download(video_id: str, subdirectory: str, directoros: str) -> str:
    """
    Pobiera audio z YouTube na podstawie ID.
    Zapisuje plik w katalogu static/<subdirectory>.
    Zwraca ścieżkę do pobranego pliku.
    """
    subdir = Path(subdirectory)

    # Podkatalog musi być względny i nie może wychodzić poza media.
    if subdir.is_absolute() or ".." in subdir.parts:
        raise ValueError("Podaj prawidłowy podkatalog wewnątrz media/.")

    output_dir = directoros / subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    url = f"https://www.youtube.com/watch?v={video_id}"

    options = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return str(Path(filename))
