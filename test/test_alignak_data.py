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
import os
import configparser as cfg

from alignak_app.alignak_data import AlignakData
from alignak_app.app import get_alignak_home


class TestAlignakData(unittest2.TestCase):
    """
        This file test methods of AlignakData class
    """

    filepath = get_alignak_home() + '/alignak_app/settings.cfg'
    config = cfg.ConfigParser()
    config.read(filepath)

    def test_connection(self):
        under_test = AlignakData()

        under_test.log_to_backend(TestAlignakData.config)

        # Compare config url and backend
        self.assertEquals(
            under_test.backend.url_endpoint_root,
            TestAlignakData.config.get('Backend', 'backend_url')
        )

    def test_if_hosts_states(self):
        alignak_data = AlignakData()

        alignak_data.log_to_backend(TestAlignakData.config)

        under_test = alignak_data.get_host_states()

        self.assertTrue(alignak_data.backend.authenticated)
        self.assertTrue(under_test)

    def test_if_services_states(self):
        alignak_data = AlignakData()

        alignak_data.log_to_backend(TestAlignakData.config)

        under_test = alignak_data.get_service_states()

        self.assertTrue(alignak_data.backend.authenticated)
        self.assertTrue(under_test)
