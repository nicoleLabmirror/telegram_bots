import sqlite3
from sqlite3 import Error

INSERT_PERSON = """
    INSERT INTO person(name, chat_id) VALUES(?,?)
"""

INSERT_ROUTE = """
    INSERT INTO route(date, distance ,person_id) VALUES(?,?,?)
"""

SELECT_PERSON = """
    SELECT id FROM person WHERE chat_id=?
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
    result = cur

    return result


db_file = "motorcze_test.db"


def main():
    database = "motorcze_test.db"

    conn = create_connection(database)
    with conn:
        person = read_data(conn, SELECT_PERSON, (326247323,))
        print(person)
        # person_id = person[0][0]

        # route_1 = ("Testfahrt", 31, person_id)
        route_2 = ("Ausfahrt", 40, person_id)

        # person_1 = ("Klaus", 326247323)
        # create_data(conn, INSERT_PERSON, person_1)
        # create_data(conn, INSERT_ROUTE, route_1)
        # create_data(conn, INSERT_ROUTE, route_2)


if __name__ == "__main__":
    main()
