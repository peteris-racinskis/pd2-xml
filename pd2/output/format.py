class Formatter:
    Q_INDEX = {
        "debug":    [],
        "top":      [],
        "player":   [],
        "rough":    [],
        "referee":  [],
    }

    def __init__(self, command, config, db_handler):
        self.command = command
        self.db_handler = db_handler
        self.load_queries(config)
    
    def load_queries(self, config):
        queries = []
        for k in self.Q_INDEX.keys():
            with open(config["QUERY_PATH"].format(k), 'r') as f:
                for line in f.readlines():
                    self.Q_INDEX[k] = self.Q_INDEX[k] + [line]
        print(self.Q_INDEX)

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
                for query in self.Q_INDEX[self.command]]        
        if self.command == "top":
            self.top()
        elif self.command == "player":
            self.player()
        elif self.command == "rough":
            self.rough()
        elif self.command == "referee":
            self.referee()
        [print(self.format_string.format(x)) for x in self.data]
    

    def top(self):
        pass

    def player(self):
        pass

    def rough(self):
        pass

    def referee(self):
        pass
