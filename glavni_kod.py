from pyscript import display, HTML
import pyodide

# --- VAŠI PODACI (Skraćeno za primer, vi dodajte sve jezike) ---
main_cats = {
    "srpski": ["Belo meso", "Crveno meso", "Hemija i higijena"],
    "deutsch": ["Weißes Fleisch", "Rotes Fleisch", "Chemie und Hygiene"]
}

sub_cats = {
    "srpski": {
        "Belo meso": ["Pileće", "Ćureće"],
        "Hemija i higijena": ["Lična higijena"]
    },
    "deutsch": {
        "Weißes Fleisch": ["Huhn", "Truthahn"],
        "Chemie und Hygiene": ["Persönliche Hygiene"]
    }
}

parts = {
    "srpski": {
        "Pileće": ["Celo pile", "Batak", "Belo meso"],
        "Lična higijena": ["Sapun", "Šampon"]
    },
    "deutsch": {
        "Huhn": ["Ganzes Huhn", "Keule", "Brust"],
        "Persönliche Hygiene": ["Seife", "Shampoo"]
    }
}

# STANJE ZALIHA (Ovo bi u budućnosti išlo u memoriju telefona)
zalihe = {}

trenutni_jezik = "srpski"

def promeni_kolicinu(artikal, delta):
    zalihe[artikal] = zalihe.get(artikal, 0) + delta
    if zalihe[artikal] < 0: zalihe[artikal] = 0
    prikazi_artikle(trenutna_podkat)

def prikazi_jezike():
    html = "<div style='text-align:center; padding:20px;'><h1>IZABERITE JEZIK</h1>"
    for lang in main_cats.keys():
        html += f'<button id="lang-{lang}" style="width:100%; padding:15px; margin:5px; font-size:20px; border-radius:10px;">{lang.upper()}</button>'
    html += "</div>"
    display(HTML(html), target="python-output", append=False)
    
    from js import document
    for lang in main_cats.keys():
        document.getElementById(f"lang-{lang}").onclick = pyodide.ffi.create_proxy(lambda e, l=lang: postavi_jezik(l))

def postavi_jezik(lang):
    global trenutni_jezik
    trenutni_jezik = lang
    prikazi_glavne_kategorije()

def prikazi_glavne_kategorije():
    html = f"<div style='padding:10px;'><button onclick='location.reload()'>⬅️</button><h2>{trenutni_jezik.upper()}</h2>"
    for cat in main_cats[trenutni_jezik]:
        html += f'<button id="cat-{cat}" style="width:100%; padding:20px; margin:5px; background:#007bff; color:white; border-radius:10px; font-size:18px;">{cat}</button>'
    html += "</div>"
    display(HTML(html), target="python-output", append=False)
    
    from js import document
    for cat in main_cats[trenutni_jezik]:
        document.getElementById(f"cat-{cat}").onclick = pyodide.ffi.create_proxy(lambda e, c=cat: prikazi_podkategorije(c))

def prikazi_podkategorije(glavna_kat):
    html = f"<div style='padding:10px;'><button id='back-to-main'>⬅️ NAZAD</button><h2>{glavna_kat}</h2>"
    lista = sub_cats[trenutni_jezik].get(glavna_kat, [])
    for sub in lista:
        html += f'<button id="sub-{sub}" style="width:100%; padding:20px; margin:5px; background:#28a745; color:white; border-radius:10px; font-size:18px;">{sub}</button>'
    html += "</div>"
    display(HTML(html), target="python-output", append=False)
    
    from js import document
    document.getElementById("back-to-main").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_glavne_kategorije())
    for sub in lista:
        document.getElementById(f"sub-{sub}").onclick = pyodide.ffi.create_proxy(lambda e, s=sub: prikazi_artikle(s))

def prikazi_artikle(podkat):
    global trenutna_podkat
    trenutna_podkat = podkat
    html = f"<div style='padding:10px;'><button id='back-to-sub'>⬅️ NAZAD</button><h2>{podkat}</h2>"
    lista_artikala = parts[trenutni_jezik].get(podkat, [])
    
    for art in lista_artikala:
        kol = zalihe.get(art, 0)
        html += f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding:15px; border-bottom:1px solid #ddd;">
            <span style="font-size:18px;">{art}</span>
            <div>
                <button id="m-{art}" style="padding:10px 15px;">-</button>
                <b style="margin:0 10px; font-size:20px;">{kol}</b>
                <button id="p-{art}" style="padding:10px 15px; background:green; color:white;">+</button>
            </div>
        </div>"""
    html += "</div>"
    display(HTML(html), target="python-output", append=False)
    
    from js import document
    document.getElementById("back-to-sub").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_glavne_kategorije())
    for art in lista_artikala:
        document.getElementById(f"m-{art}").onclick = pyodide.ffi.create_proxy(lambda e, a=art: promeni_kolicinu(a, -1))
        document.getElementById(f"p-{art}").onclick = pyodide.ffi.create_proxy(lambda e, a=art: promeni_kolicinu(a, 1))

prikazi_jezike()
