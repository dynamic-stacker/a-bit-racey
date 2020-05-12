import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute("""CREATE TABLE player_id
             (id integer, playername text, coins integer, gems integer, highscore integer)""")

c.execute("""CREATE TABLE vehicle_id
             (id integer, vehiclename text)""")


##first_3_attempts = [('1', 'James', '42', '2', '35'),
##                    ('2', 'Edwards', '34', '6', '23'),
##                    ('3', 'Jayden', '88', '4', '78')
##                    ]
##
##c.executemany('INSERT INTO player_id VALUES (?,?,?,?,?)', first_3_attempts)
##
def deleteRecord():
    try:
        # Deleting single record now
        sql_delete_person = """DELETE FROM player_id WHERE id = 1"""
        c.execute(sql_delete_person)
        conn.commit()
        print("Player record deleted successfully ")
        c.close()

    except sqlite3.Error as error:
        print("Failed to delete player record from sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")

deleteRecord()


