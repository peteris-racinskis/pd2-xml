

class Packager:
    
    insert = "INSERT or IGNORE into {} VALUES {}"
    INSERTS = {
                "players"   :   "(?, ?, ?, ?, ?)",
                "teams"     :   "(?)",
                "games"     :   "(?, ?, ?, ?, ?)",
                "goals"     :   "(?, ?, ?, ?, ?, ?, ?)",
                "participants": "(?, ?, ?)",
                "penalties" :   "(?, ?, ?)",
    }        


    def __init__(self, args, parser, db_handler):
        self.db_handler = db_handler
        self.parser = parser
        self.args = args

    def run(self):
        self.parser.read_documents(self.args)
        for k,v in self.parser.formatted:
            self.db_handler.write_data(
                    self.insert.format(k,self.INSERTS[k]),v)
