import requests

headers = {'Content-Type': 'application/json'}

def alignak_backend_auth(Config):
    # Credentials
    username = Config.get('Backend', 'username')
    password = Config.get('Backend', 'password')
    params = {
        'username': username,
        'password': password
    }

    # Token
    backend_url = Config.get('Backend', 'backend_url')
    response = requests.post(backend_url + '/login', json=params, headers=headers)
    resp = response.json()
    token = resp['token']

    # Basic auth
    backend_auth = requests.auth.HTTPBasicAuth(token, '')

    return backend_auth

def get_host_state(authentication, Config):
    # Request
    hosts = requests.get(
        Config.get('Backend', 'backend_url') + '/livestate?where={"type":"host"}',
        auth=authentication
    )
    s = hosts.json()

    # Store Data
    alignak_data = {}
    for host in s['_items']:
        alignak_data[host['name']] = host['state']

    return alignak_data
