const CACHE_NAME = 'zalihe-app-cache-v3';

const FILES_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './install.js',
  './multi-jezik5a.py',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

// INSTALL
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(FILES_TO_CACHE);
    })
  );
});

// ACTIVATE
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

// FETCH
self.addEventListener('fetch', event => {
  // PyScript CDN uvek online
  if (event.request.url.includes('pyscript.net')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    }).catch(() => {
      return new Response('Offline mode', { status: 503 });
    })
  );
});
