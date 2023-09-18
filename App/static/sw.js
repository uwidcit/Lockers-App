// https://developer.chrome.com/docs/workbox/modules/workbox-sw/

importScripts(
  'https://storage.googleapis.com/workbox-cdn/releases/7.0.0/workbox-sw.js'
);

self.skipWaiting()

const {offlineFallback} = workbox.recipes;
const {BackgroundSyncPlugin,Queue} = workbox.backgroundSync;
const {registerRoute,setDefaultHandler} = workbox.routing;
const {CacheFirst, StaleWhileRevalidate, NetworkOnly,NetworkFirst} = workbox.strategies;
const {precacheAndRoute} = workbox.precaching;
const {CacheableResponse, CacheableResponsePlugin} = workbox.cacheableResponse;

precacheAndRoute([ { url: '/locker', revision: null }, ...[{"revision":"bc56a6869ac03cd8815461a8a58ca256","url":"autocomplete.js"},{"revision":"9d295ec8b213fdfaac1595e739a950ef","url":"keep_alive.js"},{"revision":"a541907cc008b72fd31ac8895bfbc3eb","url":"lockers.js"},{"revision":"870b5ea4295065881458d40c6df53a78","url":"main.js"},{"revision":"a9f21e821e64f385b3f330d3b0a19845","url":"manage_locker_offline.html"},{"revision":"5c939ef677a57602e5e12eaa34058ead","url":"map_init.js"},{"revision":"b0663391a6dd5efed956259f29fa18dd","url":"materialize.css"},{"revision":"74ac8fd1cd0b94f532c54d4c707a86ae","url":"materialize.js"},{"revision":"ec1df3ba49973dcb9ff212f052d39483","url":"materialize.min.css"},{"revision":"5dcfc8944ed380b2215dc28b3f13835f","url":"materialize.min.js"},{"revision":"b7a97dc36dffb61a3b3e165b9dbe20d2","url":"offline.html"},{"revision":"7a2b4050bd5b0159ba5101b00d60b40f","url":"static-user.html"},{"revision":"ceac046cad1656146e8d521968b87cda","url":"style.css"},{"revision":"1d8179f18fcc6c658c386f9f30ef126b","url":"util.js"},{"revision":"2cd1cbbe5f9d94f135c89263d2eb4d2b","url":"workbox-a482575e.js"}]]);

setDefaultHandler(new NetworkFirst());

offlineFallback();

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

// Log all network requests
self.addEventListener('fetch', (event) => {
  console.log('SW: Fetching', event.request.url);
  // You can also log other request details like event.request.method, event.request.headers, etc.

  // Pass through the fetch request
  event.respondWith(fetch(event.request));
});

const bgSyncPlugin = new BackgroundSyncPlugin('LockersQueue',{
  maxRetentionTime:48 *60,
  onSync: customReplay,
  forceSyncFallback:true,

})

async function customReplay(){
  let entry;
  while ((entry = await this.shiftRequest())){
    try{
      const response = await fetch(entry.request.clone())
    }
    catch (error){
      await this.unshiftRequest(entry)
      throw new Error ('Cannot connect to server')
    }
  }
}

const statusPlugin = {
  fetchDidSucceed: ({response}) =>{
    console.log(response)
    if (response.status >= 500){
      throw new Error('Server error.')
    }
    return response
  }
}

registerRoute(
  new RegExp('\/api/*'),
  new NetworkOnly({
    plugins:[
      statusPlugin,
      bgSyncPlugin,
    ]
  }),
  'POST'
  )

registerRoute(
  new RegExp('\/api/*'),
  new NetworkFirst({
    cacheName: 'api-cache',
    networkTimeoutSeconds: 8,
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
);

registerRoute(
  new RegExp('\/static/*'),
  new StaleWhileRevalidate()
);

registerRoute(
  new RegExp('\/locker'),
  new NetworkFirst()
);

registerRoute(
  new RegExp('https://code.jquery.com/jquery-3.7.0.min.js'),
  new CacheFirst({
    cacheName: 'lockers-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
);

registerRoute(
  new RegExp('https://cdn.datatables.net/1.13.4/js/jquery.dataTables.js'),
  new CacheFirst({
    cacheName: 'lockers-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
);

registerRoute(
  new RegExp('https://cdn.datatables.net/1.13.4/js/jquery.dataTables.js'),
  new CacheFirst({
    cacheName: 'lockers-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
);

registerRoute(
  new RegExp('https://cdn.datatables.net/select/1.6.2/js/dataTables.select.min.js'),
  new CacheFirst({
    cacheName: 'lockers-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
);

registerRoute(
  new RegExp('https://fonts.googleapis.com/*'),
  new CacheFirst({
    cacheName: 'lockers-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
)

registerRoute(
  new RegExp('https://fonts.gstatic.com/*'),
  new CacheFirst({
    cacheName: 'lockers-cache',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200]
      })
    ]
  })
)