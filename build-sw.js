importScripts('/static/wb/workbox-v7.0.0/workbox-sw.js')

const {precacheAndRoute} = workbox.precaching

precacheAndRoute(self.__WB_MANIFEST);