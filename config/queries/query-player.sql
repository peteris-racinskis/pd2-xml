SELECT firstname, lastname, num, players.team FROM players INNER JOIN goals ON players.num=goals.s  AND players.team=goals.team 
SELECT firstname, lastname, num, players.team FROM players INNER JOIN goals ON players.num=goals.p1 AND players.team=goals.team
SELECT firstname, lastname, num, players.team FROM players INNER JOIN goals ON players.num=goals.p2 AND players.team=goals.team
SELECT firstname, lastname, num, players.team FROM players INNER JOIN goals ON players.num=goals.p3 AND players.team=goals.team