from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def inicializet_db():
    savienojums = sqlite3.connect('zinojumi.db')
    c = savienojums.cursor()
    # Lietotāju tabula
    c.execute('''CREATE TABLE IF NOT EXISTS lietotaji
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  vards TEXT NOT NULL,
                  uzvards TEXT NOT NULL,
                  lietotajvards TEXT UNIQUE NOT NULL)''')
    
    # Ziņojumu tabula
    c.execute('''CREATE TABLE IF NOT EXISTS zinojumi
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  lietotaja_id INTEGER,
                  zinojums TEXT NOT NULL,
                  FOREIGN KEY (lietotaja_id) REFERENCES lietotaji (id))''')
    savienojums.commit()
    savienojums.close()

@app.route('/')
def sakums():
    return redirect(url_for('registracija'))

@app.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if request.method == 'POST':
        vards = request.form['vards']
        uzvards = request.form['uzvards']
        lietotajvards = request.form['lietotajvards']
        
        savienojums = sqlite3.connect('zinojumi.db')
        c = savienojums.cursor()
        try:
            c.execute("INSERT INTO lietotaji (vards, uzvards, lietotajvards) VALUES (?, ?, ?)",
                     (vards, uzvards, lietotajvards))
            savienojums.commit()
        except sqlite3.IntegrityError:
            return "Lietotājvārds jau eksistē!"
        finally:
            savienojums.close()
        return redirect(url_for('zinojumi'))
    return render_template('registracija.html')

@app.route('/zinojumi', methods=['GET', 'POST'])
def zinojumi():
    savienojums = sqlite3.connect('zinojumi.db')
    c = savienojums.cursor()
    
    if request.method == 'POST':
        lietotaja_id = request.form['lietotajs']
        zinojums = request.form['zinojums']
        c.execute("INSERT INTO zinojumi (lietotaja_id, zinojums) VALUES (?, ?)",
                 (lietotaja_id, zinojums))
        savienojums.commit()
    
    lietotaji = c.execute("SELECT id, vards, uzvards, lietotajvards FROM lietotaji").fetchall()
    zinojumi = c.execute("""
        SELECT lietotaji.vards, lietotaji.uzvards, zinojumi.zinojums 
        FROM zinojumi 
        JOIN lietotaji ON zinojumi.lietotaja_id = lietotaji.id
        ORDER BY zinojumi.id DESC
    """).fetchall()
    
    savienojums.close()
    return render_template('zinojumi.html', lietotaji=lietotaji, zinojumi=zinojumi)

@app.route('/statistika')
def statistika():
    savienojums = sqlite3.connect('zinojumi.db')
    c = savienojums.cursor()
    statistika = c.execute("""
        SELECT lietotaji.vards, lietotaji.uzvards, COUNT(zinojumi.id) as skaits
        FROM lietotaji
        LEFT JOIN zinojumi ON lietotaji.id = zinojumi.lietotaja_id
        GROUP BY lietotaji.id
        ORDER BY skaits DESC
    """).fetchall()
    savienojums.close()
    return render_template('statistika.html', statistika=statistika)

if __name__ == '__main__':
    inicializet_db()
    app.run(debug=True)
