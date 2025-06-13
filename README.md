# Bogucki Cards

Bogucki Cards to połączenie gry przeglądarkowej oraz bota Discord, w której zbierasz karty inspirowane Pokemon TCG. Projekt zawiera backend w FastAPI, prosty frontend HTML/JS oraz rozbudowanego bota korzystającego z biblioteki `discord.py`.

## Najważniejsze funkcje

- **Otwarte boostery** – kupuj i otwieraj paczki kart na stronie WWW.
- **Ekonomia** – zarabiaj BoguckiCoiny za codzienne zadania i wymieniaj je na nowe karty.
- **Osiągnięcia** – zbieraj odznaki za aktywność i kolekcjonowanie.
- **Giveawaye** – administratorzy mogą uruchamiać losowania boosterów z poziomu bota.
- **Integracja z YouTube** – opcjonalnie nagradza za oglądanie streamów twórcy.

## Wymagania i instalacja

1. Zainstaluj Python 3.11 lub nowszy.
2. Zainstaluj pakiety:
   ```bash
   pip install -r requirements.txt
   ```
3. Utwórz plik `.env` i ustaw wymagane zmienne:
   ```ini
   BOT_TOKEN=twoj_token_bota
   POKETCG_API_KEY=klucz_do_api
   DISCORD_CLIENT_ID=id_aplikacji
   DISCORD_CLIENT_SECRET=sekret_aplikacji
   DISCORD_REDIRECT_URI=http://localhost:8000/callback
   ```
4. (Opcjonalnie) skonfiguruj PostgreSQL i ustaw `DATABASE_URL` w `.env`.

## Uruchamianie

- **Bot Discord**
  ```bash
  python3 src/bot.py
  ```
- **Serwer FastAPI**
  ```bash
  uvicorn backend.main:app --reload
  ```
  Po uruchomieniu odwiedź [http://localhost:8000/](http://localhost:8000/) aby
  zobaczyć komunikat testowy `{"Hello": "CardCollectorGame Backend running!"}`.
- **Testy**
  ```bash
  pytest -v
  ```

## Jak stworzyć bota w Discord Developer Portal

1. Wejdź na <https://discord.com/developers/applications> i kliknij „New Application”.
2. W zakładce **Bot** dodaj bota i skopiuj jego token – trafi on do zmiennej `BOT_TOKEN`.
3. W zakładce **OAuth2** dodaj URL przekierowania (np. `http://localhost:8000/callback`).
4. Wygeneruj link z uprawnieniami bota i dodaj go na swój serwer Discord.

## Struktura projektu

- `src/` – kod bota i skrypty pomocnicze.
- `backend/` – aplikacja FastAPI z modelem baz danych.
- `frontend/` – statyczne szablony HTML/CSS/JS.
- `tests/` – podstawowe testy `pytest`.
- `data/` – lokalne pliki z danymi graczy i konfiguracją.

Projekt jest w fazie rozwojowej i ma służyć jako przykład integracji bota Discord z prostą grą sieciową. Korzystaj na własną odpowiedzialność i baw się dobrze!
