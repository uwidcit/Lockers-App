importScripts('/static/wb/workbox-v7.0.0/workbox-sw.js')

workbox.setConfig({
    modulePathPrefix:'/static/wb/workbox-v7.0.0/',
    debug:true,
})

workbox.loadModule('workbox-routing')
workbox.loadModule('workbox-strategies');
workbox.loadModule('workbox-precaching')


const {NetworkFirst} = workbox.strategies
const {NavigationRoute, Route, registerRoute} = workbox.routing
const {precacheAndRoute} = workbox.precaching

precacheAndRoute(self.__WB_MANIFEST);


const NaviRoute = new NavigationRoute(
    new NetworkFirst({
    cacheName: 'webpage'
  }));
  
  const stylesRoute = new Route(({ request }) => {
    return request.destination === 'style';
  }, new NetworkFirst({
    cacheName: 'styles'
  }));
  
  const javascriptRoute = new Route(({ request }) => {
    return request.destination === 'script';
  }, new NetworkFirst({
    cacheName: 'script'
  }));
  
  registerRoute(NaviRoute)
  registerRoute(javascriptRoute);
  registerRoute(stylesRoute);
  
  const cacheKey = 'LockerCache_v1'
  
  self.addEventListener('install',(event) =>{
      event.waitUntil(caches.open(cacheKey).then((cache)=>{
          return cache.addAll([
              '/static/manage_locker_offline.html',
              '/static/materialize.css',
              '/static/materialize.js',
              '/static/util.js',
              '/static/style.css',
              '/static/autocomplete.js',
              'https://code.jquery.com/jquery-3.7.0.min.js',
              'https://cdn.datatables.net/1.13.4/js/jquery.dataTables.js',
              'https://cdn.datatables.net/1.13.4/css/jquery.dataTables.css',
              '/api/locker',
              '/api/area',
              '/api/student/available'
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