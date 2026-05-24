# SolidSmells — Asystent AI (SOLID & Code Smells)

Aplikacja webowa analizująca fragment kodu Pythona pod kątem naruszeń zasad **SOLID** i **Code Smells** z użyciem Gemini API.

## Stos technologiczny

- Python 3.11+
- Flask 3.x — serwer HTTP
- google-genai — klient Gemini
- python-dotenv — konfiguracja z `.env`
- unittest (stdlib) + coverage — testy i pokrycie kodu
- HTML / CSS / JavaScript (vanilla) — interfejs użytkownika

## Struktura projektu

```
SolidSmells/
├── src/          # kod produkcyjny
├── test/         # testy unittest
├── run.py        # uruchomienie aplikacji (docelowo)
└── requirements.txt
```

## Uruchomienie

> Szczegółowa instrukcja instalacji i uruchomienia zostanie uzupełniona w finalnym commicie dokumentacji.

1. Sklonuj repozytorium i utwórz venv.
2. `pip install -r requirements.txt`
3. Skopiuj `.env.example` → `.env` i uzupełnij `GEMINI_API_KEY`.
4. `python run.py` → http://localhost:5000

## Testy

```bash
python -m unittest discover -s test -v
coverage run -m unittest discover -s test
coverage report -m
```

## Cel projektu (kurs Testowanie oprogramowania)

- TDD z widocznymi commitami RED / GREEN / REFACTOR
- Pokrycie kodu testami ≥ 85%
- SOLID (m.in. DIP przez `LlmClient` Protocol)
- Atrapy (`unittest.mock.Mock`) zamiast prawdziwego API w testach jednostkowych
