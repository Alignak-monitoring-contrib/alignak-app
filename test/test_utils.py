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

from alignak_app.core.utils.config import get_url_endpoint_from_icon_name


class TestUtils(unittest2.TestCase):
    """
        This file test methods of `utils.py` file.
    """

    # def test_init_config(self):
    #     """Set and Get app_config"""
    #
    #     # Reset app_config to None
    #     settings.app_config = None
    #
    #     self.assertIsNone(settings.app_config)
    #
    #     settings.init_config()
    #
    #     self.assertIsNotNone(settings.app_config)
    #
    # def test_set_get_app_config(self):
    #     """Set and Get app_config"""
    #
    #     # Reset and Init "app_config"
    #     settings.app_config = configparser.ConfigParser(os.environ)
    #     self.assertIsNone(settings.app_config)
    #     settings.init_config()
    #
    #     # Get current url
    #     under_test = settings.get_config('Alignak', 'url')
    #     self.assertEqual('http://demo.alignak.net', under_test)
    #
    #     # Change url
    #     settings.edit_setting_value('Alignak', 'url', 'http://127.0.0.1')
    #     new_under_test = settings.get_config('Alignak', 'url')
    #     self.assertEqual('http://127.0.0.1', new_under_test)
    #
    #     # Back url to normal
    #     settings.edit_setting_value('Alignak', 'url', 'http://demo.alignak.net')
    #     last_under_test = settings.get_config('Alignak', 'url')
    #
    #     self.assertEqual('http://demo.alignak.net', last_under_test)
    #
    # def test_reload_config(self):
    #     """Reload Configuration"""
    #
    #     # Reset and Init "app_config"
    #     settings.app_config = configparser.ConfigParser(os.environ)
    #     self.assertIsNone(settings.app_config)
    #     settings.init_config()
    #
    #     cur_config = settings.app_config
    #
    #     settings.init_config()
    #
    #     new_config = settings.app_config
    #
    #     self.assertFalse(cur_config is new_config)
    #     self.assertTrue(settings.app_config is new_config)

    def test_get_url_endpoint_from_icon_name(self):
        """get Url Endpoint from Icon Name"""

        under_test = get_url_endpoint_from_icon_name('services_ok')

        self.assertEqual('/table?search=ls_state:OK', under_test)

        under_test = get_url_endpoint_from_icon_name('unknown_icon')

        self.assertEqual('/table', under_test)
