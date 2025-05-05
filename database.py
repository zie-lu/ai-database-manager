import sqlalchemy
from sqlalchemy import MetaData, text
from config import MYSQL_CONFIG

def generate_db_schema(engine):
    """Automatycznie generuje opis schematu bazy danych"""
    metadata = MetaData()
    metadata.reflect(bind=engine)
    schema_description = []
    for table in metadata.sorted_tables:
        schema_description.append(f"-- Tabela {table.name}")
        columns = []
        fk_constraints = []
        
        # Definicje kolumn
        for column in table.columns:
            col_info = f"{column.name} {column.type}"
            if column.primary_key:
                col_info += " PRIMARY KEY"
            if getattr(column, "autoincrement", False):
                col_info += " AUTO_INCREMENT"
            if not column.nullable:
                col_info += " NOT NULL"
            if column.unique:
                col_info += " UNIQUE"
            columns.append(col_info)
        
        # Klucze obce z opcjami ON DELETE/UPDATE
        for constraint in table.foreign_key_constraints:
            parent_cols = [col.name for col in constraint.columns]
            ref_table = constraint.elements[0].column.table.name
            ref_cols = [fk.column.name for fk in constraint.elements]
            fk_sql = (
                f"FOREIGN KEY ({', '.join(parent_cols)}) "
                f"REFERENCES {ref_table}({', '.join(ref_cols)})"
            )
            if constraint.ondelete:
                fk_sql += f" ON DELETE {constraint.ondelete.upper()}"
            if constraint.onupdate:
                fk_sql += f" ON UPDATE {constraint.onupdate.upper()}"
            fk_constraints.append(fk_sql)
        
        # Łączenie kolumn i constraintów
        all_defs = columns + fk_constraints
        schema_description.append(
            f"CREATE TABLE {table.name} (\n  " + ",\n  ".join(all_defs) + "\n);\n"
        )
    
    return "\n".join(schema_description)



def init_db_connection():
    """Inicjalizuje połączenie z bazą MySQL"""
    try:
        ssl_args = {'ssl_ca': MYSQL_CONFIG['ssl_ca']}
        engine = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username=MYSQL_CONFIG['username'],
                password=MYSQL_CONFIG['password'],
                host=MYSQL_CONFIG['host'],
                port=MYSQL_CONFIG['port'],
                database=MYSQL_CONFIG['database']
            ),
            connect_args=ssl_args
        )
        conn = engine.connect()
        db_schema = generate_db_schema(engine)
        return conn, db_schema
    except Exception as e:
        raise RuntimeError(f"Błąd połączenia z bazą: {str(e)}")

def execute_sql_query(conn, sql_query: str):
    """Wykonuje zapytanie SQL i zwraca wyniki"""
    try:
        result = conn.execute(text(sql_query))

        if sql_query.strip().upper().startswith('SELECT'):
            return [dict(row) for row in result.mappings()]
        else:
            conn.commit()
            return f"Operacja wykonana pomyślnie. Liczba zmienionych wierszy: {result.rowcount}"

    except Exception as e:
        raise RuntimeError(f"Błąd wykonania zapytania: {str(e)}")
