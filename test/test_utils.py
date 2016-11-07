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
import configparser

from alignak_app.utils import *


class TestUtils(unittest2.TestCase):
    """
        This file test methods of `utils.py` file.
    """

    # Simulate config file
    config_file = get_alignak_home() + '/alignak_app/settings.cfg'
    config = configparser.ConfigParser()
    config.read(config_file)

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



        # Get the template
        under_test = get_template('css.tpl', dict(color_title='#27ae60'), TestUtils.config)

        self.assertEqual(under_test, expected_css)

    def test_get_alignak_home(self):
        """Get Alignak-App Home"""

        expected_home = os.environ['HOME'] + '/.local'

        home = get_alignak_home()

        self.assertEqual(home, expected_home)

