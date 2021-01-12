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
        [print(self.format_string.format(*x)) for x in self.data]
    

    def top(self):
        pass
    
    """
    Player:
    1. Grabs the set of goals and players associated with them (scorers);
    2. Counts the appearance of each unique player as the scorer;
    3. Counts the appearance of each unique player as a passer;
    4. Sorts by scores, passes in that order;
    5. Formats the container string and output data.
    """
    def player(self):
        self.data[1] = self.data[1] + self.data[2] + self.data[3]
        scores = {x:self.data[0].count(x) for x in self.data[0]}
        ret = [(k,v1,self.data[1].count(k)) for (k,v1) in scores.items()]
        ret.sort(key= lambda x: (-x[1], -x[2]))
        self.data = [(v1, v2, k[2], k[3], k[0], k[1]) 
            for (k,v1,v2) in ret[:(10 if (len(ret) > 10) else len(ret))]]
        self.format_string ="Score: {} Passes: {} - {}:{} \t- {} {}"

    """
    Basically same as above, only counts penalties instead (2 tables instead of 5)
    """
    def rough(self):
        penalties = {x:self.data[0].count(x) for x in self.data[0]}
        ret = [(k,v) for (k,v) in penalties.items()]
        ret.sort(key= lambda x: -x[1])
        self.data = [(v, k[2], k[3], k[0], k[1]) for (k,v) in ret]
        self.format_string ="Penalties: {} - {}:{} \t- {} {}"

    """
    Ditto, but for head referees instead of players this time.
    """
    def referee(self):
        penalties = {x:self.data[0].count(x) for x in self.data[0]}
        ret = [(k,v,self.data[1].count(k),float(v)/self.data[1].count(k)) 
            for (k,v) in penalties.items()]
        ret.sort(key= lambda x: -x[3])
        self.data = [(v1,v2,v3,k[0],k[1]) for (k,v1,v2,v3) in ret]
        self.format_string ="Penalties: {} Games: {} Average: {} - {}:{} "
    
