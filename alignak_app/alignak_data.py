#!/usr/bin/env python
# -*- coding: utf-8 -*-

from alignak_backend_client.client import Backend
import future

class AlignakData(object):
    """
        Alignak Bridge

        This class collect informations with Backend-Client and return essential things for
        Alignak-App.
    """

    def __init__(self):
        self.current_hosts = {}
        self.current_services = {}
        self.username = ''
        self.backend = None

    def log_to_backend(self, Config):
        # Credentials
        self.username = Config.get('Backend', 'username')
        password = Config.get('Backend', 'password')

        # Backend login
        backend_url = Config.get('Backend', 'backend_url')
        self.backend = Backend(backend_url)
        self.backend.login(self.username, password)

    def get_host_state(self):
        # Request
        all_host = self.backend.get_all(self.backend.url_endpoint_root + '/livestate?where={"type":"host"}')

        # Store Data
        for host in all_host['_items']:
            self.current_hosts[host['name']] = host['state']
        return self.current_hosts

    def get_service_state(self):
        # Request
        all_services = self.backend.get_all(self.backend.url_endpoint_root + '/livestate?where={"type":"service"}')

        # Store Data
        for service in all_services['_items']:
            self.current_services[service['name']] = service['state']
        return self.current_services
