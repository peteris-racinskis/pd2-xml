CREATE TABLE IF NOT EXISTS players (team string, num integer, role string, firstname string, lastname string, unique(num, team))
CREATE TABLE IF NOT EXISTS teams (team string)
CREATE TABLE IF NOT EXISTS games (time string, venue string, ot boolean, winner string, loser string, ref_name string, ref_lname string, unique(time, venue))
CREATE TABLE IF NOT EXISTS goals (game_time string, venue string, team string, s integer, time string, p1 integer, p2 integer, p3 integer)
CREATE TABLE IF NOT EXISTS penalties (time string, venue string, team string, player integer, ref_name string, ref_lname string)
CREATE TABLE IF NOT EXISTS referees (firstname string, lastname string)
