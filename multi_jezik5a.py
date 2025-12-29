from pyscript import display, HTML, window

# 1. TVOJI PODACI
proizvodi = {
    "HRANA": ["Hleb", "Mleko", "Jaja", "Brašno", "Šećer", "Ulje"],
    "HIGIJENA": ["Sapun", "Šampon", "Pasta za zube", "Deterdžent"],
    "OSTALO": ["Baterije", "Sijalice"]
}

# 2. FUNKCIJA KOJA REŠAVA "UNDEFINED" PROBLEM
def prikazi(ime):
    lista = proizvodi.get(ime, [])
    stavke_html = "".join([f"<div style='padding:15px; border-bottom:1px solid #eee; font-size:20px;'>{s}</div>" for s in lista])
    
    sadrzaj = f"""
    <div style="font-family: sans-serif; max-width: 400px; margin: auto; background: white; border-radius: 15px; padding: 20px;">
        <h2 style="text-align: center; color: #007bff;">📦 {ime}</h2>
        {stavke_html}
        <button onclick="location.reload()" style="width:100%; margin-top:20px; padding:15px; background:#6c757d; color:white; border:none; border-radius:10px; font-size:18px;">⬅️ NAZAD</button>
    </div>
    """
    display(HTML(sadrzaj), target="python-output", append=False)

# 3. POVEZIVANJE SA DUGMIĆIMA (Ovo sprečava grešku)
window.prikazi_hranu = lambda e: prikazi("HRANA")
window.prikazi_higijenu = lambda e: prikazi("HIGIJENA")
window.prikazi_ostalo = lambda e: prikazi("OSTALO")

def pocetni_ekran():
    html = """
    <div style="font-family: sans-serif; max-width: 400px; margin: auto; text-align:center; padding: 10px;">
        <h1 style="color:#333; margin-bottom:20px;">🏠 MOJE ZALIHE</h1>
        
        <button id="btn-hrana" py-click="prikazi_hranu" style="width:100%; margin:10px 0; padding:25px; background:#007bff; color:white; border:none; border-radius:15px; font-size:22px; font-weight:bold;">🍎 HRANA</button>
        
        <button id="btn-higijena" py-click="prikazi_higijenu" style="width:100%; margin:10px 0; padding:25px; background:#28a745; color:white; border:none; border-radius:15px; font-size:22px; font-weight:bold;">🧼 HIGIJENA</button>
        
        <button id="btn-ostalo" py-click="prikazi_ostalo" style="width:100%; margin:10px 0; padding:25px; background:#fd7e14; color:white; border:none; border-radius:15px; font-size:22px; font-weight:bold;">🔧 OSTALO</button>
    </div>
    """
    display(HTML(html), target="python-output")

pocetni_ekran()
