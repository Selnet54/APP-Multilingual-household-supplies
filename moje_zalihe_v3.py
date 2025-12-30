from pyscript import display, HTML
import pyodide
from js import localStorage, document

# --- 1. VAŠI ORIGINALNI PODACI (Svi jezici iz multi-jezik5a.py) ---
main_categories_translations = {
    "srpski": ["Belo meso", "Crveno meso", "Sitna divljač", "Krupna divljač", "Riba", "Mlečni proizvodi", "Povrće", "Zimnica i kompoti", "Testo i Slatkiši", "Pića", "Hemija i higijena", "Ostalo"],
    "hungary": ["Fehér hús", "Vörös hús", "Apróvad", "Nagyvad", "Hal", "Tejtermékek", "Zöldség", "Befőttek és kompótok", "Tészta és Édességek", "Italok", "Kémia i higiénia", "Egyéb"],
    "ukrajinski": ["Біле м'ясо", "Червоне м'ясо", "Дрібна дичина", "Велика дичина", "Риба", "Молочні продукти", "Овочі", "Заготовки та компоти", "Тісто та солодощі", "Напої", "Хімія та гігієна", "Інше"],
    "ruski": ["Белое мясо", "Красное мясо", "Мелкая дичь", "Крупная дичь", "Рыба", "Молочные продукты", "Овощи", "Заготовки и компоты", "Тесто и сладости", "Напитки", "Химия и гигиена", "Прочее"],
    "english": ["White meat", "Red meat", "Small game", "Big game", "Fish", "Dairy products", "Vegetables", "Pickles and compotes", "Dough and Sweets", "Drinks", "Chemistry and hygiene", "Other"],
    "deutsch": ["Weißes Fleisch", "Rotes Fleisch", "Kleinwild", "Großwild", "Fisch", "Milchprodukte", "Gemüse", "Konserven und Kompotte", "Teig und Süßigkeiten", "Getränke", "Chemie und Hygiene", "Andere"],
    "mandarinski": ["白肉", "红肉", "小野味", "大野味", "鱼", "乳制品", "蔬菜", "腌菜和蜜饯", "面食和甜点", "饮料", "化学和卫生", "其他"],
    "espanol": ["Carne blanca", "Carne roja", "Caza menor", "Caza mayor", "Pescado", "Lácteos", "Verduras", "Encurtidos y compotas", "Pasta y dulces", "Bebidas", "Química e higiene", "Otros"],
    "portugalski": ["Carne branca", "Carne vermelha", "Caça pequena", "Caça grande", "Peixe", "Laticínios", "Vegetais", "Conservas e compotas", "Massas e doces", "Bebidas", "Química e higiene", "Outros"],
    "francais": ["Viande blanche", "Viande rouge", "Petit gibier", "Grand gibier", "Poisson", "Produits laitiers", "Légumes", "Conserves et compotes", "Pâtes et sucreries", "Boissons", "Chimie et hygiène", "Autres"]
}

# --- 2. LOGIKA ZA SKLADIŠTENJE (LocalStorage umesto SQLite) ---
def get_count(item_name):
    val = localStorage.getItem(item_name)
    return int(val) if val else 0

def update_count(item, delta, subcat):
    new_val = max(0, get_count(item) + delta)
    localStorage.setItem(item, str(new_val))
    prikazi_artikle(subcat)

# --- 3. NAVIGACIJA KROZ APLIKACIJU ---
trenutni_jezik = "srpski"

def prikazi_jezike():
    jezici = [
        ("Srpski", "srpski"), ("Magyar", "hungary"), ("Українська", "ukrajinski"),
        ("Pусский", "ruski"), ("English", "english"), ("Deutsch", "deutsch"),
        ("中文", "mandarinski"), ("Español", "espanol"), ("Português", "portugalski"),
        ("Français", "francais")
    ]
    html = '<div class="container">'
    for ime, kod in jezici:
        html += f'<button class="btn-lang" id="l-{kod}">{ime}</button>'
    html += '</div>'
    document.getElementById("title").innerText = "IZBOR JEZIKA / VÁLASSZ NYELVET"
    display(HTML(html), target="app-body", append=False)
    
    for _, kod in jezici:
        btn = document.getElementById(f"l-{kod}")
        btn.onclick = pyodide.ffi.create_proxy(lambda e, k=kod: postavi_jezik(k))

def postavi_jezik(k):
    global trenutni_jezik
    trenutni_jezik = k
    prikazi_glavne_kategorije()

def prikazi_glavne_kategorije():
    kategorije = main_categories_translations.get(trenutni_jezik, main_categories_translations["srpski"])
    html = '<div class="container">'
    for cat in kategorije:
        html += f'<button class="btn-cat" id="c-{cat}">{cat}</button>'
    html += '<button class="btn-lang" style="background:#ff4444; color:white; margin-top:20px;" id="nazad-jezici">IZLAZ / BACK</button>'
    html += '</div>'
    document.getElementById("title").innerText = trenutni_jezik.upper()
    display(HTML(html), target="app-body", append=False)
    
    document.getElementById("nazad-jezici").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_jezike())
    for cat in kategorije:
        document.getElementById(f"c-{cat}").onclick = pyodide.ffi.create_proxy(lambda e, c=cat: prikazi_artikle(c))

# Ovo je "srce" - ovde će se prikazivati artikli sa + i -
def prikazi_artikle(kategorija):
    # Za demo koristimo par artikala, kasnije ćemo uliti svih 3000
    artikli = ["Artikal 1", "Artikal 2", "Artikal 3"] # Ovde idu vaši podaci
    
    html = '<div class="container">'
    for art in artikli:
        count = get_count(art)
        html += f'''
        <div class="item-card">
            <span>{art}</span>
            <div style="display:flex; align-items:center; gap:10px;">
                <button id="m-{art}" style="width:40px;height:40px;border-radius:50%; border:1px solid #ccc;">-</button>
                <b style="min-width:30px; text-align:center;">{count}</b>
                <button id="p-{art}" style="width:40px;height:40px;border-radius:50%; background:#4CAF50; color:white; border:none;">+</button>
            </div>
        </div>
        '''
    html += f'<button class="btn-lang" id="nazad-glavno">⬅ NAZAD</button>'
    html += '</div>'
    document.getElementById("title").innerText = kategorija
    display(HTML(html), target="app-body", append=False)
    
    document.getElementById("nazad-glavno").onclick = pyodide.ffi.create_proxy(lambda e: prikazi_glavne_kategorije())
    for art in artikli:
        document.getElementById(f"m-{art}").onclick = pyodide.ffi.create_proxy(lambda e, a=art: update_count(a, -1, kategorija))
        document.getElementById(f"p-{art}").onclick = pyodide.ffi.create_proxy(lambda e, a=art: update_count(a, 1, kategorija))

prikazi_jezike()
