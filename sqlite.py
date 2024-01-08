import sqlite3

# Établir une connexion à la base de données
conn = sqlite3.connect('visages_connus.db')
cursor = conn.cursor()

# Créer une table 'people' si elle n'existe pas déjà
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
        counter INTEGER PRIMARY KEY,
        id INTEGER ,
        timestamp TEXT,
        image BLOB
    )
''')



conn.commit()
conn.close()