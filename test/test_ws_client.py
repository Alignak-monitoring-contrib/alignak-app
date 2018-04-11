#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2018:
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

from alignak_app.backend.ws_client import WSClient
from alignak_app.utils.config import settings


class TestWSClient(unittest2.TestCase):
    """
        This file test methods of WSClient class
    """

    # Init config for all methods.
    settings.init_config()

    def test_initialize_ws_client(self):
        """Initialize Web Service"""

        under_test = WSClient()

        self.assertFalse(under_test.token)
        self.assertFalse(under_test.ws_backend)
        self.assertIsNone(under_test.auth)

    def test_login_ws_with_wrong_token(self):
        """Login to WS with Wrong Token"""

        under_test = WSClient()
        under_test.login('wrong_token')

        self.assertFalse(under_test.token)
        self.assertEqual('http://demo.alignak.net:8888', under_test.ws_backend)
        # WS is not auth
        self.assertIsNone(under_test.auth)
