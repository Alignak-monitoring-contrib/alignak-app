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

import os
import unittest2
import configparser

from alignak_app.core.utils.config import get_url_endpoint_from_icon_name, Settings


class TestUtils(unittest2.TestCase):
    """
        This file test methods of `utils.py` file.
    """

    def test_init_config(self):
        """Init Settings"""

        under_test = Settings()

        self.assertIsInstance(under_test.app_config, configparser.ConfigParser)
        self.assertIsInstance(under_test.img_config, configparser.ConfigParser)
        self.assertTrue('settings' in under_test.settings)
        self.assertTrue('images' in under_test.settings)
        self.assertIsNone(under_test.app_cfg_dir)
        self.assertIsNone(under_test.user_cfg_dir)
        self.assertIsNone(under_test.css_style)

        under_test.init_config()

        self.assertIsInstance(under_test.app_config, configparser.ConfigParser)
        self.assertIsInstance(under_test.img_config, configparser.ConfigParser)
        self.assertTrue('settings' in under_test.settings)
        self.assertTrue('images' in under_test.settings)
        self.assertIsNotNone(under_test.app_cfg_dir)
        self.assertIsNotNone(under_test.user_cfg_dir)
        self.assertIsNone(under_test.css_style)

    def test_app_dir_from_env(self):
        """App Workdir from Env"""

        under_test = Settings()
        under_test.init_config()

        self.assertEqual('%s/.local/alignak_app' % os.environ['HOME'], under_test.user_cfg_dir)

        os.environ['ALIGNAKAPP_USER_CFG'] = '/tmp/alignak_app'
        os.environ['ALIGNAKAPP_APP_CFG'] = '/tmp/alignak_app/settings'

        under_test.init_config()

        self.assertEqual('/tmp/alignak_app', under_test.user_cfg_dir)
        self.assertEqual('/tmp/alignak_app/settings', under_test.app_cfg_dir)

        # Reset env var for other tests
        os.environ['ALIGNAKAPP_USER_CFG'] = ''
        os.environ['ALIGNAKAPP_APP_CFG'] = ''

    def test_set_app_config(self):
        """Set and Get app_config"""

        under_test = Settings()
        under_test.init_config()

        # Get current url
        url_test = under_test.get_config('Alignak', 'url')
        self.assertEqual('http://demo.alignak.net', url_test)

        # Change url
        under_test.edit_setting_value('Alignak', 'url', 'http://127.0.0.1')
        new_url_test = under_test.get_config('Alignak', 'url')
        self.assertEqual('http://127.0.0.1', new_url_test)

        # Back url to normal
        under_test.edit_setting_value('Alignak', 'url', 'http://demo.alignak.net')
        last_url_test = under_test.get_config('Alignak', 'url')

        self.assertEqual('http://demo.alignak.net', last_url_test)

        bool_test = under_test.get_config('Log', 'debug', boolean=True)

        self.assertIsInstance(bool_test, bool)

    def test_get_image(self):
        """Get Image"""

        under_test = Settings()
        under_test.init_config()

        test_icon = under_test.get_image('icon')

        self.assertEqual('%s/.local/alignak_app/images/icon.svg' % os.environ['HOME'], test_icon)

        test_icon_error = under_test.get_image('NONE')

        self.assertEqual(
            '%s/.local/alignak_app/images/error.svg' % os.environ['HOME'], test_icon_error
        )

    def test_init_css(self):
        """Init CSS"""

        under_test = Settings()
        under_test.init_config()

        self.assertIsNone(under_test.css_style)

        under_test.init_css()

        self.assertIsNotNone(under_test.css_style)
        self.assertIsInstance(under_test.css_style, str)

        # Set 'ALIGNAKAPP_APP_CFG' and init again config
        os.environ['ALIGNAKAPP_APP_CFG'] = '/tmp/alignak_app'
        under_test.init_config()

        under_test.init_css()

        self.assertEqual('', under_test.css_style)

        # Reset env var for other tests
        os.environ['ALIGNAKAPP_APP_CFG'] = ''

    def test_get_url_endpoint_from_icon_name(self):
        """Get Url Endpoint from Icon Name"""

        under_test = get_url_endpoint_from_icon_name('services_ok')

        self.assertEqual('/table?search=ls_state:OK', under_test)

        under_test = get_url_endpoint_from_icon_name('unknown_icon')

        self.assertEqual('/table', under_test)
