let db;

const request = indexedDB.open("ZaliheDB", 1);

request.onupgradeneeded = event => {
    db = event.target.result;

    if (!db.objectStoreNames.contains("zalihe")) {
        db.createObjectStore("zalihe", {
            keyPath: "id",
            autoIncrement: true
        });
    }
};

request.onsuccess = event => {
    db = event.target.result;
    prikaziZalihe();
};

request.onerror = () => {
    alert("Greška pri otvaranju baze");
};
