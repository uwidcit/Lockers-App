importScripts('/static/wb/workbox-v7.0.0/workbox-sw.js')
importScripts('/static/wb/workbox-v7.0.0/workbox-routing.prod.js')
importScripts('/static/wb/workbox-v7.0.0/workbox-strategies.prod.js')

workbox.precaching.precacheAndRoute([{"revision":"bc56a6869ac03cd8815461a8a58ca256","url":"autocomplete.js"},{"revision":"9d295ec8b213fdfaac1595e739a950ef","url":"keep_alive.js"},{"revision":"4f0283c6ce28e888000e978e537a6a56","url":"leaflet/images/layers-2x.png"},{"revision":"a6137456ed160d7606981aa57c559898","url":"leaflet/images/layers.png"},{"revision":"401d815dc206b8dc1b17cd0e37695975","url":"leaflet/images/marker-icon-2x.png"},{"revision":"2273e3d8ad9264b7daa5bdbf8e6b47f8","url":"leaflet/images/marker-icon.png"},{"revision":"44a526eed258222515aa21eaffd14a96","url":"leaflet/images/marker-shadow.png"},{"revision":"de8227f9c5a6e5aa0449b8e37c61a5ab","url":"leaflet/leaflet-src.esm.js"},{"revision":"d2f7695952d3f22a85695b58d06b567d","url":"leaflet/leaflet-src.js"},{"revision":"c02c12fe5e21d2493070649584ca38b7","url":"leaflet/leaflet.css"},{"revision":"35b48eb991f383702f153452506e07b2","url":"leaflet/leaflet.js"},{"revision":"c80c3f262ba1e7ee6dd2044ac958e2fb","url":"lockers.js"},{"revision":"870b5ea4295065881458d40c6df53a78","url":"main.js"},{"revision":"9b509c52d596f9fd54f52d535970bcb2","url":"manage_locker_offline.html"},{"revision":"5c939ef677a57602e5e12eaa34058ead","url":"map_init.js"},{"revision":"b0663391a6dd5efed956259f29fa18dd","url":"materialize.css"},{"revision":"9832259e6e013b2e55f342c053c26104","url":"materialize.js"},{"revision":"ec1df3ba49973dcb9ff212f052d39483","url":"materialize.min.css"},{"revision":"5dcfc8944ed380b2215dc28b3f13835f","url":"materialize.min.js"},{"revision":"7a2b4050bd5b0159ba5101b00d60b40f","url":"static-user.html"},{"revision":"ceac046cad1656146e8d521968b87cda","url":"style.css"},{"revision":"1d8179f18fcc6c658c386f9f30ef126b","url":"util.js"}]);

const NaviRoute = new workbox.routing.NavigationRoute(
  new workbox.strategies.NetworkFirst({
  cacheName: 'webpage'
}))

const stylesRoute = new workbox.routing.Route(({ request }) => {
  return request.destination === 'style';
}, new workbox.strategies.NetworkFirst({
  cacheName: 'styles'
}));

const javascriptRoute = new workbox.routing.Route(({ request }) => {
  return request.destination === 'script';
}, new workbox.strategies.NetworkFirst({
  cacheName: 'script'
}));

workbox.routing.registerRoute(NaviRoute)
workbox.routing.registerRoute(javascriptRoute);
workbox.routing.registerRoute(stylesRoute);

const cacheKey = 'LockerCache_v1'

self.addEventListener('install',(event) =>{
    event.waitUntil(caches.open(cacheKey).then((cache)=>{
        return cache.addAll([
            '/static/manage_locker_offline.html',
            '/static/materialize.css',
            '/static/materialize.js',
            '/static/util.js',
            '/static/style.css',
            '/static/autocomplete.js'
        ])
    })
)})

self.addEventListener('fetch', (event) => {
    // Check if this is a navigation request
    if (event.request.mode === 'navigate') {
      // Open the cache
      event.respondWith(caches.open(cacheKey).then((cache) => {
        // Go to the network first
        return fetch(event.request.url).then((fetchedResponse) => {
          cache.put(event.request, fetchedResponse.clone());
  
          return fetchedResponse;
        }).catch(() => {
          // If the network is unavailable, get
          return cache.match(event.request.url);
        });
      }));
    } else {
      return;
    }
  });