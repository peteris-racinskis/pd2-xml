#!/usr/bin/python3

def construct_tables(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS players " + 
    "(num integer, team text, role text, firstname text, lastname text)")
    conn.commit()

def init_db():
    import sqlite3
    try:
        conn = sqlite3.connect('storage/file.db')
        print("Database connection succesful")
        construct_tables(conn)
        conn.close()
    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    init_db()
