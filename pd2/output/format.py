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
    2:  Pack returned data in a list of lists;
    3:  Apply any required mutations on data;
    4:  Apply any required mutations on format string;
    5:  Output to stdout.
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
    
    """
    Just combines the results of a large number of separate queries.
    Not very performant, but it works.
    """
    def top(self):
        teams = []
        for d in self.data:
            teams = teams + d
        tw = {x:self.data[0].count(x) for x in teams}                    # Total wins
        ow = {x:self.data[1].count(x) for x in teams}                    # Overtime wins
        ol = {x:self.data[2].count(x) for x in teams}                    # Overtime losses
        tl = {x:self.data[3].count(x) for x in teams}                    # Total losses
        gt = {x:self.data[4].count(x) for x in teams}                    # Goals taken
        gl = {x:self.data[5].count(x) for x in teams}                    # Goals lost
        sc = {x:(5*tw[x] + 3*ow[x] + 2*ol[x] + tl[x]) for x in teams}    # Score
        ret = [(k[0],tw[k],ow[k],ol[k],tl[k],gt[k],gl[k],sc[k]) for k in tw]
        ret.sort(key= lambda x: (-x[-1]))
        self.data = ret
        self.format_string = "Score: {7:}\t{0:<15}|\tWins (NOT/OT): {1}:{2}\t|\tLosses (NOT/OT): {3}:{4}\t|\tGoals (gain/lose): {5}:{6}"
    
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
        self.format_string ="Penalties: {} Games: {} Average: {} - {}:{}"
    
