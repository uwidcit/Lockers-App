// https://developer.chrome.com/docs/workbox/modules/workbox-sw/

importScripts(
  'https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js'
);

const {registerRoute} = workbox.routing;
const {CacheFirst} = workbox.strategies;
const {precacheAndRoute} = workbox.precaching;
const {CacheableResponse, CacheableResponsePlugin} = workbox.cacheableResponse;



precacheAndRoute([ { url: '/locker/offline', revision: null }, ...[{"revision":"dad012731df1721b57dc48cf4f1add53","url":"autocomplete.js"},{"revision":"0dd78473fc27caf72ea72c454ec18a84","url":"keep_alive.js"},{"revision":"4f0283c6ce28e888000e978e537a6a56","url":"leaflet/images/layers-2x.png"},{"revision":"a6137456ed160d7606981aa57c559898","url":"leaflet/images/layers.png"},{"revision":"401d815dc206b8dc1b17cd0e37695975","url":"leaflet/images/marker-icon-2x.png"},{"revision":"2273e3d8ad9264b7daa5bdbf8e6b47f8","url":"leaflet/images/marker-icon.png"},{"revision":"44a526eed258222515aa21eaffd14a96","url":"leaflet/images/marker-shadow.png"},{"revision":"e3892d074983b63ffd604791f43d9e30","url":"leaflet/leaflet-src.esm.js"},{"revision":"df65e4dedb0f7e6b0e29ed00ec6fa463","url":"leaflet/leaflet-src.js"},{"revision":"049a8e8f1dbe4187144fa2343a2754c5","url":"leaflet/leaflet.css"},{"revision":"35b48eb991f383702f153452506e07b2","url":"leaflet/leaflet.js"},{"revision":"c04b5861eed5390a1803bbf55861277e","url":"lockers.js"},{"revision":"887d54f3e212bc67511d78086e044318","url":"main.js"},{"revision":"beec393c821934ccca45f4f161cbe133","url":"manage_locker_offline.html"},{"revision":"9298cb6a6bb2cba6ab1d9dd3f4865b99","url":"map_init.js"},{"revision":"b0663391a6dd5efed956259f29fa18dd","url":"materialize.css"},{"revision":"54596df2e8100554ca1508ce94a2fa9f","url":"materialize.js"},{"revision":"ec1df3ba49973dcb9ff212f052d39483","url":"materialize.min.css"},{"revision":"87d84bf8b4cc051c16092d27b1a7d9b3","url":"materialize.min.js"},{"revision":"13dd5c2619bcbed86af479c1c532d605","url":"static-user.html"},{"revision":"b139cfe10ede9b5038d0064723a6b35b","url":"style.css"},{"revision":"b05bf22f01944cec506282e9024be5c2","url":"util.js"}]]);

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