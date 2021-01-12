CREATE TABLE IF NOT EXISTS players (num integer, team text, role text, firstname text, lastname text, unique(num, team))
CREATE TABLE IF NOT EXISTS teams (team text)
CREATE TABLE IF NOT EXISTS games (time text, venue text, winner text, loser text, ot bool, unique(time, venue))
CREATE TABLE IF NOT EXISTS goals (scored integer, p1 integer, p2 integer, t1 text, t2 text, goalie integer, time integer)
CREATE TABLE IF NOT EXISTS participants (num integer, team text, ot bool)
CREATE TABLE IF NOT EXISTS penalties (card text, num integer, team text)
