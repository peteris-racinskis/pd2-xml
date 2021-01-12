from xml.dom.minidom import parse
from pd2.input.templates import Game, Team, Player, Referee, Goal, Penalty


class DocParser:
    
    def __init__(self, in_db):
        # Not optimal for very large datasets but this should easily fit in memory
        self.data = {
            "games"       : in_db,
            "teams"       : set(),
            "players"     : set(),
            "goals"       : set(),
            "penalties"   : set(),
            "referees"    : set(),
        }


    def read_documents(self, filenames):
        for filename in filenames:
            print(filename)
            game_info = parse(filename)
            self.extract_info(game_info)

    def extract_info(self, game_info):
        game = game_info.getElementsByTagName('Spele')[0]
        if Game(game, populate=True).data() in self.data["games"]:
            print("skipping")
            return
        print("not skipping")
        teams = game.getElementsByTagName('Komanda')
        players = []
        goals = []
        penalties = []
        for team in teams:
            players = players + [Player(team, x) for x in 
                team.getElementsByTagName('Speletaji')[0]
                .getElementsByTagName('Speletajs')]
            goals = goals + [Goal(game, team, x) for x in 
                team.getElementsByTagName('VG')]
            penalties = penalties + [Penalty(game, team, x) for x in
                team.getElementsByTagName('Sods')]
        self.data["games"].add(Game(game, populate=True).data())
        self.data["referees"].add(Referee(game).data())
        [self.data["teams"].add(Team(team).data()) for team in teams]
        [self.data["players"].add(x.data()) for x in players]
        [self.data["goals"].add(x.data()) for x in goals]
        [self.data["penalties"].add(x.data()) for x in penalties]

    