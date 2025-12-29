import sqlite3
from pyscript import display, HTML

# 1. BAZA PODATAKA (Isto kao kod vas)
conn = sqlite3.connect('domacinstvo.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS zalihe
             (id INTEGER PRIMARY KEY AUTOINCREMENT, stavka TEXT, kolicina REAL)''')
conn.commit()

# 2. FUNKCIJE LOGIKE
def dodaj_stavku(event):
    stavka = Element("stavka-input").element.value
    kolicina = Element("kolicina-input").element.value
    
    if stavka and kolicina:
        c.execute("INSERT INTO zalihe (stavka, kolicina) VALUES (?, ?)", (stavka, float(kolicina)))
        conn.commit()
        prikazi_zalihe()
        # Ocisti polja
        Element("stavka-input").element.value = ""
        Element("kolicina-input").element.value = ""

def prikazi_zalihe():
    c.execute("SELECT * FROM zalihe")
    podaci = c.fetchall()
    
    html_tabele = "<table border='1' style='width:100%; border-collapse: collapse; margin-top:10px;'>"
    html_tabele += "<tr style='background-color:#ddd;'><th>ID</th><th>Stavka</th><th>Količina</th></tr>"
    
    for red in podaci:
        html_tabele += f"<tr><td>{red[0]}</td><td>{red[1]}</td><td>{red[2]}</td></tr>"
    html_tabele += "</table>"
    
    Element("tabela-prikaz").element.innerHTML = html_tabele

# 3. KREIRANJE WEB INTERFEJSA (Menja Tkinter)
web_gui = """
<div style="font-family: sans-serif; max-width: 500px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px;">
    <h2>📦 Zalihe Domaćinstva</h2>
    
    <input type="text" id="stavka-input" placeholder="Naziv stavke" style="padding: 10px; width: 80%; margin-bottom: 5px;"><br>
    <input type="number" id="kolicina-input" placeholder="Količina" style="padding: 10px; width: 80%; margin-bottom: 10px;"><br>
    
    <button py-click="dodaj_stavku" style="padding: 10px 20px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">
        Dodaj u bazu
    </button>
    
    <hr>
    <h3>Trenutno stanje:</h3>
    <div id="tabela-prikaz"></div>
</div>
"""

# Prikazi sve na ekranu
display(HTML(web_gui), target="python-output")
prikazi_zalihe()
