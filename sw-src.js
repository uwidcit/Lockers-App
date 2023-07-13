// https://developer.chrome.com/docs/workbox/modules/workbox-sw/

importScripts(
  'https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js'
);

const {offlineFallback} = workbox.recipes;
const {BackgroundSyncPlugin,Queue} = workbox.backgroundSync;
const {registerRoute,setDefaultHandler} = workbox.routing;
const {CacheFirst, StaleWhileRevalidate, NetworkOnly,NetworkFirst} = workbox.strategies;
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
  new StaleWhileRevalidate()
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
  new CacheFirst()
);

registerRoute(
  new RegExp('https://cdn.datatables.net/1.13.4/js/jquery.dataTables.js'),
  new CacheFirst()
);

registerRoute(
  new RegExp('https://cdn.datatables.net/1.13.4/js/jquery.dataTables.js'),
  new CacheFirst()
);

registerRoute(
  new RegExp('https://cdn.datatables.net/select/1.6.2/js/dataTables.select.min.js'),
  new CacheFirst()
);