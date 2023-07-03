importScripts('/static/workbox-v7.0.0/workbox-sw.js')

workbox.setConfig({
    debug:true,
    modulePathPrefix: '/static/workbox-v7.0.0/'
})

workbox.loadModule('workbox-strategies')
workbox.loadModule('workbox-precaching')
workbox.loadModule('workbox-routing')

const {precacheAndRoute} = workbox.precaching 
const {registerRoute} = workbox.routing
const {StaleWhileRevalidate,NetworkFirst,CacheFirst} = workbox.strategies

precacheAndRoute([{"revision":"bc56a6869ac03cd8815461a8a58ca256","url":"autocomplete.js"},{"revision":"9d295ec8b213fdfaac1595e739a950ef","url":"keep_alive.js"},{"revision":"4f0283c6ce28e888000e978e537a6a56","url":"leaflet/images/layers-2x.png"},{"revision":"a6137456ed160d7606981aa57c559898","url":"leaflet/images/layers.png"},{"revision":"401d815dc206b8dc1b17cd0e37695975","url":"leaflet/images/marker-icon-2x.png"},{"revision":"2273e3d8ad9264b7daa5bdbf8e6b47f8","url":"leaflet/images/marker-icon.png"},{"revision":"44a526eed258222515aa21eaffd14a96","url":"leaflet/images/marker-shadow.png"},{"revision":"7e29848ca196493b99af2368a37633a9","url":"leaflet/leaflet-src.esm.js"},{"revision":"e2633201d0c94e27be73c45656fe84ad","url":"leaflet/leaflet-src.js"},{"revision":"c02c12fe5e21d2493070649584ca38b7","url":"leaflet/leaflet.css"},{"revision":"f7a3fe98f3eb12ae0e6cff8019a0a672","url":"leaflet/leaflet.js"},{"revision":"313ade5fb9577c96eee71050bf2c59ad","url":"lockers.js"},{"revision":"870b5ea4295065881458d40c6df53a78","url":"main.js"},{"revision":"7ea0c40eeaa95f07fbfe6b744b8cc018","url":"manage_locker_offline.html"},{"revision":"5c939ef677a57602e5e12eaa34058ead","url":"map_init.js"},{"revision":"b0663391a6dd5efed956259f29fa18dd","url":"materialize.css"},{"revision":"74ac8fd1cd0b94f532c54d4c707a86ae","url":"materialize.js"},{"revision":"ec1df3ba49973dcb9ff212f052d39483","url":"materialize.min.css"},{"revision":"5dcfc8944ed380b2215dc28b3f13835f","url":"materialize.min.js"},{"revision":"7a2b4050bd5b0159ba5101b00d60b40f","url":"static-user.html"},{"revision":"ceac046cad1656146e8d521968b87cda","url":"style.css"},{"revision":"1d8179f18fcc6c658c386f9f30ef126b","url":"util.js"},{"revision":"7e66ed8fbc882e6c81c59c30ee151897","url":"workbox-a482575e.js"},{"revision":"b476cd2d6beda8c08ea6e9e42db277a9","url":"workbox-v7.0.0/workbox-background-sync.dev.js"},{"revision":"adcdac0dc6f0b8a46b4ef9198dbaea70","url":"workbox-v7.0.0/workbox-background-sync.prod.js"},{"revision":"0e3f02f0129fc0ea098f0219bfff4d27","url":"workbox-v7.0.0/workbox-broadcast-update.dev.js"},{"revision":"e7d64619f5a7da2cfecbbff5f26b280b","url":"workbox-v7.0.0/workbox-broadcast-update.prod.js"},{"revision":"d518b580c6cff923afe2db3b5a50b3c5","url":"workbox-v7.0.0/workbox-cacheable-response.dev.js"},{"revision":"de20e6d6d8316454ac18dfe0309b389c","url":"workbox-v7.0.0/workbox-cacheable-response.prod.js"},{"revision":"1cce93618bad75160e3234df8268a2e4","url":"workbox-v7.0.0/workbox-core.dev.js"},{"revision":"e7ce12b23585d1c7f4aa5bc922019166","url":"workbox-v7.0.0/workbox-core.prod.js"},{"revision":"580f1168b4041cc1ce41d094ed17e47a","url":"workbox-v7.0.0/workbox-expiration.dev.js"},{"revision":"73d7b64ca94567480a1fc755240e47de","url":"workbox-v7.0.0/workbox-expiration.prod.js"},{"revision":"b42f115e71a5da89daf597a4defb4f47","url":"workbox-v7.0.0/workbox-navigation-preload.dev.js"},{"revision":"51f190da208b5fc6c8da8a9cddb5aeb6","url":"workbox-v7.0.0/workbox-navigation-preload.prod.js"},{"revision":"a30b4268e1c8dc6bbd9afc728ab29f59","url":"workbox-v7.0.0/workbox-offline-ga.dev.js"},{"revision":"85044fbada9c1bc50ea96d4f3ca3f5e1","url":"workbox-v7.0.0/workbox-offline-ga.prod.js"},{"revision":"ece82fb4403a09e7a9a4c10cc2db83c0","url":"workbox-v7.0.0/workbox-precaching.dev.js"},{"revision":"bada902ea96cdb8e930c89ee3e5c6f53","url":"workbox-v7.0.0/workbox-precaching.prod.js"},{"revision":"0f9c77c8ac89283a40c92d01b42fb230","url":"workbox-v7.0.0/workbox-range-requests.dev.js"},{"revision":"5691cae739ccc1efe53af6796874bb8b","url":"workbox-v7.0.0/workbox-range-requests.prod.js"},{"revision":"78e40fd245d40b7062b8db44b61497ab","url":"workbox-v7.0.0/workbox-recipes.dev.js"},{"revision":"14fc689e0322e43ed60355f759af5b2c","url":"workbox-v7.0.0/workbox-recipes.prod.js"},{"revision":"a8b74360cea4695ae1612cce286d1af4","url":"workbox-v7.0.0/workbox-routing.dev.js"},{"revision":"faa4ac9aee7aa6a2e2101ec6156c5200","url":"workbox-v7.0.0/workbox-routing.prod.js"},{"revision":"e1e205c5757510e7c82df7106c8acb86","url":"workbox-v7.0.0/workbox-strategies.dev.js"},{"revision":"d3c70c4022b501e4664608ee90e23f51","url":"workbox-v7.0.0/workbox-strategies.prod.js"},{"revision":"24e1f7221d9e72b59bde3ba1e1c4929e","url":"workbox-v7.0.0/workbox-streams.dev.js"},{"revision":"368b89e2e8a87299c95587305d871bd4","url":"workbox-v7.0.0/workbox-streams.prod.js"},{"revision":"2797e7ee31539d5acc08fc84c8e85df8","url":"workbox-v7.0.0/workbox-sw.js"},{"revision":"95b45d0538e1ed0d621133afbb5c582b","url":"workbox-v7.0.0/workbox-window.dev.es5.mjs"},{"revision":"b21b6e067a6571f517b7b0cb09f70360","url":"workbox-v7.0.0/workbox-window.dev.mjs"},{"revision":"4697cbb636741d0b18b9322406220114","url":"workbox-v7.0.0/workbox-window.dev.umd.js"},{"revision":"ddfc7562051687fe2eb5e9d0565f07e7","url":"workbox-v7.0.0/workbox-window.prod.es5.mjs"},{"revision":"8dc2128f286abcbd5911a4c0bd4ff120","url":"workbox-v7.0.0/workbox-window.prod.mjs"},{"revision":"2fc7482d9bcbb7afff6cfe97b660051e","url":"workbox-v7.0.0/workbox-window.prod.umd.js"}])


registerRoute(
    new RegExp('/api/locker'),
    new StaleWhileRevalidate()
);

registerRoute(
    new RegExp('/api/area'),
    new StaleWhileRevalidate()
);

registerRoute(
    new RegExp('/api/rentType'),
    new StaleWhileRevalidate()
);

registerRoute(
    new RegExp('/api/student/available'),
    new StaleWhileRevalidate()
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


