#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM Matches;")
    c.execute("UPDATE Players SET wins = 0, matches = 0;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM Players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(id) FROM Players;")
    total_players = c.fetchone()[0]
    db.close()
    
    return total_players

def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    clean_name = bleach.clean(name)
    c.execute("INSERT INTO Players (name) VALUES (%s);", (clean_name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM Standings;")
    standings = []
    for row in c:
	temp_row = [row[0], row[1], row[2], row[3]]
	standings.append(temp_row)
    db.commit()
    db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO Matches (winner, loser) VALUES (%s, %s);", (winner, loser,))
    c.execute("UPDATE Players SET wins = wins + 1, matches = matches + 1 WHERE id = (%s);", (winner,))
    c.execute("UPDATE Players SET matches = matches + 1 WHERE id = (%s);", (loser,))
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM Standings;")
    standings = c.fetchall()
    pairings = []
    row_index = 0
    while (row_index < countPlayers()):
	temp_row = [standings[row_index][0], standings[row_index][1], standings[row_index+1][0], standings[row_index+1][1]]
	pairings.append(temp_row)
	row_index += 2
    db.close()
    return pairings
