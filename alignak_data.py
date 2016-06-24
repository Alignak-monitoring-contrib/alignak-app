import json, requests

def get_alignak_data():
    url = 'http://94.76.229.155:90/login'
    params = {'username': 'admin', 'password': 'admin'}

    resp = requests.post(url=url, json=params)
    token = json.loads(resp.text)
    print(token)