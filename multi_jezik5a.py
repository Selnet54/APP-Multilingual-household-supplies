from pyscript import display, HTML
import pyodide

# 1. PODACI
proizvodi = {
    "HRANA": ["Hleb", "Mleko", "Jaja", "Brašno", "Šećer", "Ulje"],
    "HIGIJENA": ["Sapun", "Šampon", "Pasta za zube", "Deterdžent"],
    "OSTALO": ["Baterije", "Sijalice"]
}

# 2. FUNKCIJE
def prikazi_kategoriju(ime):
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

# 3. GLAVNI EKRAN
def pocetni_ekran():
    html = """
    <div style="font-family: sans-serif; max-width: 400px; margin: auto; text-align:center; padding: 10px;">
        <h1 style="color:#333; margin-bottom:20px;">🏠 MOJE ZALIHE</h1>
        <button id="btn1" style="width:100%; margin:10px 0; padding:25px; background:#007bff; color:white; border:none; border-radius:15px; font-size:22px; font-weight:bold;">🍎 HRANA</button>
        <button id="btn2" style="width:100%; margin:10px 0; padding:25px; background:#28a745; color:white; border:none; border-radius:15px; font-size:22px; font-weight:bold;">🧼 HIGIJENA</button>
        <button id="btn3" style="width:100%; margin:10px 0; padding:25px; background:#fd7e14; color:white; border:none; border-radius:15px; font-size:22px; font-weight:bold;">🔧 OSTALO</button>
    </div>
    """
    display(HTML(html), target="python-output")

    # POVEZIVANJE KOJE NE MOŽE DA OMANE
    from js import document
    
    # Pravimo "mostove" za svako dugme posebno
    btn1_proxy = pyodide.ffi.create_proxy(lambda e: prikazi_kategoriju("HRANA"))
    document.getElementById("btn1").addEventListener("click", btn1_proxy)
    
    btn2_proxy = pyodide.ffi.create_proxy(lambda e: prikazi_kategoriju("HIGIJENA"))
    document.getElementById("btn2").addEventListener("click", btn2_proxy)
    
    btn3_proxy = pyodide.ffi.create_proxy(lambda e: prikazi_kategoriju("OSTALO"))
    document.getElementById("btn3").addEventListener("click", btn3_proxy)

pocetni_ekran()
