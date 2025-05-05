## README

# SQL Assistant z LLM

Prosty asystent konsolowy, który generuje i wykonuje zapytania SQL na bazie MySQL na podstawie poleceń w języku naturalnym, wykorzystując lokalny model LLM (np. Ollama).

---

**Funkcje:**

- Automatyczne generowanie zapytań SQL na podstawie poleceń użytkownika.
- Obsługa dowolnego schematu bazy MySQL (schemat pobierany automatycznie).
- Wykonywanie zapytań i prezentacja wyników w konsoli.
- Integracja z lokalnym modelem LLM przez API (np. Ollama).

---

## Wymagania

- Python 3.8+
- MySQL
- Zainstalowane biblioteki:
    - `sqlalchemy`
    - `pymysql`
    - `requests`
- Lokalnie uruchomiony serwer Ollama lub inny zgodny endpoint LLM.

---

## Konfiguracja

1. Skonfiguruj plik `config.py` z danymi do bazy oraz adresem API LLM, np.:
```python
MYSQL_CONFIG = {
    'username': 'user',
    'password': 'haslo',
    'host': 'localhost',
    'port': 3306,
    'database': 'moja_baza',
    'ssl_ca': '/ścieżka/do/cacert.pem'
}

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "nazwa-modelu"
```

2. Upewnij się, że baza danych jest dostępna i użytkownik ma uprawnienia.

---

## Uruchomienie

```bash
python app.py
```

Aplikacja wyświetli schemat bazy i poprosi o polecenie.
Aby zakończyć, wpisz `exit`.

---

## Przykład użycia

```
Podaj polecenie: Wyświetl wszystkich użytkowników z tabeli users.

Wynik wykonania:
{'id': 1, 'name': 'Jan', 'email': 'jan@example.com'}
{'id': 2, 'name': 'Anna', 'email': 'anna@example.com'}
```


---

## Struktura projektu

- `app.py` – główny plik uruchamiający aplikację.
- `database.py` – obsługa połączenia i zapytań SQL.
- `llm_integration.py` – generowanie zapytań SQL przez LLM.
- `config.py` – konfiguracja połączeń.

---

## Uwagi

- Model LLM generuje wyłącznie zapytania SQL, nie wyjaśnia ich działania.
- Jeśli polecenie nie dotyczy SQL, model zwraca komunikat:
_"Skąd mam to niby wiedziec?"_
- Obsługiwane są tylko polecenia zgodne z MySQL.

---

