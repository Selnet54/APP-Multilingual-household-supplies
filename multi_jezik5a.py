from pyscript import display, HTML, window
import pyodide

# 1. VAŠA KOMPLETNA LISTA (Sada je proširena)
podaci = {
    "SRB": {
        "naslov": "ZALIHE DOMAĆINSTVA",
        "nazad": "⬅️ NAZAD",
        "kat": ["HRANA", "HIGIJENA", "OSTALO"],
        "proizvodi": {
            "HRANA": ["Hleb", "Mleko", "Jaja", "Brašno", "Šećer", "Ulje", "Meso", "Povrće"],
            "HIGIJENA": ["Sapun", "Šampon", "Pasta za zube", "Deterdžent", "Toalet papir"],
            "OSTALO": ["Baterije", "Sijalice", "Sveće"]
        }
    },
    "GER": {
        "naslov": "HAUSHALTSVORRAT",
        "nazad": "⬅️ ZURÜCK",
        "kat": ["LEBENSMITTEL", "HYGIENE", "SONSTIGES"],
        "proizvodi": {
            "LEBENSMITTEL": ["Brot", "Milch", "Eier", "Mehl", "Zucker", "Öl", "Fleisch", "Gemüse"],
            "HYGIENE": ["Seife", "Shampoo", "Zahnpasta", "Waschmittel", "Toilettenpapier"],
            "SONSTIGES": ["Batterien", "Glühbirnen", "Kerzen"]
        }
    }
}

trenutni_jezik = "SRB"

# 2. FUNKCIJA ZA PRIKAZ PROIZVODA
def prikazi_listu(kategorija_index):
    jezik = podaci[trenutni_jezik]
    ime_kat = jezik["kat"][kategorija_index]
    lista = jezik["proizvodi"].get(ime_kat, [])
    
    stavke_html = "".join([f"<div style='padding:15px; border-bottom:1px solid #eee; font-size:20px;'>{s}</div>" for s in lista])
    
    sadrzaj = f"""
    <div style="font-family: sans-serif; max-width: 400px; margin: auto; background: white; border-radius: 15px; padding: 20px;">
        <h2 style="text-align: center; color: #007bff;">{ime_kat}</h2>
        {stavke_html}
        <button onclick="location.reload()" style="width:100%; margin-top:20px; padding:15px; background:#6c757d; color:white; border:none; border-radius:10px; font-size:18px;">{jezik['nazad']}</button>
    </div>
    """
    display(HTML(sadrzaj), target="python-output", append=False)

# 3. POČETNI EKRAN
def pocetni_ekran():
    jezik = podaci[trenutni_jezik]
    
    html = f"""
    <div style="font-family: sans-serif; max-width: 400px; margin: auto; text-align:center;">
        <h1 style="color:#333; margin-bottom:20px;">🏠 {jezik['naslov']}</h1>
        
        <button id="kat0" style="width:100%; margin:10px 0; padding:20px; background:#007bff; color:white; border:none; border-radius:15px; font-size:20px;">🍎 {jezik['kat'][0]}</button>
        <button id="kat1" style="width:100%; margin:10px 0; padding:20px; background:#28a745; color:white; border:none; border-radius:15px; font-size:20px;">🧼 {jezik['kat'][1]}</button>
        <button id="kat2" style="width:100%; margin:10px 0; padding:20px; background:#fd7e14; color:white; border:none; border-radius:15px; font-size:20px;">🔧 {jezik['kat'][2]}</button>
        
        <div style="margin-top:30px;">
            <button id="btnSRB" style="padding:10px;">🇷🇸 SRB</button>
            <button id="btnGER" style="padding:10px;">🇩🇪 GER</button>
        </div>
    </div>
    """
    display(HTML(html), target="python-output", append=False)

    # POVEZIVANJE DUGMADI
    from js import document
    
    def postavi_jezik(lang):
        global trenutni_jezik
        trenutni_jezik = lang
        pocetni_ekran()

    # Proxy za klikove
    document.getElementById("kat0").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_listu(0))
    document.getElementById("kat1").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_listu(1))
    document.getElementById("kat2").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_listu(2))
    
    document.getElementById("btnSRB").onclick = pyodide.ffi.create_proxy(lambda e: postavi_jezik("SRB"))
    document.getElementById("btnGER").onclick = pyodide.ffi.create_proxy(lambda e: postavi_jezik("GER"))

pocetni_ekran()
