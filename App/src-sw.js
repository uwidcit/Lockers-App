importScripts('/static/workbox-v7.0.0/workbox-sw.js')

workbox.setConfig({
    debug:true,
    modulePathPrefix: '/static/workbox-v7.0.0/'
})

const {precacheAndRoute} = workbox.precaching 

precacheAndRoute(self.__WB_MANIFEST)

