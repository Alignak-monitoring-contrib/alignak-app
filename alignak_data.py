import json, requests

url = 'http://94.76.229.155:90'
headers = {'Content-Type': 'application/json'}
params = {'username': 'admin', 'password': 'admin'}

def alignak_backend_data():

    # Token
    response = requests.post(url + '/login', json=params, headers=headers)
    resp = response.json()
    token = resp['token']

    # Basic auth
    auth = requests.auth.HTTPBasicAuth(token, '')

    # get hosts
    hosts = requests.get(
        url + '/livestate?where={"type":"host"}',
        auth=auth
    )
    s = hosts.json()

    data = {}
    for host in s['_items']:
        data[host['name']] = host['state']

    print(data)

def get_alignak_service():
    alignak_backend_data()



if __name__ == "__main__":
    get_alignak_service()