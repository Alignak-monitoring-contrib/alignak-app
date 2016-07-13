#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
#   Matthieu Estrada, ttamalfor@gmail.com
#
# This file is part of (AlignakApp).
#
# (AlignakApp) is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# (AlignakApp) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with (AlignakApp).  If not, see <http://www.gnu.org/licenses/>.

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
        self.backend = None

    def log_to_backend(self, config):
        # Credentials
        username = config.get('Backend', 'username')
        password = config.get('Backend', 'password')

        # Backend login
        backend_url = config.get('Backend', 'backend_url')
        self.backend = Backend(backend_url)
        self.backend.login(username, password)

    def get_host_state(self):
        # Request
        all_host = self.backend.get_all(self.backend.url_endpoint_root +
                                        '/livestate?where={"type":"host"}')
        # Store Data
        for host in all_host['_items']:
            self.current_hosts[host['name']] = host['state']
        return self.current_hosts

    def get_service_state(self):
        # Request
        all_services = self.backend.get_all(self.backend.url_endpoint_root +
                                            '/livestate?where={"type":"service"}')

        # Store Data
        for service in all_services['_items']:
            self.current_services[service['name']] = service['state']
        return self.current_services
