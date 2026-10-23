# Playlist +

Prosty program terminalowy do sprawdzania playlist YouTube i pobierania audio
z nowych pozycji. Po aktualizacji można wybrać kolejną playlistę albo zakończyć
program.

## Wymagania

- Python 3
- `make`
- pakiety Python: `pick` i `yt-dlp`

## Instalacja

Z głównego katalogu projektu zainstaluj zależności:

```bash
python3 -m pip install pick yt-dlp
```

Utwórz katalog na dane i zainicjuj pustą listę playlist:

```bash
mkdir -p data
make deleteall
```

## Uruchamianie

```bash
make start
```

Można też uruchomić program bezpośrednio:

```bash
python3 main.py
```

## Korzystanie

W menu poruszaj się strzałkami i zatwierdzaj wybór klawiszem Enter.

- Wybierz playlistę, aby sprawdzić jej aktualną zawartość.
- Jeśli pojawiły się nowe pozycje, program pobierze z nich audio. Utwory
  zachowane na playliście nie są pobierane ponownie.
- Jeśli playlisty nie zmieniły się, program nie pobiera plików ani nie zapisuje
  zmian.
- `+ Nowa` dodaje playlistę. Podaj jej nazwę i link lub identyfikator playlisty
  YouTube.
- `Wyjście` kończy program.

Program zapisuje pliki w katalogu wskazanym przez `savedir` w konfiguracji,
w podkatalogu o nazwie playlisty. Domyślnie jest to `static/<nazwa-playlisty>/`.
Format pliku zależy od audio udostępnionego przez YouTube.

Playlisty muszą być dostępne dla `yt-dlp` (na przykład publiczne lub
niepubliczne z dostępnym linkiem).

## Dane i konfiguracja

Plik `data/list.json` przechowuje konfigurację i stan playlist. Minimalna
początkowa zawartość:

```json
{
  "playlists": [],
  "savedir": "static"
}
```

Każda playlista jest zapisywana jako obiekt z polami:

- `name` — nazwa wyświetlana w menu,
- `dir` — nazwa podkatalogu na pobrane pliki,
- `ref` — link lub identyfikator playlisty YouTube,
- `items` — aktualnie zapisane pozycje playlisty.

`make deleteall` tworzy powyższą pustą konfigurację, nadpisując
`data/list.json`. Użyj go tylko wtedy, gdy chcesz wyczyścić zapisane playlisty.
