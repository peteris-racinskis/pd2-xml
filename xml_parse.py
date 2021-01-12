from xml.dom.minidom import parse


class Game:

    def __init__(self, dom_instance, populate=False):
        self.date = dom_instance.getAttribute('Laiks')
        self.venue = dom_instance.getAttribute('Vieta')
        self.ot = self.winner = self.loser = None
        if (populate):
            self.populate(dom_instance)

    def dump_id(self):
        return self.date, self.venue

    def __repr__(self):
        return f"Game({(self.date, self.venue)}, '{self.ot}', ({self.winner} - {self.loser})"

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

    def __repr__(self):
        return f"{self.name}"

class Player:

    def __init__(self, team, dom_instance):
        self.num = dom_instance.getAttribute('Nr')
        self.team = Team(team).dump_id()
        self.firstname = dom_instance.getAttribute('Vards')
        self.lastname = dom_instance.getAttribute('Uzvards')
        self.role = dom_instance.getAttribute('Loma')
    
    def __repr__(self):
        return f"Player('{self.team}:{self.num}', '{self.firstname} {self.lastname}', '{self.role}')"


class Referee:

    def __init__(self, dom_instance):
        self.firstname = dom_instance.getAttribute('Vards')
        self.lastname = dom_instance.getAttribute('Uzvards')
    
    def dump_id(self):
        return self.firstname, self.lastname

    def __repr__(self):
        return f"{self.firstname} {self.lastname}"

class Goal:

    def __init__(self, game, team, dom_instance):
        self.gameid = self.get_gameid(game)
        self.team = Team(team).name
        self.time = dom_instance.getAttribute('Laiks')
        self.player = dom_instance.getAttribute('Nr')
        self.passes = self.get_passes(dom_instance.getElementsByTagName('P'))
    
    def get_gameid(self, game):
        return game.getAttribute('Laiks'), game.getAttribute('Vieta')

    def get_passes(self, pass_object):
        ret = []
        for p in pass_object:
            ret.append(p.getAttribute('Nr'))
        return ret
    
    def __repr__(self):
        return f"Goal({self.gameid}, {self.time}', '{self.team}:{self.player}', {self.passes})"

class Penalty:

    def __init__(self, game, team, dom_instance):
        self.gameid = self.get_gameid(game)
        self.player = self.get_playerid(team, dom_instance)
        self.ref = self.get_ref(game)

    def __repr__(self):
        return f"Penalty({self.player}, {self.gameid}, {self.ref})"
    
    def get_gameid(self, game):
        return game.getAttribute('Laiks'), game.getAttribute('Vieta')
    
    def get_playerid(self, team, penalty):
        team = team.getAttribute('Nosaukums')
        num = penalty.getAttribute('Nr')
        return team, num
    
    def get_ref(self, game):
        vt_instance = game.getElementsByTagName('VT')[0]
        firstname = vt_instance.getAttribute('Vards')
        lastname = vt_instance.getAttribute('Uzvards')
        return firstname, lastname


def get_teams(data):
    return data.getElementsByTagName('Komanda')

def get_score(team):
    return len(team.getElementsByTagName('VG'))

def get_goals(game, team):
    goals = team.getElementsByTagName('VG')
    return [Goal(game, team, x) for x in goals]

def get_penalties(game, team):
    penalties = team.getElementsByTagName('Sods')
    return [Penalty(game, team, x) for x in penalties]

def get_players(game):
    ret = []
    for team in game.getElementsByTagName('Komanda'):
        ret = ret + [Player(team, x) 
            for x in team.getElementsByTagName('Speletaji')[0]
                        .getElementsByTagName('Speletajs')]
    return ret


game_info = parse("xml/0.xml")
game = game_info.getElementsByTagName('Spele')[0]
print(Game(game, populate=True))
teams = get_teams(game_info)
scores = [get_score(team) for team in teams]
goals = [get_goals(game, team) for team in teams]
penalties = [get_penalties(game, team) for team in teams]
players = get_players(game)
[print(x) for x in players]
print(scores)
for team in goals:
    [print(goal) for goal in team] 
for team in penalties:
    [print(x) for x in team]


