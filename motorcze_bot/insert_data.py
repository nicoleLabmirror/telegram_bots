import sqlite3
from sqlite3 import Error

INSERT_PERSON = """
    INSERT INTO person(name) VALUES(?)
"""

INSERT_ROUTE = """
    INSERT INTO route(date, distance ,person_id) VALUES(?,?,?)
"""

SELECT_PERSON = """
    SELECT * FROM person WHERE id=?
"""


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_data(conn, sql, data):
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

    return cur.lastrowid


def read_data(conn, sql, data):
    cur = conn.cursor()
    cur.execute(sql, data)
    result = cur.fetchall()

    return result


def main():
    database = "motorcze_test.db"

    conn = create_connection(database)
    with conn:
        person = read_data(conn, SELECT_PERSON, "1")
        person_id = person[0][0]

        route_1 = ("Testfahrt", 31, person_id)
        route_2 = ("Ausfahrt", 40, person_id)

        create_data(conn, INSERT_ROUTE, route_1)
        create_data(conn, INSERT_ROUTE, route_2)


if __name__ == "__main__":
    main()
