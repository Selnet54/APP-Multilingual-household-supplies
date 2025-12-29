from pyscript import display, HTML
import pyodide

# --- VAŠI ORIGINALNI PODACI IZ KODA ---
main_categories = {
    "srpski": ["Belo meso", "Crveno meso", "Sitna divljač", "Krupna divljač", "Riba", "Mlečni proizvodi", "Povrće", "Zimnica i kompoti", "Testo i Slatkiši", "Pića", "Hemija i higijena", "Ostalo"],
    "hungary": ["Fehér hús", "Vörös hús", "Apróvad", "Nagyvad", "Hal", "Tejtermékek", "Zöldség", "Befőttek és kompótok", "Tészta és Édességek", "Italok", "Kémia i higiénia", "Egyéb"]
    # ... ovde ćemo dodati i ostale jezike koje ste poslali
}

# Koristimo deo vaših podkategorija za test
sub_categories = {
    "srpski": {
        "Belo meso": ["Pileće", "Ćureće", "Guska", "Patka", "Ostalo"],
        "Crveno meso": ["Svinjsko", "Jagnjeće", "Ovčije", "Juneće", "Govedina", "Konjsko", "Zečije", "Ostalo"],
        "Hemija i higijena": ["Sanitar", "Lična higijena", "Pribor", "Ostalo"]
    }
}

# Koristimo vaše specifične delove proizvoda
product_parts = {
    "srpski": {
        "Pileće": ["Gril pile", "Pile celo", "Ceo batak", "Karabatak", "Belo (grudi)", "File", "Krilca", "Mleveno"],
        "Svinjsko": ["Šnicla", "Karmenadla", "Vrat", "But", "Kare", "Rebra", "Mleveno"],
        "Lična higijena": ["Sapun", "Šampon", "Dezodorans", "Brijač"]
    }
}

zalihe = {}
trenutni_jezik = "srpski"

def prikazi_glavni_meni():
    html = "<div style='background:#f8f9fa; padding:15px; border-radius:15px; text-align:center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>"
    html += "<h2 style='color:#333;'>📦 MOJE ZALIHE</h2>"
    for cat in main_categories[trenutni_jezik]:
        html += f'<button id="cat-{cat}" style="width:90%; padding:15px; margin:8px; background:#007bff; color:white; border:none; border-radius:10px; font-size:18px; font-weight:bold;">{cat}</button>'
    html += "</div>"
    display(HTML(html), target="python-output", append=False)
    
    from js import document
    for cat in main_categories[trenutni_jezik]:
        document.getElementById(f"cat-{cat}").onclick = pyodide.ffi.create_proxy(lambda e, c=cat: prikazi_podkategorije(c))

def prikazi_podkategorije(glavna_kat):
    html = f"<div style='padding:10px;'><button id='nazad' style='background:#6c757d; color:white; border:none; padding:10px; border-radius:5px;'>⬅️ Nazad</button>"
    html += f"<h3 style='text-align:center;'>{glavna_kat}</h3>"
    
    lista = sub_categories[trenutni_jezik].get(glavna_kat, ["Ostalo"])
    for sub in lista:
        html += f'<button id="sub-{sub}" style="width:90%; padding:15px; margin:8px; background:#28a745; color:white; border:none; border-radius:10px; font-size:17px;">{sub}</button>'
    html += "</div>"
    display(HTML(html), target="python-output", append=False)
    
    from js import document
    document.getElementById("nazad").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_glavni_meni())
    for sub in lista:
        document.getElementById(f"sub-{sub}").onclick = pyodide.ffi.create_proxy(lambda e, s=sub: prikazi_artikle(s))

def prikazi_artikle(podkat):
    html = f"<div style='padding:10px;'><button id='nazad-pod' style='background:#6c757d; color:white; border:none; padding:10px; border-radius:5px;'>⬅️ Nazad</button>"
    html += f"<h3 style='text-align:center;'>{podkat}</h3>"
    
    lista = product_parts[trenutni_jezik].get(podkat, ["Ostalo"])
    for art in lista:
        kol = zalihe.get(art, 0)
        html += f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding:15px; background:white; margin-bottom:8px; border-radius:10px; border-left: 5px solid #28a745;">
            <span style="font-size:18px; font-weight:500;">{art}</span>
            <div style="display:flex; align-items:center; gap:15px;">
                <button id="m-{art}" style="width:35px; height:35px; border-radius:50%; border:1px solid #ccc;">-</button>
                <b style="font-size:20px; min-width:25px; text-align:center;">{kol}</b>
                <button id="p-{art}" style="width:35px; height:35px; border-radius:50%; background:#28a745; color:white; border:none;">+</button>
            </div>
        </div>"""
    html += "</div>"
    display(HTML(html), target="python-output", append=False)
    
    from js import document
    document.getElementById("nazad-pod").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_glavni_meni())
    for art in lista:
        document.getElementById(f"m-{art}").onclick = pyodide.ffi.create_proxy(lambda e, a=art: menjaj(a, -1, podkat))
        document.getElementById(f"p-{art}").onclick = pyodide.ffi.create_proxy(lambda e, a=art: menjaj(a, 1, podkat))

def menjaj(art, delta, podkat):
    zalihe[art] = max(0, zalihe.get(art, 0) + delta)
    prikazi_artikle(podkat)

prikazi_glavni_meni()
