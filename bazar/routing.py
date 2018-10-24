from channels.routing import route

from core.consumers import ws_connect,ws_disconnect, request_saved

channel_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect),
    route("request-saved", request_saved),
]