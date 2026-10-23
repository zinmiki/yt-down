from pick import pick
from util import *


def aktualizujPlayliste(selected_playlist, items, filepath="data/list.json"):
    new_items = playlist(selected_playlist["ref"])
    previous_items = selected_playlist.get("items", [])

    previous_by_id = {item["id"]: item for item in previous_items}
    new_ids = {item["id"] for item in new_items}

    changes = [
        {"change": "added", "item": item}
        for item in new_items
        if item["id"] not in previous_by_id
    ]
    changes.extend(
        {"change": "removed", "item": item}
        for item in previous_items
        if item["id"] not in new_ids
    )

    if not changes:
        return changes

    updated_items = []
    for item in new_items:
        updated_item = {**previous_by_id.get(item["id"], {}), **item}
        if item["id"] not in previous_by_id:
            updated_item["filename"] = download(
                item["id"], selected_playlist["dir"], items["savedir"]
            )
        updated_items.append(updated_item)

    selected_playlist["items"] = updated_items
    selected_playlist["changes"] = changes
    selected_playlist.pop("uptodate", None)
    selected_playlist.pop("downall", None)
    save_data(items, filepath)

    return changes


def dodajPlayliste(items, filepath="data/list.json"):
    print("=== Dodawanie playlisty ===")
    print("\nNazwa playlisty:")
    name = input("> ")
    print("\nŁączenie playlisty z YouTube")
    print("Aby to działało playlista musi być publiczna lub niepubliczna")
    print("Podaj link youtube.com/playlist?list:")
    ref = input("> ")
    print("\nDodaję playlistę...")
    items["playlists"].append({
        "name": name,
        "dir": name,
        "ref": ref,
        "items": [],
    })
    save_data(items, filepath)


def main():
    items = load_data()

    while True:
        names = [playlist_data["name"] for playlist_data in items["playlists"]]
        names.extend(["+ Nowa", "Wyjście"])

        title = "                 ==== PLAYLIST + ===\nTen Program służy wyłącznie do aktualizacji playlist i\npobierania nowych. Odsłuchasz już w innym programie\n\nWybierz playlistę za pomocą strzałek i naciśnij Enter:"
        _, selected_index = pick(names, title, indicator=">")

        if selected_index == len(items["playlists"]):
            dodajPlayliste(items)
            continue

        if selected_index == len(items["playlists"]) + 1:
            return

        selected_playlist = items["playlists"][selected_index]
        print(f"Wybrano playlistę: {selected_playlist['name']}")
        changes = aktualizujPlayliste(selected_playlist, items)
        print("\nZmiany w playliście:")
        if not changes:
            print("Brak zmian.")
        for change in changes:
            item_name = change["item"].get("title") or change["item"]["id"]
            print(f"{change['change']}: {item_name}")
        input("Naciśnij ENTER aby powrócić...")


if __name__ == "__main__":
    main()