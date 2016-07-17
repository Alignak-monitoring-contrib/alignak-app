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

import unittest2
import configparser as cfg

from alignak_app.alignak_data import AlignakData

class TestAlignakData(unittest2.TestCase):
    """
        This file test methods of AlignakData class
    """

    def test_connection(self):
        under_test = AlignakData()

        config = cfg.ConfigParser()
        config.read('etc/settings.cfg')

        under_test.log_to_backend(config)

        # Compare config url and backend
        self.assertEquals(under_test.backend.url_endpoint_root, config.get('Backend', 'backend_url'))
        # Test if all is empty
        self.assertFalse(under_test.current_hosts)
        self.assertFalse(under_test.current_services)

    def test_if_hosts_and_services(self):
        under_test = AlignakData()

        config = cfg.ConfigParser()
        config.read('etc/settings.cfg')

        under_test.log_to_backend(config)

        self.assertTrue(under_test.get_host_state())
        self.assertTrue(under_test.get_service_state())
