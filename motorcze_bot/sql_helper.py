import sqlite3

INSERT_PERSON = """
    INSERT INTO person(name, chat_id) VALUES(?,?)
"""

INSERT_ROUTE = """
    INSERT INTO route(date, distance ,person_id) VALUES(?,?,?)
"""

SELECT_ROUTE = """
    SELECT * FROM route WHERE person_id
"""

SELECT_PERSON = """
    SELECT id FROM person WHERE chat_id=?
"""

DB_FILE = "motorcze_test.db"


def create_connection(db_file):
    conn = None
    conn = sqlite3.connect(db_file)

    return conn


def read_route_data_from_db(data):
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    cur.execute(SELECT_PERSON, (data,))
    result = cur.fetchall()

    return result


def write_route_data_to_db(data):
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    cur.execute(INSERT_ROUTE, (data,))
    conn.commit()

    return cur.lastrowid
