import pyodide
import pyodide.ffi
from pyscript import display, HTML
from js import document

# --- 1. NASLOVNA PORUKA NA 10 JEZIKA ---
# Ovo je tekst koji će se menjati u plavom polju
naslovi_izbor_jezika = {
    "srpski": "IZABERITE JEZIK",
    "hungary": "VÁLASSZ NYELVET",
    "ukrajinski": "ВИБЕРІТЬ МОВУ",
    "ruski": "ВЫБЕРИТЕ ЯЗЫК",
    "english": "SELECT LANGUAGE",
    "deutsch": "SPRACHE WÄHLEN",
    "mandarinski": "选择语言",
    "espanol": "SELECCIONE IDIOMA",
    "portugalski": "SELECIONAR IDIOMA",
    "francais": "CHOISIR LA LANGUE"
}

# --- 2. FUNKCIJA ZA PRIKAZ JEZIKA ---
def prikazi_jezike():
    # Lista zastava i kodova jezika
    jezici = [
        ("🇷🇸 Srpski", "srpski"), ("🇭🇺 Magyar", "hungary"), 
        ("🇺🇦 Українська", "ukrajinski"), ("🇷🇺 Pусский", "ruski"), 
        ("🇬🇧 English", "english"), ("🇩🇪 Deutsch", "deutsch"),
        ("🇨🇳 中文", "mandarinski"), ("🇪🇸 Español", "espanol"), 
        ("🇵🇹 Português", "portugalski"), ("🇫🇷 Français", "francais")
    ]
    
    # Pravimo HTML za dugmad u dve kolone
    html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px;">'
    for ime, kod in jezici:
        html += f'<button class="btn-lang" id="l-{kod}" style="height: 80px;">{ime}</button>'
    html += '</div>'
    
    # Postavljamo naslov u plavo polje (spajamo sve jezike za početak)
    sve_poruke = " / ".join(naslovi_izbor_jezika.values())
    document.getElementById("title").innerText = "IZBOR JEZIKA"
    document.getElementById("title").style.fontSize = "18px"
    
    # Prikazujemo dugmad na ekranu
    display(HTML(html), target="app-body", append=False)
    
    # Povezujemo svako dugme da ispiše koji je jezik izabran
    for _, kod in jezici:
        document.getElementById(f"l-{kod}").onclick = pyodide.ffi.create_proxy(lambda e, k=kod: potvrdio_izbor(k))

def potvrdio_izbor(k):
    # Kada klikneš na zastavu, naslov se menja u taj jezik
    izabrani_naslov = naslovi_izbor_jezika.get(k, "Selected")
    document.getElementById("title").innerText = izabrani_naslov
    
    # Ispisujemo kratku poruku ispod
    poruka = f'<div style="text-align:center; margin-top:50px;"><h2>Uspešno ste izabrali: {k.upper()}</h2>'
    poruka += '<p>Sledeći korak: Ubacivanje kategorija...</p>'
    poruka += '<button onclick="location.reload()" class="btn-cat">PONOVI IZBOR</button></div>'
    display(HTML(poruka), target="app-body", append=False)

# POKRETANJE
prikazi_jezike()
