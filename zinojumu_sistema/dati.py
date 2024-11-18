import sqlite3

def izveidot_savienojumu():
    savienojums = sqlite3.connect('zinojumi.db')
    savienojums.row_factory = sqlite3.Row
    return savienojums

def izveidot_tabulas():
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS lietotaji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vards TEXT NOT NULL
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS kategorijas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nosaukums TEXT NOT NULL
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS zinojumi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            virsraksts TEXT NOT NULL,
            teksts TEXT NOT NULL,
            autors_id INTEGER,
            kategorija_id INTEGER,
            datums TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (autors_id) REFERENCES lietotaji (id),
            FOREIGN KEY (kategorija_id) REFERENCES kategorijas (id)
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS komentari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teksts TEXT NOT NULL,
            autors_id INTEGER,
            zinojums_id INTEGER,
            datums TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (autors_id) REFERENCES lietotaji (id),
            FOREIGN KEY (zinojums_id) REFERENCES zinojumi (id)
        )
    ''')
    
    savienojums.commit()
    savienojums.close()

def iegut_zinojumus(id=None, kategorija_id=None):
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    if id:
        cur.execute('''
            SELECT z.*, l.vards, k.nosaukums
            FROM zinojumi z
            JOIN lietotaji l ON z.autors_id = l.id
            JOIN kategorijas k ON z.kategorija_id = k.id
            WHERE z.id = ?
        ''', (id,))
        return cur.fetchone()
    
    if kategorija_id:
        cur.execute('''
            SELECT z.*, l.vards, k.nosaukums
            FROM zinojumi z
            JOIN lietotaji l ON z.autors_id = l.id
            JOIN kategorijas k ON z.kategorija_id = k.id
            WHERE z.kategorija_id = ?
        ''', (kategorija_id,))
    else:
        cur.execute('''
            SELECT z.*, l.vards, k.nosaukums
            FROM zinojumi z
            JOIN lietotaji l ON z.autors_id = l.id
            JOIN kategorijas k ON z.kategorija_id = k.id
            ORDER BY z.datums DESC
        ''')
    
    rezultats = cur.fetchall()
    savienojums.close()
    return rezultats

def pievienot_zinojumu(virsraksts, teksts, autors, kategorija):
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('INSERT INTO zinojumi (virsraksts, teksts, autors_id, kategorija_id) VALUES (?, ?, ?, ?)',
                  (virsraksts, teksts, autors, kategorija))
    
    savienojums.commit()
    savienojums.close()

def dzest_zinojumu(id):
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('DELETE FROM komentari WHERE zinojums_id = ?', (id,))
    cur.execute('DELETE FROM zinojumi WHERE id = ?', (id,))
    
    savienojums.commit()
    savienojums.close()

def iegut_kategorijas():
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('SELECT * FROM kategorijas')
    rezultats = cur.fetchall()
    
    savienojums.close()
    return rezultats

def pievienot_kategoriju(nosaukums):
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('INSERT INTO kategorijas (nosaukums) VALUES (?)', (nosaukums,))
    
    savienojums.commit()
    savienojums.close()

def iegut_lietotajus():
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('SELECT * FROM lietotaji')
    rezultats = cur.fetchall()
    
    savienojums.close()
    return rezultats

def pievienot_lietotaju(vards):
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('INSERT INTO lietotaji (vards) VALUES (?)', (vards,))
    
    savienojums.commit()
    savienojums.close()

def iegut_komentarus(zinojuma_id):
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('''
        SELECT k.*, l.vards
        FROM komentari k
        JOIN lietotaji l ON k.autors_id = l.id
        WHERE k.zinojums_id = ?
        ORDER BY k.datums DESC
    ''', (zinojuma_id,))
    
    rezultats = cur.fetchall()
    savienojums.close()
    return rezultats

def pievienot_komentaru(teksts, autors_id, zinojums_id):
    savienojums = izveidot_savienojumu()
    cur = savienojums.cursor()
    
    cur.execute('INSERT INTO komentari (teksts, autors_id, zinojums_id) VALUES (?, ?, ?)',
                  (teksts, autors_id, zinojums_id))
    
    savienojums.commit()
    savienojums.close()

# Izveido tabulas, kad fails tiek importēts
izveidot_tabulas()