import requests
import json
from config import OLLAMA_URL, MODEL

def get_sql_query(user_prompt: str, db_schema: str) -> str:
    """Generuje zapytanie SQL przy użyciu modelu LLM"""
    prompt = f"""
    Na podstawie poniższego schematu bazy danych wygeneruj tylko jedno, poprawne zapytanie mySQL odpowiadające poleceniu użytkownika.
    Zwróć wyłącznie zapytanie mySQL, bez żadnych wyjaśnień.
    **Zabronione jest używanie jakichkolwiek znaczników (```, `SQL` itp.)!**
    Jeśli polecenie nie dotyczy mySQL, odpowiedz: "Skąd mam to niby wiedziec?".

    Schemat bazy:
    {db_schema}

    Polecenie użytkownika:
    {user_prompt}
    """
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True
    }

    full_response = []
    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
            response.raise_for_status()

            print("Generuję odpowiedź...\n")
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    print(chunk['response'], end='', flush=True)
                    full_response.append(chunk['response'])

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Błąd połączenia: {str(e)}")

    return ''.join(full_response).strip()

# import requests
# import json
# from config import OLLAMA_URL, MODEL

# def get_sql_query(user_prompt: str, db_schema: str) -> str:
#     """Generuje zapytanie SQL przy użyciu modelu LLM"""
#     prompt = f"""
#     Na podstawie poniższego schematu bazy danych wygeneruj tylko jedno, poprawne zapytanie mySQL odpowiadające poleceniu użytkownika.
#     Zwróć wyłącznie zapytanie mySQL, bez żadnych wyjaśnień.
#     Jeśli polecenie nie dotyczy mySQL, odpowiedz: "Skąd mam to niby wiedziec?".

# Polecenie użytkownika:
# {user_prompt}
# """
#     payload = {
#         "model": MODEL,
#         "system": db_schema,
#         "prompt": prompt,
#         "stream": True
#     }

#     full_response = []
#     try:
#         with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
#             response.raise_for_status()

#             print("Generuję odpowiedź...\n")
#             for line in response.iter_lines():
#                 if line:
#                     chunk = json.loads(line.decode('utf-8'))
#                     print(chunk['response'], end='', flush=True)
#                     full_response.append(chunk['response'])

#     except requests.exceptions.RequestException as e:
#         raise RuntimeError(f"Błąd połączenia: {str(e)}")

#     return ''.join(full_response).strip()

