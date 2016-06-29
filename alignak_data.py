from alignak_backend_client.client import Backend

def login_backend(Config):
    # Credentials
    username = Config.get('Backend', 'username')
    password = Config.get('Backend', 'password')

    # Backend login
    backend_url = Config.get('Backend', 'backend_url')
    backend = Backend(backend_url)
    backend.login(username, password)

    return backend

def get_host_state(backend):
    # Request
    all_host = backend.get_all(backend.url_endpoint_root + '/livestate?where={"type":"host"}')

    # Store Data
    current_hosts = {}
    for host in all_host['_items']:
        current_hosts[host['name']] = host['state']
        print(host['name'], '->', host['state'])

    return current_hosts

def get_service_state(backend):
    # Request
    all_services = backend.get_all(backend.url_endpoint_root + '/livestate?where={"type":"service"}')

    # Store Data
    current_services = {}
    for service in all_services['_items']:
        current_services[service['name']] = service['state']
        print(service['name'], '->', service['state'])

    return current_services
