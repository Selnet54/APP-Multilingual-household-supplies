from pyscript import display, HTML

# Test lista proizvoda (Umesto baze, za probu)
zalihe = [
    {"stavka": "Hleb", "kolicina": 2},
    {"stavka": "Mleko", "kolicina": 5}
]

def osveži_prikaz():
    tabela = "<table style='width:100%; background:white; border-collapse:collapse; border-radius:10px; overflow:hidden;'>"
    tabela += "<tr style='background:#007bff; color:white;'><th>Proizvod</th><th>Količina</th></tr>"
    for stavka in zalihe:
        tabela += f"<tr style='border-bottom:1px solid #ddd;'><td style='padding:10px;'>{stavka['stavka']}</td><td>{stavka['kolicina']}</td></tr>"
    tabela += "</table>"
    
    html_interfejs = f"""
    <div style="padding:15px; background:white; border-radius:15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="color:#333;">Moje Zalihe</h2>
        {tabela}
        <p style="margin-top:20px; font-size:12px; color:gray;">Aplikacija radi bez instaliranog Pythona!</p>
    </div>
    """
    display(HTML(html_interfejs), target="python-output")

osveži_prikaz()
