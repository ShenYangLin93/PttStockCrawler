import os
from sqlalchemy import create_engine, engine
from sqlalchemy.exc import ProgrammingError

db_user = os.getenv('DB_USER')
db_pswd = os.getenv('DB_PSWD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

db_address = f"mysql+pymysql://{db_user}:{db_pswd}@{db_host}:{db_port}/"
schema_address = f"mysql+pymysql://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}"

create_table_cmd = '''
    CREATE TABLE post (
        url VARCHAR(50) PRIMARY KEY,
        author VARCHAR(50),
        pushes LONGTEXT,
        status INT
    )
'''


def create_db_if_not_exists():
    engine = create_engine(db_address)
    try:
        # Try to create the database
        engine.execute(f"CREATE DATABASE {db_name}")
        print("Database created successfully.")
    except ProgrammingError as e:
        if "1007" in str(e):
            print(f"Database '{db_name}' already exists. Skipping creation.")
        else:
            # Handle other potential errors
            print(f"Error creating database: {e}")


def create_table_if_not_exist():
        engine = create_engine(schema_address)
        result = engine.execute(f"SHOW TABLES LIKE 'post'")
        if not result.rowcount > 0:
            engine.execute(create_table_cmd)
            print('Table created successfully.')
        else:
            print('Table already exists.')

def get_mysql_connect() -> engine.base.Connection:
    engine = create_engine(schema_address)
    connect = engine.connect()
    return connect


    
