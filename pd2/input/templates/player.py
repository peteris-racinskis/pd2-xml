
class Player:
    """
        PLAYER - BEHAVIOUR:
        for player in game[..teams[...players]]]:
            player = Player[game] <- takes entire game json as input data
        needs to figure out the following:
        role | firstname | lastname | team | # scores | # passes | # losses (as goalie) | # penalties | t0 | t1

        This then gets sent to db:
        first pass - INSERT or IGNORE INTO ....
        second pass - UPDATE valiue ... WHERE ...
    """
    def __init__(self, data, player_data, team_index):
        num, firstname, lastname, role = self.parse_player(player_data)
        team = data["Spele"]["Komanda"][team_index]
        other_team = data["Spele"]["Komanda"][(team_index+1) % 2]
        team_name = self.get_team_name(team)
        t1, t2 = self.get_time(team, num)
        goal_container = team["Varti"]
        goals = self.get_goals(goal_container, num)
        if role == "V":
            lgoal_container = other_team["Varti"]
            lgoals = self.get_lgoals(lgoal_container, t1, t2)
        team_name = self.get_team_name(team)

        pass
    
    def match_in_dict_list(self, dict_list, pattern, num):
        for d in dict_list:
            if eval("d"+pattern) == num:
                return 1, d
        return 0, {}

    def get_time(self, team, num):
        roster = team["Pamatsastavs"]["Speletajs"]
        shifts = team["Mainas"]
        pattern = "['Maina']"
        n = "['Nr{}']"
        a, _ = self.match_in_dict_list(roster, "['Nr']", num)
        if a == 1:
            t1 = 0
        elif type(shifts) == dict:
            shifts = [shifts]
        n1, shift = self.match_in_dict_list(shifts, pattern + n.format(1), num)
        n2, shift = self.match_in_dict_list(shifts, pattern + n.format(2), num)
        if n1 == 1:
            t2 = 


    def parse_player(self, p):
        return p["Nr"], p["Vards"], p["Uzvards"], p["Loma"]

    def get_team_name(self, team):
        return team["Nosaukums"]
    
    def get_goals(self, goal_container, num):
        res = 0
        if type(goal_container) == dict:
            res, _ = self.match_in_dict_list([goal_container, "['Nr']", num)
        elif len(goal_container) > 1:
            for goal in goal_container:
                res = res + self.get_goals(goal)
        return res