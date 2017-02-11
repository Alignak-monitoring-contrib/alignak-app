#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2017:
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

import os

import unittest2

import alignak_app.core.utils as utils


class TestUtils(unittest2.TestCase):
    """
        This file test methods of `utils.py` file.
    """

    def test_get_app_root(self):
        """Get Alignak-App Root Folder"""

        expected_home = os.environ['HOME'] + '/.local'

        home = utils.get_app_root()

        self.assertEqual(home, expected_home)

    def test_app_config(self):
        """Set and Get app_config"""

        # Reset app_config to None
        utils.app_config = None

        self.assertIsNone(utils.app_config)

        utils.init_config()

        self.assertIsNotNone(utils.app_config)

    def test_set_app_config(self):
        """Reload config"""

        # Reset and Init "app_config"
        utils.app_config = None
        self.assertIsNone(utils.app_config)
        utils.init_config()

        # Get current url
        under_test = utils.get_app_config('Alignak', 'url')
        self.assertEqual('http://demo.alignak.net', under_test)

        # Change url
        utils.set_app_config('Alignak', 'url', 'http://127.0.0.1')
        new_under_test = utils.get_app_config('Alignak', 'url')
        self.assertEqual('http://127.0.0.1', new_under_test)

        # Back url to normal
        utils.set_app_config('Alignak', 'url', 'http://demo.alignak.net')
        last_under_test = utils.get_app_config('Alignak', 'url')

        self.assertEqual('http://demo.alignak.net', last_under_test)

    def test_reload_config(self):
        """Reload Configuration"""

        # Reset and Init "app_config"
        utils.app_config = None
        self.assertIsNone(utils.app_config)
        utils.init_config()

        cur_config = utils.app_config

        utils.init_config()

        new_config = utils.app_config

        self.assertFalse(cur_config is new_config)
        self.assertTrue(utils.app_config is new_config)

    def test_get_image_path(self):
        """Get Right Image Path"""
        utils.init_config()

        expected_img = utils.get_app_root() + '/alignak_app/images/icon.svg'

        under_test = utils.get_image_path('icon')

        self.assertEqual(under_test, expected_img)
