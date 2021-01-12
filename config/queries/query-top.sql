SELECT teams.team FROM teams INNER JOIN games ON teams.team=games.winner AND games.ot = false
SELECT teams.team FROM teams INNER JOIN games ON teams.team=games.winner AND games.ot = true
SELECT teams.team FROM teams INNER JOIN games ON teams.team=games.loser AND games.ot = true
SELECT teams.team FROM teams INNER JOIN games ON teams.team=games.loser AND games.ot = false
SELECT teams.team FROM teams INNER JOIN goals ON teams.team=goals.team
SELECT teams.team FROM teams INNER JOIN goals ON teams.team=goals.other