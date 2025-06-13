# Poké Booster Bot

<img src="graphic/logo.png" alt="Logo" width="200"/>


Polski bot Discord do kolekcjonowania kart Pokémon i otwierania wirtualnych boosterów.
Korzysta z [Pokemon TCG API](https://pokemontcg.io/) i pozwala zbierać karty,
wykonywać codzienne zadania oraz handlować przedmiotami w wbudowanym sklepie.

Projekt obecnie rozbudowuje się o pełny stack aplikacji sieciowej. Bot na Discordzie
pozostaje miejscem, w którym zdobywa się monety i wykonuje szybkie akcje,
natomiast kupowanie i otwieranie boosterów przenosimy na stronę WWW.

Backend powstaje w **FastAPI** z bazą **PostgreSQL**, a frontend w **Next.js**.
Logowanie w serwisie działa w oparciu o OAuth2 Discord. Dodatkowo planowana
jest integracja z YouTube API, dzięki czemu będzie można zbierać monety za
oglądanie streamów.


## Funkcje

- **Kolekcja kart** – kupuj i otwieraj boostery z prawdziwych setów Pokémon.
- **System ekonomii** – zdobywaj monety przez codzienne nagrody i osiągnięcia,
  a następnie wydawaj je w sklepie.
- **Sklep** – przeglądaj dostępne boostery i przedmioty.
- **Otwieranie boosterów online** – odsłaniaj karty i zarządzaj kolekcją na stronie WWW.
- **Logowanie przez Discord** – strona korzysta z OAuth2, więc używasz tych samych danych co na serwerze.
- **Integracja z YouTube** – dodatkowe monety za oglądanie transmisji.
- **Osiągnięcia i ranking tygodniowy** – zdobywaj odznaki za master sety,
  30‑dniowy streak i najlepszy drop tygodnia.
- **Giveaway** – administratorzy mogą tworzyć losowania boosterów.
  Zwycięzcy otrzymują nagrody automatycznie i dostają powiadomienie w DM.
- **Eventy** – czasowe bonusy jak podwójne monety lub zwiększona szansa na drop.

## Instalacja

1. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
2. Utwórz plik `.env` i wpisz w nim wartości tokenu bota Discord oraz klucza
   API:
   ```ini
   BOT_TOKEN=twoj_token_bota
   POKETCG_API_KEY=twoj_klucz_api
   # Opcjonalnie ID emoji bc_coin na Twoim serwerze
   BC_COIN_ID=1381617796282319010
   ```
3. Uruchom bota:
   ```bash
   python3 src/bot.py
   ```
4. Backend FastAPI i frontend wymagają własnego środowiska. W katalogach
   `backend/` i `frontend/` znajdują się przykładowe konfiguracje projektu
   (uwaga: repozytorium obecnie zawiera tylko kod bota).

## Podstawowe komendy

- `/start` – załóż konto i odbierz startową pulę monet.
- `/saldo` – sprawdź aktualną ilość posiadanych monet.
- `/daily` – codzienna nagroda pieniędzy (24 h cooldown). Co 7 dni serii otrzymasz bonus 200 BC.
- `/sklep` – otwiera widok sklepu z boosterami i przedmiotami.
- `/profil` – wyświetla Twój profil z kartami i boosterami.
- `/profil_gracza` – pokaż uproszczony profil wskazanego gracza.
- `/osiagniecia` – lista zdobytych osiągnięć.
- `/ranking` – najlepsze dropy tygodnia.
- `/help` – lista wszystkich komend bota.
- `/otworz` – komenda dostępna w dotychczasowej wersji bota. Po migracji
  otwieranie boosterów odbywa się już na stronie WWW.
- `/giveaway` – stwórz losowanie boosterów (administrator).
- `/nagroda` – przyznaj booster lub monety wybranemu graczowi (administrator).

Poniżej przykład grafiki jednego z setów dostępnych w sklepie:

![Set logo](https://images.pokemontcg.io/sv10/logo.png)

Miniaturki boosterów są dostępne pod adresem `https://images.pokemontcg.io/<ID>/booster.png`,
gdzie `<ID>` to identyfikator zestawu zapisany w `sets.json`. Bot korzysta z tych
adresów, aby pokazywać obrazki boosterów w sklepie.

## Pliki danych

- `data/users.json` – lokalna baza kont użytkowników i ich kolekcji.
- `data/sets.json` – lista setów pobierana z API; aktualizuje się automatycznie.
- `data/price.json` – zapisane ceny boosterów w monetach.
- `data/data.json` – statystyki zakupów i inne dane pomocnicze.
- `data/channels.json` – przypisanie ID kanałów do funkcji bota (np. dropy, sklep, giveaway).

W kolejnych wersjach część danych z tych plików zostanie przeniesiona do
bazy **PostgreSQL**, którą obsługuje aplikacja FastAPI.

Przed pierwszym uruchomieniem bota pliki te mogą być puste. Bot sam pobierze
niezbędne dane.

## Licencja

Projekt ma charakter demonstracyjny i wymaga własnego tokenu Discord oraz
klucza do Pokemon TCG API. Wykorzystuj na własną odpowiedzialność.


## Backend i frontend

W katalogu `backend/` znajduje się przykładowa aplikacja FastAPI z modelami
SQLAlchemy oraz skryptem `load_data.py` do migracji plików JSON do bazy
PostgreSQL. Frontend w `frontend/` zawiera proste szablony HTML oraz arkusz
stylów. Strony korzystają z API udostępnionego przez backend i umożliwiają
podstawowe akcje jak podgląd profilu, sklep, ranking czy aktualne giveawaye.
