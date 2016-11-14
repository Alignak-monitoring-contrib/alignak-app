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

import alignak_app.utils as utils


class TestUtils(unittest2.TestCase):
    """
        This file test methods of `utils.py` file.
    """

    def test_get_template(self):
        """Get a Template"""

        # Simulate an expected Template
        expected_css = """QWidget{
    Background: #eee;
    color:white;
}
QLabel#title{
    Background: #78909C;
    border: none;
    border-radius: 10px;
    font-size: 18px bold;
}
QLabel#msg{
    Background: #eee;
    color: black;
}
QLabel#state{
    Background-color: #27ae60;
    font-size: 16px bold;

}
QToolButton{
    Background: #eee;
    border: none;
}
"""

        # Initialize config
        utils.set_app_config()

        # Get the template
        under_test = utils.get_template('css.tpl', dict(color_title='#27ae60'))

        self.assertEqual(under_test, expected_css)

    def test_get_alignak_home(self):
        """Get Alignak-App Home"""

        expected_home = os.environ['HOME'] + '/.local'

        home = utils.get_alignak_home()

        self.assertEqual(home, expected_home)

    def test_app_config(self):
        """Set and Get app_config"""

        # Reset app_config to None
        utils.app_config = None
        under_test = utils.get_app_config()

        self.assertIsNone(under_test)
        self.assertIsNone(utils.app_config)

        utils.set_app_config()

        under_test = utils.get_app_config()
        self.assertIsNotNone(under_test)
        self.assertIsNotNone(utils.app_config)

    def test_get_image(self):
        """Get image"""
        utils.set_app_config()

        expected_img = utils.get_alignak_home() + '/' + utils.__pkg_name__ + '/images/alignak.svg'

        under_test = utils.get_image('icon')

        self.assertEqual(under_test, expected_img)
