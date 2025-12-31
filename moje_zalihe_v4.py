import pyodide
import pyodide.ffi
from pyscript import display, HTML
from js import document

# --- 1. SVI NASLOVI ZA PLAVI PRAVOUGAONIK ---
lista_naslova = [
    "IZABERITE JEZIK", "VÁLASSZ NYELVET", "ВИБЕРІТЬ МОВУ", 
    "ВЫБЕРИТЕ ЯЗЫК", "SELECT LANGUAGE", "SPRACHE WÄHLEN", 
    "选择语言", "SELECCIONE IDIOMA", "SELECIONAR IDIOMA", "CHOISIR LA LANGUE"
]

# Spajamo ih u jedan dugački niz sa kosom crtom
pun_tekst = " / ".join(lista_naslova)

def prikazi_jezike():
    # 1. Postavljamo dugački tekst u plavi header
    header_title = document.getElementById("title")
    header_title.innerText = pun_tekst
    
    # Smanjujemo malo font da bi više teksta stalo u vidno polje
    header_title.style.fontSize = "14px" 
    header_title.style.whiteSpace = "normal" # Dozvoljava tekstu da ide u više redova ako treba

    # 2. Pravimo dugmad sa zastavama
    jezici = [
        ("🇷🇸 Srpski", "srpski"), ("🇭🇺 Magyar", "hungary"), 
        ("🇺🇦 Українська", "ukrajinski"), ("🇷🇺 Pусский", "ruski"), 
        ("🇬🇧 English", "english"), ("🇩🇪 Deutsch", "deutsch"),
        ("🇨🇳 中文", "mandarinski"), ("🇪🇸 Español", "espanol"), 
        ("🇵🇹 Português", "portugalski"), ("🇫🇷 Français", "francais")
    ]
    
    html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 10px;">'
    for ime, kod in jezici:
        html += f'<button class="btn-lang" id="l-{kod}" style="height: 70px; font-size: 16px;">{ime}</button>'
    html += '</div>'
    
    display(HTML(html), target="app-body", append=False)
    
    # 3. Povezivanje dugmadi
    for _, kod in jezici:
        document.getElementById(f"l-{kod}").onclick = pyodide.ffi.create_proxy(lambda e, k=kod: izbor_jezika(k))

def izbor_jezika(k):
    # Samo privremena potvrda dok ne ubacimo kategorije
    document.getElementById("title").innerText = f"IZABRANO: {k.upper()}"
    display(HTML(f"<h3>Sledeći korak: Prikaz kategorija za {k}</h3>"), target="app-body", append=False)

# POKRETANJE
prikazi_jezike()
