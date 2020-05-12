import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

##c.execute("""CREATE TABLE stats
##             (name text, coins integer, gems integer, highscore integer)""")

##first_3_attempts = [('James', '42', '2', '35'),
##                    ('Edwards', '34', '6', '23'),
##                    ('Jayden', '88', '4', '78')
##                    ]
##
##c.executemany('INSERT INTO stats VALUES (?,?,?,?)', first_3_attempts)

def deleteRecord():
    try:
        # Deleting single record now
        sql_delete_person = """DELETE FROM stats WHERE name = 'Edwards'"""
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


