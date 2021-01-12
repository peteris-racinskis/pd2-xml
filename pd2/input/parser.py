import json

class Game:
    __tablename__ = "games"
    venue = Column('venue', String, primary_key=True)
    date = Column('date', String, primary_key=True)
    winner = Column('win', String, ForeignKey("team.name"))
    loser = Column('lose', String, ForeignKey("team.name"))
    ot = Column('ot', Boolean)
    __table_args__ = (UniqueConstraint(venue,date),)

class Team:
    __tablename__ = "teams"
    name = Column('name', String, primary_key=True)
    players = relationship("Player", backref="teamname", lazy=True)

class Player:
    __tablename__ = "players"
    num = Column('num', Integer, primary_key=True)
    firstname = Column('firstname', String)
    lastname =  Column('lastname', String)
    team = Column('team', String, ForeignKey("team.name"), primary_key=True)
    __table_args__ = (UniqueConstraint(num, team),)

class Referee:
    __tablename__ = "referees"
    firstname = Column('firstname', String, primary_key=True)
    lastname = Column('lastname', String, primary_key=True)

class Goal:
    __tablename__ = "goals"
    date = Column('date', String, ForeignKey('games.date'))
    venue = Column('venue', String, ForeignKey('games.venue'))
    t = Column('t', String, ForeignKey('players.team'))
    s = Column('s', String, ForeignKey('players.num'))
    p1 = Column('p1', String, ForeignKey('players.num'))
    p2 = Column('p2', String, ForeignKey('players.num'))
    time = 0

class Penalty:
    __tablename__ = "goals"
    date = Column('date', String, ForeignKey('games.date'))
    venue = Column('venue', String, ForeignKey('games.venue'))
    t = Column('t', String, ForeignKey('players.team'))
    ref = Column('ref', String, ForeignKey('players.num'))
    p1 = Column('p1', String, ForeignKey('players.num'))



class DocParser:
    
    MAGIC_CONSTANT = 40 # idk 

    def __init__(self):
        self.players = {}
        self.games = []
        self.goals = []
        self.penalties = []
        self.participants = []

    
    def read_documents(self, filenames):
        while len(filenames) > 0:
            print("Remaining filenames: {}".format(len(filenames)))
            self.data = []
            while len(filenames) > 0 and len(self.data) < self.MAGIC_CONSTANT:
                filename = filenames[0]
                with open(filename, 'rb') as f:
                    q = f.read()
                    self.data.append(json.loads(q.decode('latin-1')))
                filenames.pop(0)
            self.update()
        self.format_data()

    def update(self):
        e = get_existing_games()
        for d in self.data:
            self.parse_records(d ,e)
        self.parse_players()
        self.parse_games()
    
    def parse_records(self, game_info, existing):
        teams = dict()
        game = Game(
            venue = game_info["Spele"]["Vieta"],
            date =  game_info["Spele"]["Laiks"],
        )
        if (game.venue, game.data) in existing:
            return
        ref = get_referee(game_info)                    # Referee 
        endtime = 0
        for i in (0,1):
            team = game_info["Spele"]["Komanda"][i]         # json object (dict)
            goals = get_goals(team, game)                   # [Goal, ..   ]
            score = get_score(goals)                        # int
            players = get_players(team)                     # [Player, .. ]
            penalties = get_penalties(team)                 # [Penalty, ..]
            teams[score] = get_team(team)                   # { score:Team, }
            endtime = max(endtime, get_last_time(goals))    # int
        game.ot = (endtime > 60)                            # bool
        game.winner = teams[max(teams)].name
        game.loser = teams[min(teams)].name
        commit_to_database(game, teams, players, penalties, goals, referee) 

    def get_referee(self, game_info):
        ref = Referee(
            firstname = game_info["Spele"]["VT"]["Vards"],
            lastname = game_info["Spele"]["VT"]["Uzvards"]
        )
        return ref
    
    def get_goals(self, team, game):
        date = game.date
        venue = game.venue
        team = team["Nosaukums"]
        container = team["Varti"]
        if container == "":
            return None
        container = container["VG"]
        if type(container) == dict:
            container = [container]
        for entry in container:
            
            goal = Goal(
                date = date,
                venue = venue,
                t = team,

            )
        

    def format_data(self):
        self.formatted = {
            "players":      [(v["Nr"],v["team"],v["Loma"],v["Vards"],v["Uzvards"])
                for v in self.players.values()],
            "teams":        [],
            "games":        self.games,
            "goals":        [],
            "participants": [],
            "penalties":    [],
        }

    """
    Parsing: keep data flows separate, don't mix everything into one big function.
    Linear loss in efficiency but much easier to debug.
    """
    def parse_players(self):
        # The overly nested structure of this json annoys me
        TEAMS =     "['Spele']['Komanda']"
        ROSTER =    "['Speletaji']['Speletajs']"
        NAME =      "['Nosaukums']"
        for game in self.data:
            for team in eval("game"+TEAMS):
                name = eval("team"+NAME)
                new = {(name,item["Nr"]):item for item in eval("team"+ROSTER)}
                for key,item in new.items():
                    item["team"] = name
                self.players = { **self.players, **new }
    


    def parse_single_game(self, game):
        teams = self.get_teams(game)
        for team in teams:
            self.players.append(self.get_players(team))
            participants = self.get_participants(team)
            self.goals.append(self.get_goals(team, teams[(teams.index(team) + 1) % 2]))
            self.participants.append(self.get_participants(team))
            self.penalties.append(self.get_penalties(team))
        winner, loser = self.get_winner(teams)
        ot = self.check_overtime(teams)
        self.teams = self.teams + teams
        
        self.games.append(
            self.get_time(game),
            self.get_venue(game),
            winner,
            loser,
            ot)

    def get_teams(self, game):
        return game['Spele']['Komanda']
            
    
    def get_players(self, team):
        roster = team['Speletaji']['Speletajs']
        name = team['Nosaukums']
        return [(x["Nr"],name,x["Loma"],x["Vards"],x["Uzvards"]) for x in roster]
    
    def get_goals(self, team, opposed):
        t1 = team["Nosaukums"]
        t2 = opposed["Nosaukums"]
        ret = []
        if team["Varti"] == "":
            pass
        else:
            vg = team["Varti"]["VG"]
            ret = []
            for v in vg:
                scored = v["Nr"] 
                time = self.to_seconds(v["Laiks"])
                p1, p2 = self.get_passes(v)
                goalie = self.get_goalie(opposed, time)
                ret.append((scored, p1, p2, t1, t2, goalie, time))
        return ret
   
    def get_passes(self, v):
        ret = []
        try:
            P = v["P"]
            for p in P:
                ret.append(p)
            if len(ret) != 2:
                ret.append(-1)
        except Exception:
            ret = [-1,-1]
        return ret
    
    

    def to_seconds(self, s):
        s = s.split(":")
        return int(s[0])*60 + int(s[1])

    def get_team_score(self, team):
        if team["Varti"] == "":
            return 0
        else:
            return len(team["Varti"]["VG"]

    def get_teams(self, game):
        pass

    def get_goals(self, team):
        pass

    def get_game_score(self, goals):
        

    def parse_games(self):
        VENUE =             "['Spele']['Vieta']"
        DATE =              "['Spele']['Laiks']"
        TEAMS =             "['Spele']['Komanda']"
        GOALS =             "['Varti']['VG']"
        LAST_TIME = GOALS + "[:-1]['Laiks']"
        NAME =              "['Nosaukums']"
        for game in self.data:
            venue = eval("game"+VENUE)
            date = eval("game"+DATE)
            try:
                teams = {len(eval("team"+GOALS)):team for team in eval("game"+TEAMS)}
                winner = teams[max(teams)]
                loser = teams[min(teams)]
            except Exception as e:
                for team in eval("game"+TEAMS):

            #teams = {print(eval("team"+GOALS)) for team in eval("game"+TEAMS)}
            """teams = {len(eval("team"+GOALS)):team for team in eval("game"+TEAMS)}
            winner = teams[max(teams)]
            loser = teams[min(teams)]
            OT = (int(eval("winner"+LAST_TIME).split(":")[0]) > 90)
            winner = eval("winner"+NAME)
            loser = eval("loser"+NAME)
            self.games.append((date, venue, winner, loser, OT))
            """
    def check_score(self, team):
        print(team["Varti"])

    def parse_goals(self):
        pass

    def parse_penalties(self):
        pass

    def parse_participants(self):
        pass

