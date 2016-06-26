import json, requests

url = 'http://94.76.229.155:90'
headers = {'Content-Type': 'application/json'}
params = {'username': 'admin', 'password': 'admin'}

def alignak_backend_auth():

    # Token
    response = requests.post(url + '/login', json=params, headers=headers)
    resp = response.json()
    token = resp['token']

    # Basic auth
    backend_auth = requests.auth.HTTPBasicAuth(token, '')
    return backend_auth

def get_host_state(authentication):
    # get hosts
    hosts = requests.get(
        url + '/livestate?where={"type":"host"}',
        auth=authentication
    )
    s = hosts.json()

    data = {}
    for host in s['_items']:
        data[host['name']] = host['state']
    return data

if __name__ == "__main__":
    auth = alignak_backend_auth()
    data = get_host_state(auth)

    print(data)