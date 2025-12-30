const CACHE = "zalihe-v1";

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE).then(cache =>
      cache.addAll([
        "./",
        "./index.html",
        "./app.html",
        "./style.css",
        "./app.js",
        "./db.js",
        "./manifest.json"
      ])
    )
  );
});
