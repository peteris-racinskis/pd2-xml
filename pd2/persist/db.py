import sqlite3

class DbHandler:

    def __init__(self, path, schema):
        try:
            self.conn = sqlite3.connect(path)
        except Exception as e:
            print("Database connection couldn't be established: {}".format(e))
            exit(1)
        self.create_tables(schema)

    def create_tables(self, schema):
        c = self.conn.cursor()
        for command in schema:
            c.execute(command)
        self.conn.commit()

    def write_data(self, query, data):
        c = self.conn.cursor()
        c.executemany(query, data)
        self.conn.commit()
        

    def read_data(self, query):
        c = self.conn.cursor()
        c.execute(query)
        return c.fetchall()

