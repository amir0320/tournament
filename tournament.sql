-- Table definitions for the tournament project.
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- In case we've already created the tables and the database:
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS "Players", "Matches";

-- Create the database tournament
CREATE DATABASE tournament;

-- Connect to the database we just built
\c tournament;

-- Create the players table to store the player information
-- Example: [id] [player_name] [score_of_the_player]
CREATE TABLE Players (
	id serial PRIMARY KEY,
	name text,
	wins integer DEFAULT 0,
	matches integer DEFAULT 0
);

-- Create the matches table to store the matches record
-- Example: [match_id] [winner_id] [loser_id]
CREATE TABLE Matches (
	id serial PRIMARY KEY,
	winner serial REFERENCES Players (id),
	loser serial REFERENCES Players (id)
);

CREATE VIEW Standings AS
	SELECT * FROM Players
	ORDER BY wins DESC;
