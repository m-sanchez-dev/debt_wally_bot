""" Module containing all interactions with the database """
import os
import psycopg2


class DatabaseConection:
    def __init__(self):
        # DATABASE_URL = os.environ.get("DATABASE_URL")

        DATABASE_URL = "postgres://xijijinmgktzxs:706e427bb61cdfdce54b50d0be8ea486dd2fa9b6b9769701477a8ad453cc6b8d@ec2-52-214-178-113.eu-west-1.compute.amazonaws.com:5432/dbf5om2l8ub0se"

        self.con = psycopg2.connect(DATABASE_URL)

        self.cursor = self.con.cursor()

    def check_db_tables(self):
        self.cursor.execute(
            """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
        )

    def get_from_db(self) -> None:

        select_query = "SELECT * FROM cuentas;"
        self.run_query(select_query)

    def save_to_db(self, persona, asunto, gasto, es_parcial, parcial, total) -> None:

        insert_query = f"INSERT INTO cuentas (persona, asunto, gasto, es_parcial, parcial, total) VALUES('{persona}', '{asunto}', '{gasto}', '{es_parcial}','{parcial}','{total}');"
        self.run_query(insert_query)

    def run_query(self, query):
        self.cursor.execute(query)

    def get_last_record(self):

        insert_query = "SELECT * FROM cuentas ORDER BY compra_id DESC LIMIT 1;"
        self.run_query(insert_query)

    def show_results(self):
        for results in self.cursor.fetchall():
            print(results)

    def get_result(self, only_one=True):
        if only_one:
            return self.cursor.fetchall()[0]

        return self.cursor.fetchall()

    def close_connection(self):
        self.con.commit()
        self.cursor.close()
