import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute("""CREATE TABLE stats (name text, coins integer, gems integer, highscore integer)""")
