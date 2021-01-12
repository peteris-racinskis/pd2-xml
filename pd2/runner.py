import sqlite3
import json
from pd2.input.parser import DocParser
from pd2.input.packager import Packager
from pd2.persist.db import DbHandler
from pd2.output.format import Formatter


class Runner:

    def __init__(self, args):
        self.mode = ""
        self.parse_config(args)
        self.db_handler = DbHandler(self.config["DB_PATH"], self.schema)

    def run(self):
        if self.mode == "update":
            old = set(self.db_handler.read_data("SELECT * FROM games;"))
            parser = DocParser(old)
            packager = Packager(self.args, parser, self.db_handler)
            packager.run()
        elif self.mode == "display":
            formatter = Formatter(self.args[0], self.config, self.db_handler)
            formatter.run()
        else:
            self.usage()

    def parse_config(self, args):
        with open('config/config.json', 'rb') as f:
            q = f.read()
            self.config = json.loads(q.decode('latin-1'))
        with open(self.config["SCHEMA_PATH"],'r') as f:
            self.schema = [line for line in f.readlines()]
        if len(args) > 2:
            self.mode = args[1]
            self.args = args[2:]
    
    def usage(self):
        with open(self.config["USAGE_PATH"], 'r') as f:
            print()
            print(f.read())

