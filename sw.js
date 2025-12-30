const CACHE_NAME = "zalihe-v1";
const urlsToCache = [
  "./",
  "./index.html",
  "./app.html",
  "./style.css",
  "./app.js",
  "./db.js",
  "./manifest.json",
  "./icons/192.jpg",
  "./icons/512.jpg"
];

// Instalacija SW i keširanje fajlova
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Aktivacija SW i čišćenje starih keševa
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => 
      Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      )
    )
  );
});

// Fetch handler - vraća iz keša ili sa mreže
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
