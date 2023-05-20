import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "motorcze_test.db"

    sql_create_person_table = """
        CREATE TABLE IF NOT EXISTS person (
            id integer PRIMARY KEY,
            name text NOT NULL
        );
    """

    sql_create_route_table = """
        CREATE TABLE IF NOT EXISTS route (
            id integer PRIMARY KEY,
            date text NOT NULL,
            name text NOT NULL,
            distance float NOT NULL,
            person_id integer NOT NULL,
            FOREIGN KEY (person_id) REFERENCES person (id)
        );
    """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_person_table)
        create_table(conn, sql_create_route_table)
    else:
        print("Error! cannot create the database connection.")

    conn.close()


if __name__ == "__main__":
    main()
