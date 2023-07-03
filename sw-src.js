// https://developer.chrome.com/docs/workbox/modules/workbox-sw/

importScripts(
  'https://storage.googleapis.com/workbox-cdn/releases/6.4.1/workbox-sw.js'
);

const {registerRoute} = workbox.routing;
const {CacheFirst} = workbox.strategies;
const {precacheAndRoute} = workbox.precaching;
const {CacheableResponse} = workbox.cacheableResponse;


precacheAndRoute(self.__WB_MANIFEST);


// runtime data caching
registerRoute(
  ({ url }) => url.pathname.startsWith('/locker'),
  new CacheFirst({
    cacheName: 'api',
    plugins: [
      new CacheableResponse({
        statuses: [200],
      }),
    ],
  })
);