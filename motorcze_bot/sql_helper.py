import sqlite3


INSERT_ROUTE = """
    INSERT INTO route(date, name, distance ,person_id)
    VALUES(:date, :name, :distance, :person_id)
"""

SELECT_ROUTE = """
    SELECT route.date, route.name, route.distance
    FROM route
    JOIN person
    WHERE date LIKE :year
    AND person.chat_id = :person_id
"""

DB_FILE = "motorcze_test.db"


def create_connection(db_file):
    conn = None
    conn = sqlite3.connect(db_file)

    return conn


def read_route_data_from_db(data):
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    # TODO: this can't be right. It works but ...   
    data["year"] = str(data["year"]) + "-%"
    cur.execute(SELECT_ROUTE, data)
    result = cur.fetchall()

    return result


def write_route_data_to_db(data):
    conn = create_connection(DB_FILE)
    cur = conn.cursor()
    cur.execute(INSERT_ROUTE, data)
    conn.commit()

    return cur.lastrowid
