"""
Relies on imports from xml.dom.minidom
"""

class Game:

    def __init__(self, dom_instance, populate=False):
        self.date = dom_instance.getAttribute('Laiks')
        self.venue = dom_instance.getAttribute('Vieta')
        self.ot = self.winner = self.loser = None
        if (populate):
            self.populate(dom_instance)

    def dump_id(self):
        return self.date, self.venue
    
    def data(self):
        return (self.date, self.venue, self.ot, self.winner, self.loser)

    def __repr__(self):
        return f"Game({self.data()})"

    def populate(self, game):
        self.get_ot(game)
        self.get_result(game)
    
    def get_ot(self, game):
        goals = game.getElementsByTagName('VG')
        last = 0
        for g in goals:
            last = max(int(g.getAttribute('Laiks').split(":")[0]), last)
        self.ot = (last > 60)
    
    def get_result(self, game):
        teams = game.getElementsByTagName('Komanda')
        scores = []
        for team in teams:
            scores.append(len(team.getElementsByTagName('VG')))
        self.winner = Team(teams[scores.index(max(scores))]).dump_id()
        self.loser = Team(teams[scores.index(min(scores))]).dump_id()
        

class Team:

    def __init__(self, dom_instance):
        self.name = dom_instance.getAttribute('Nosaukums')

    def dump_id(self):
        return self.name

    def data(self):
        return (self.name)

    def __repr__(self):
        return f"Team{self.data}"

class Player:

    def __init__(self, team, dom_instance):
        self.num = int(dom_instance.getAttribute('Nr'))
        self.team = Team(team).dump_id()
        self.firstname = dom_instance.getAttribute('Vards')
        self.lastname = dom_instance.getAttribute('Uzvards')
        self.role = dom_instance.getAttribute('Loma')
    
    def data(self):
        return (self.team, self.num, self.role, self.firstname, self.lastname)

    def __repr__(self):
        return f"Player{self.data}"


class Referee:

    def __init__(self, game):
        dom_instance = game.getElementsByTagName('VT')[0]
        self.firstname = dom_instance.getAttribute('Vards')
        self.lastname = dom_instance.getAttribute('Uzvards')
    
    def dump_id(self):
        return self.firstname, self.lastname

    def data(self):
        return self.dump_id()
    
    def __repr__(self):
        return f"Referee{self.data}"

class Goal:

    def __init__(self, game, team, dom_instance):
        self.gameid = Game(game).dump_id()
        self.playerid = (Team(team).dump_id(), int(dom_instance.getAttribute('Nr')))
        self.time = dom_instance.getAttribute('Laiks')
        self.passes = self.get_passes(dom_instance.getElementsByTagName('P'))
        
    def data(self):
        return (self.gameid[0],
                self.gameid[1],
                self.playerid[0], 
                self.playerid[1],
                self.time,
                self.passes[0],
                self.passes[1],
                #self.passes[2],
        )

    def __repr__(self):
        return f"Goal{self.data}"
    
    def get_passes(self, dom_array):
        passes = [int(p.getAttribute('Nr')) for p in dom_array] + [-1 for i in range(3)]
        for p in dom_array:
            passes.pop()
        return passes


class Penalty:

    def __init__(self, game, team, dom_instance):
        self.gameid = Game(game).dump_id()
        self.playerid = self.get_playerid(team, dom_instance)
        self.ref = Referee(game).dump_id()

    def data(self):
        return (self.gameid[0],
                self.gameid[1],
                self.playerid[0], 
                self.playerid[1],
                self.ref[0],
                self.ref[1],
        )

    def __repr__(self):
        return f"Penalty{self.data}"
    
    def get_playerid(self, team, penalty):
        team = team.getAttribute('Nosaukums')
        num = int(penalty.getAttribute('Nr'))
        return team, num

