from pyscript import display, HTML

# 1. TVOJI PROIZVODI (Izvukao sam deo iz tvog koda)
proizvodi = {
    "HRANA": ["Hleb", "Mleko", "Jaja", "Brašno", "Šećer", "Ulje"],
    "HIGIJENA": ["Sapun", "Šampon", "Pasta za zube", "Deterdžent"],
    "OSTALO": ["Baterije", "Sijalice"]
}

# 2. FUNKCIJA ZA PRIKAZ
def prikazi_kategoriju(ime_kategorije):
    lista = proizvodi.get(ime_kategorije, [])
    stavke_html = "".join([f"<div style='padding:10px; border-bottom:1px solid #eee;'>{s}</div>" for s in lista])
    
    html = f"""
    <div style="font-family: Arial; max-width: 400px; margin: auto; background: white; border-radius: 15px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <h2 style="color: #2c3e50; text-align: center;">📦 {ime_kategorije}</h2>
        {stavke_html}
        <button py-click="nazad" style="width:100%; margin-top:15px; padding:10px; background:#6c757d; color:white; border:none; border-radius:5px;">Nazad na kategorije</button>
    </div>
    """
    display(HTML(html), target="python-output", append=False)

def nazad(event):
    pocetni_ekran()

def pocetni_ekran():
    dugmad = "".join([f'<button py-click="lambda e: prikazi_kategoriju(\'{k}\')" style="width:100%; margin:5px 0; padding:15px; background:#007bff; color:white; border:none; border-radius:10px; font-size:16px;">{k}</button>' for k in proizvodi.keys()])
    
    html = f"""
    <div style="font-family: Arial; max-width: 400px; margin: auto; background: #f8f9fa; border-radius: 15px; padding: 20px;">
        <h1 style="text-align:center; color:#333;">Zalihe</h1>
        {dugmad}
    </div>
    """
    display(HTML(html), target="python-output", append=False)

# Pokretanje aplikacije
pocetni_ekran()
