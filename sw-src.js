// https://developer.chrome.com/docs/workbox/modules/workbox-sw/

importScripts(
  'https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js'
);

const {registerRoute} = workbox.routing;
const {CacheFirst} = workbox.strategies;
const {precacheAndRoute} = workbox.precaching;
const {CacheableResponse, CacheableResponsePlugin} = workbox.cacheableResponse;



precacheAndRoute([ { url: '/locker/offline', revision: null }, ...self.__WB_MANIFEST]);

// Custom wrapper function to log requests and register the route
function registerRouteWithLogging(urlPattern, strategy, options) {
  console.log('Registering route:', urlPattern);

  // Log the request before registering the route
  self.addEventListener('fetch', (event) => {
    console.log('Fetching:', event.request.url);
    // You can log other request details here if needed
  });

  // Register the route with the provided strategy and options
  registerRoute(urlPattern, strategy, options);
}

registerRouteWithLogging(
  '*', // URL pattern to match
  new CacheFirst({
    cacheName: 'lockers-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
);

// Log all network requests
self.addEventListener('fetch', (event) => {
  console.log('SW: Fetching', event.request.url);
  // You can also log other request details like event.request.method, event.request.headers, etc.

  // Pass through the fetch request
  event.respondWith(fetch(event.request));
});