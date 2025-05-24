import threading
from websockets.sync.server import serve
import redis



connected = set()
r = redis.Redis()
pubsub = r.pubsub()
pubsub.subscribe("notifications")

def add_connection(ws):
    connected.add(ws)
    try:
        for _ in ws:
            pass  # ignore incoming messages
    finally:
        connected.remove(ws)


def handle_send_notification_task():
    for message in pubsub.listen():
        if message["type"] == "message":
            notification = message["data"].decode()
            for ws in list(connected):
                try:
                    ws.send(notification)
                except:
                    connected.discard(ws)


def main():
    threading.Thread(target=handle_send_notification_task, daemon=True).start()
    with serve(add_connection, "localhost", 8002) as server:
        server.serve_forever()

if __name__ == "__main__":
    main()
