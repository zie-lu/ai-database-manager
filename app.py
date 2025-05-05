from database import init_db_connection, execute_sql_query
from llm_integration import get_sql_query

def main():
    db_connection, DB_SCHEMA = init_db_connection()
    if not db_connection or not DB_SCHEMA:
        return
    print(DB_SCHEMA)
    try:
        while True:
            user_input = input("\nPodaj polecenie: ")
            if user_input.strip().lower() == "exit":
                break

            generated_sql = get_sql_query(user_input, DB_SCHEMA)
            if not generated_sql or "Skąd mam" in generated_sql:
                continue

            result = execute_sql_query(db_connection, generated_sql)
            print("\nWynik wykonania:")
            if isinstance(result, list):
                if result:
                    for row in result:
                        print(row)
                else:
                    print("Brak wyników")
            else:
                print(result)
    finally:
        db_connection.close()
        print("\n\nPołączenie z bazą zostało zamknięte.")

if __name__ == "__main__":
    main()

