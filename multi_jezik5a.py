from pyscript import display, HTML

# 1. TVOJI PROIZVODI
proizvodi = {
    "HRANA": ["Hleb", "Mleko", "Jaja", "Brašno", "Šećer", "Ulje"],
    "HIGIJENA": ["Sapun", "Šampon", "Pasta za zube", "Deterdžent"],
    "OSTALO": ["Baterije", "Sijalice"]
}

# 2. FUNKCIJE KOJE SE POZIVAJU NA KLIK
def prikazi_hranu(event):
    prikazi_kategoriju("HRANA")

def prikazi_higijenu(event):
    prikazi_kategoriju("HIGIJENA")

def prikazi_ostalo(event):
    prikazi_kategoriju("OSTALO")

def nazad(event):
    pocetni_ekran()

# 3. GLAVNA LOGIKA ZA CRTANJE
def prikazi_kategoriju(ime_kategorije):
    lista = proizvodi.get(ime_kategorije, [])
    stavke_html = "".join([f"<div style='padding:12px; border-bottom:1px solid #eee; font-size:18px;'>{s}</div>" for s in lista])
    
    html = f"""
    <div style="font-family: Arial; max-width: 400px; margin: auto; background: white; border-radius: 15px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <h2 style="color: #2c3e50; text-align: center; border-bottom: 2px solid #007bff; padding-bottom:10px;">📦 {ime_kategorije}</h2>
        <div style="margin-bottom:20px;">{stavke_html}</div>
        <button py-click="nazad" style="width:100%; padding:15px; background:#6c757d; color:white; border:none; border-radius:10px; font-size:16px; font-weight:bold;">⬅️ NAZAD</button>
    </div>
    """
    display(HTML(html), target="python-output", append=False)

def pocetni_ekran():
    html = """
    <div style="font-family: Arial; max-width: 400px; margin: auto; background: #f8f9fa; border-radius: 15px; padding: 20px; text-align:center;">
        <h1 style="color:#333; margin-bottom:25px;">🏠 MOJE ZALIHE</h1>
        
        <button py-click="prikazi_hranu" style="width:100%; margin:8px 0; padding:20px; background:#007bff; color:white; border:none; border-radius:12px; font-size:18px; font-weight:bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">🍎 HRANA</button>
        
        <button py-click="prikazi_higijenu" style="width:100%; margin:8px 0; padding:20px; background:#28a745; color:white; border:none; border-radius:12px; font-size:18px; font-weight:bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">🧼 HIGIJENA</button>
        
        <button py-click="prikazi_ostalo" style="width:100%; margin:8px 0; padding:20px; background:#fd7e14; color:white; border:none; border-radius:12px; font-size:18px; font-weight:bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">🔧 OSTALO</button>
        
        <p style="margin-top:30px; color:gray; font-size:12px;">Verzija 1.0 - Web App</p>
    </div>
    """
    display(HTML(html), target="python-output", append=False)

# Pokretanje aplikacije pri učitavanju
pocetni_ekran()
