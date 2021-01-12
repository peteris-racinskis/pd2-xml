class Team:
    """
        TEAM - BEHAVIOUR:
        for team in game[..teams]:
            team = Team(game) <- takes entire game json as input data!

        for our task, need to figure out:
        name | points | wins (no ot) | wins (ot) | losses (no ot) | losses (ot) | # goals | # goals lost |
        [txt]  [1..5]     [0..1]        [0..1]        [0..1]          [0..1]       [int]        [int]
        with this, the task requirements can be satisfied.

    """
    def __init__(self, data, index):
        name = self.get_name(data, index)
        ot, winner, goals, lgoals = self.result(data, index)
        wins_not =  int(winner and (not ot))
        wins_ot  =  int(winner and ot)
        loss_ot  =  int((not winner) and ot)
        loss_not =  int((not winner) and (not ot))
        points = 5 * wins_not + 3 * wins_ot + 2 * loss_ot + 1 * loss_not
        self.data = (name, points, wins_not, wins_ot, loss_ot, loss_not, goals, lgoals)

    def get_name(self, data, index):
        return data["Spele"]["Komanda"][index]["Nosaukums"]

    def result(self, data, index):
        scores = [self.get_score(x) for x in data["Spele"]["Komanda"]]
        this = scores[index][1]
        other = scores[(index + 1) % 2][1]
        winner = this > other
        ot = self.ot(scores[0][0]) or self.ot(scores[1][0])
        return ot, winner, this, other

    def get_score(self, team):
        if team["Varti"] == "":
            return 0, 0
        elif type(team["Varti"]["VG"]) == dict:
            return int(team["Varti"]["VG"]["Laiks"].split(":")[0]), 1
        else:
            vg = team["Varti"]["VG"]
            return int(vg[-1]["Laiks"].split(":")[0]), len(team["Varti"]["VG"])


    def ot(self, time):
        return time > 90

