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

from alignak_app.application import AlignakApp
from alignak_app.alignak_data import AlignakData

class TestApplication(unittest2.TestCase):
    """
        This file test methods of AlignakApp class.
    """

    def test_main(self):
        under_test = AlignakApp()

        self.assertIsNone(under_test.config)
        self.assertIsNone(under_test.backend_data)
        self.assertIsNone(under_test.indicator)

        config = cfg.ConfigParser()
        config.read('./etc/settings.cfg')
        under_test.config = config

        under_test.main()

        self.assertIsNotNone(under_test.config)
        self.assertIsNotNone(under_test.backend_data)

    def test_get_state(self):
        under_test = AlignakApp()

        config = cfg.ConfigParser()
        config.read('./etc/settings.cfg')
        under_test.config = config

        under_test.backend_data = AlignakData()
        under_test.backend_data.log_to_backend(under_test.config)

        # UP and DOWN must be Integer and positive
        hosts_states, services_states = under_test.get_state()

        self.assertIsInstance(hosts_states['up'], int)
        self.assertIsInstance(hosts_states['down'], int)
        self.assertIsInstance(hosts_states['unreachable'], int)
        self.assertGreater(hosts_states['up'], -1)
        self.assertGreater(hosts_states['down'], -1)
        self.assertGreater(hosts_states['unreachable'], -1)

        self.assertIsInstance(services_states['ok'], int)
        self.assertIsInstance(services_states['critical'], int)
        self.assertIsInstance(services_states['unknown'], int)
        self.assertIsInstance(services_states['warning'], int)
        self.assertGreater(services_states['ok'], -1)
        self.assertGreater(services_states['critical'], -1)
        self.assertGreater(services_states['unknown'], -1)
        self.assertGreater(services_states['warning'], -1)



