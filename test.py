#-----------------------------------------------------------------------------------------------------
# TESTS that node details can be retrieved
#-----------------------------------------------------------------------------------------------------
# import requests

# NODE_ID = "46c34751-96b2-49e5-bfae-b730be5e00a3"
# API_KEY = "1234"
# URL = "https://eee4113f-group-41.online/api/weighing-nodes"

# headers = {
#     "Node-ID": NODE_ID,
#     "Authorization": API_KEY
# }

# # while True:
# resp = requests.get(URL, headers=headers)
# print(resp.status_code)
# print(resp.text)
#-----------------------------------------------------------------------------------------------------




#-----------------------------------------------------------------------------------------------------
# TESTS that weights can be sent
#-----------------------------------------------------------------------------------------------------
import requests

NODE_ID = "46c34751-96b2-49e5-bfae-b730be5e00a3"
API_KEY = "1234"
URL = "https://eee4113f-group-41.online/api/weight-readings"

headers = {
    "Node-ID": NODE_ID,
    "Authorization": API_KEY
}

resp = requests.post(URL, data="9999, [3000, 3000, 3000], 0", headers=headers)
print(resp.status_code)
print(resp.text)
#-----------------------------------------------------------------------------------------------------