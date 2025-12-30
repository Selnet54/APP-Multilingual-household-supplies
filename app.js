document.getElementById("unosForma").addEventListener("submit", function (e) {
  e.preventDefault();

  const proizvod = {
    naziv: document.getElementById("naziv").value.trim(),
    kolicina: document.getElementById("kolicina").value,
    jedinica: document.getElementById("jedinica").value,
    rok: document.getElementById("rok").value,
    mesto: document.getElementById("mesto").value,
    vreme: new Date().toISOString()
  };

  const tx = db.transaction("zalihe", "readwrite");
  const store = tx.objectStore("zalihe");
  store.add(proizvod);

  tx.oncomplete = () => {
    document.getElementById("unosForma").reset();
    prikaziZalihe();
  };
});

function prikaziZalihe() {
  const lista = document.getElementById("lista");
  lista.innerHTML = "";

  const tx = db.transaction("zalihe", "readonly");
  const store = tx.objectStore("zalihe");

  store.openCursor().onsuccess = event => {
    const cursor = event.target.result;
    if (cursor) {
      const p = cursor.value;

      const li = document.createElement("li");
      li.textContent =
        `${p.naziv} – ${p.kolicina} ${p.jedinica} | ${p.mesto}` +
        (p.rok ? ` | Rok: ${p.rok}` : "");

      lista.appendChild(li);
      cursor.continue();
    }
  };
}
