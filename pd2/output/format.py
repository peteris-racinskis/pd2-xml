class Formatter:
    
    QUERIES = {
        "debug":    ["SELECT * FROM players WHERE team = 'Barcelona'"],
        "top":      [],
        "player":   [],
        "rough":    [],
        "pass":     [],
    }

    def __init__(self, command, config, db_handler):
        self.command = command
        self.db_handler = db_handler
    
    """
    Run:
    1:  Do query lookup, execute DB read operation;
    2:  Apply any required mutations on data;
    3:  Apply any required mutations on format string;
    4:  Output to stdout.
    """
    def run(self):
        self.format_string = "{}"
        self.data = [self.db_handler.read_data(query)
                for query in self.QUERIES[self.command]]        
        if self.command == "top":
            self.top()
        elif self.command == "player":
            self.player()
        elif self.command == "rough":
            self.rough()
        elif self.command == "team":
            self.team()
        [print(self.format_string.format(x)) for x in self.data]
    

    def top(self):
        pass

    def player(self):
        pass

    def rough(self):
        pass

    def team(self):
        pass
