import requests
import time

NODE_ID = "46c34751-96b2-49e5-bfae-b730be5e00a3"
API_KEY = "1234"
URL = "https://eee4113f-group-41.online/api/weighing-nodes"

headers = {
    "Node-ID": NODE_ID,
    "Authorization": API_KEY
}

# def update_leds(flash):
#     # Replace with real LED control logic
#     print("Flashing LEDs" if flash else "LEDs off")

# while True:
resp = requests.get(URL, headers=headers)
print(resp.status_code)
print(resp.text)
