from pyscript import display, HTML
import pyodide

# 1. VAŠE STAVKE
zalihe = {
    "Hleb": 1,
    "Mleko": 2,
    "Jaja": 10,
    "Sapun": 1
}

def promeni_kolicinu(stavka, delta):
    # Povećaj ili smanji, ali ne ispod nule
    zalihe[stavka] = max(0, zalihe[stavka] + delta)
    osvezi_ekran()

def osvezi_ekran():
    html_sadrzaj = """
    <div style="font-family: Arial; max-width: 450px; margin: auto; background: #ffffff; padding: 20px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px;">📦 STANJE ZALIHA</h2>
    """
    
    for stavka, kolicina in zalihe.items():
        html_sadrzaj += f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px 0; border-bottom: 1px solid #f0f0f0;">
            <span style="font-size: 20px; font-weight: 500; color: #444;">{stavka}</span>
            <div style="display: flex; align-items: center; gap: 20px;">
                <button id="minus-{stavka}" style="width: 45px; height: 45px; border-radius: 50%; border: 1px solid #ddd; background: #f8f9fa; font-size: 24px; cursor: pointer; display: flex; align-items: center; justify-content: center;">-</button>
                <b style="font-size: 22px; min-width: 30px; text-align: center;">{kolicina}</b>
                <button id="plus-{stavka}" style="width: 45px; height: 45px; border-radius: 50%; border: none; background: #28a745; color: white; font-size: 24px; cursor: pointer; display: flex; align-items: center; justify-content: center;">+</button>
            </div>
        </div>
        """
    
    html_sadrzaj += "</div>"
    
    display(HTML(html_sadrzaj), target="python-output", append=False)

    # POVEZIVANJE DUGMADI (Ovo omogućava da klik radi)
    from js import document
    for stavka in zalihe.keys():
        # Pravimo proxy za svako dugme
        minus_btn = document.getElementById(f"minus-{stavka}")
        plus_btn = document.getElementById(f"plus-{stavka}")
        
        minus_btn.onclick = pyodide.ffi.create_proxy(lambda e, s=stavka: promeni_kolicinu(s, -1))
        plus_btn.onclick = pyodide.ffi.create_proxy(lambda e, s=stavka: promeni_kolicinu(s, 1))

# Prvo pokretanje
osvezi_ekran()
