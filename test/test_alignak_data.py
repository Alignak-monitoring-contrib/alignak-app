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

from alignak_app.backend.alignak_data import AlignakData
from alignak_app.core.utils import set_app_config, get_app_config


class TestAlignakData(unittest2.TestCase):
    """
        This file test methods of AlignakData class
    """

    # Create config for all methods.
    set_app_config()

    def test_log_to_backend(self):
        """Connection to Alignak-Backend"""

        under_test = AlignakData()

        under_test.log_to_backend()

        # Compare config url and backend
        self.assertEquals(
            under_test.backend.url_endpoint_root,
            get_app_config('Backend', 'backend_url')
        )
        self.assertTrue(under_test.backend.authenticated)

    def test_if_hosts_states(self):
        """Collect Hosts States"""

        alignak_data = AlignakData()

        alignak_data.log_to_backend()

        # Get hosts states
        under_test = alignak_data.get_host_states()

        self.assertTrue(under_test)

    def test_if_services_states(self):
        """Collect Services States"""

        alignak_data = AlignakData()

        alignak_data.log_to_backend()

        # Get services states
        under_test = alignak_data.get_service_states()

        self.assertTrue(under_test)
