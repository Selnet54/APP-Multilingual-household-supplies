from pyscript import display, HTML, window
import pyodide

# 1. PODACI SA KOLIČINAMA (Sada je rečnik sa brojevima)
zalihe = {
    "Hleb": 1,
    "Mleko": 2,
    "Jaja": 10,
    "Sapun": 1
}

trenutni_jezik = "SRB"

def promeni_kolicinu(stavka, delta):
    zalihe[stavka] = max(0, zalihe[stavka] + delta)
    prikazi_listu()

def prikazi_listu():
    stavke_html = ""
    for stavka, kolicina in zalihe.items():
        # Pravimo red sa dugmićima za svaki proizvod
        stavke_html += f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid #eee;">
            <span style="font-size: 18px; font-weight: bold;">{stavka}</span>
            <div style="display: flex; align-items: center; gap: 15px;">
                <button id="minus-{stavka}" style="width:40px; height:40px; border-radius:50%; border:1px solid #ccc; background:#f8f9fa; font-size:20px;">-</button>
                <span style="font-size: 20px; min-width: 30px; text-align: center;">{kolicina}</span>
                <button id="plus-{stavka}" style="width:40px; height:40px; border-radius:50%; border:none; background:#28a745; color:white; font-size:20px;">+</button>
            </div>
        </div>
        """
    
    sadrzaj = f"""
    <div style="font-family: sans-serif; max-width: 400px; margin: auto; background: white; border-radius: 15px; padding: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #333;">📦 STANJE ZALIHA</h2>
        {stavke_html}
        <p style="text-align:center; color:gray; margin-top:20px; font-size:12px;">Podaci se čuvaju u memoriji aplikacije</p>
    </div>
    """
    display(HTML(sadrzaj), target="python-output", append=False)

    # POVEZIVANJE DUGMADI (Za svaku stavku pravimo most)
    from js import document
    for stavka in zalihe.keys():
        # Moramo koristiti lambda sa default argumentima da bi zapamtili koja je stavka u pitanju
        document.getElementById(f"minus-{stavka}").onclick = pyodide.ffi.create_proxy(lambda e, s=stavka: promeni_kolicinu(s, -1))
        document.getElementById(f"plus-{stavka}").onclick = pyodide.ffi.create_proxy(lambda e, s=stavka: promeni_kolicinu(s, 1))

prikazi_listu()
