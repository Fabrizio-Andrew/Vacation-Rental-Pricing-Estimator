// import service worker
importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.2.0/workbox-sw.js');

// workbox.routing.registerRoute(
//     // cache css files and js and images
//     /.*\.(?:js|css|png|jpg|jpeg|svg|gif)/,
//     // use cache but update in the background ASAP
//     new workbox.strategies.StaleWhileRevalidate({
//         // use a custom cache name
//         cacheName: 'static-resources',
//     })
    


// );

// This is the "Offline copy of assets" service worker

const CACHE = "pwa-offline";

self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

workbox.routing.registerRoute(
  new RegExp('/*'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE
  })
);