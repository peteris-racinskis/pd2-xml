from xml.dom.minidom import parse
from pd2.input.templates import Game, Team, Player, Referee, Goal, Penalty


class DocParser:
    
    def __init__(self, in_db):
        # Not optimal for very large datasets but this should easily fit in memory
        self.games = set()
        self.referees = set()
        self.teams = set()
        self.players = set()
        self.goals = set()
        self.penalties = set()

        
    def read_documents(self, filenames):
        for filename in filenames:
            print(filename)
            game_info = parse(filename)
            self.extract_info(game_info)

    def extract_info(self, game_info):
        game = game_info.getElementsByTagName('Spele')[0]
        if Game(game).data() in self.games:
            return
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
        self.games.add(Game(game, populate=True).data())
        self.referees.add(Referee(game).data())
        [self.teams.add(Team(team).data()) for team in teams]
        [self.players.add(x.data()) for x in players]
        [self.goals.add(x.data()) for x in goals]
        [self.penalties.add(x.data()) for x in penalties]

    