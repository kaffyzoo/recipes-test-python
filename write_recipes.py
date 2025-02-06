from urllib.parse import urlparse
import psycopg2
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
result = urlparse(os.getenv('POSTGRES_ACCESS'))

username = result.username
password = result.password
database = result.path[1:]
port = result.port
hostname = result.hostname

class RecipePG():
    def __init__(self, database=database, username=username, password=password, host=hostname, port=port):
        self.connection = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port,
        )
        self.cursor = self.connection.cursor()

    def teardown(self):
        self.connection.close()
        self.cursor.close()

    def read_tables(self):
        # cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
        self.cursor.execute("select * from recipe")
        print(self.cursor.fetchall())

    def read_table_schema(self):
        self.cursor.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'recipe'")
        for column in self.cursor.fetchall():
            print(column)

    def create_table(self):
        try:
            self.cursor.execute("CREATE TABLE author (id serial PRIMARY KEY, fullname varchar, bio varchar);")
            # self.cursor.execute("CREATE TABLE recipe (id serial PRIMARY KEY, time_created date, title varchar, content varchar);")
            self.connection.commit() # <--- makes sure the change is shown in the database
        except:
            print("I can't drop our test database!")

    def update_table(self):
        try:
            self.cursor.execute("ALTER TABLE recipe ADD author_id VARCHAR;")
            self.connection.commit() # <--- makes sure the change is shown in the database
        except:
            print("I can't drop our test database!")

    def write_rows(self):
        self.cursor.execute("""
            INSERT INTO author (id, fullname, bio)
            VALUES (%s, %s, %s);
        """, (
            123,
            "The New York Times",
            "Are you trying to hide a newspaper inside of your cooking app",
        ))
        self.connection.commit()

    def update_rows(self):
        self.cursor.execute("""
            UPDATE recipe
            SET author_id = %s
            WHERE id = 12345
        """, (
            123,
        ))
        self.connection.commit()

def main():
    pg_recipes = RecipePG(database=database, username=username, password=password, host=hostname, port=port)

    # pg_recipes.update_table()
    # pg_recipes.update_rows()
    pg_recipes.write_rows()

    pg_recipes.teardown()

main()
