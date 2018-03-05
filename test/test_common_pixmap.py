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

import sys

import unittest2
from PyQt5.Qt import QApplication, QPixmap

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.labels import get_icon_pixmap, get_icon_item

settings.init_config()


class TestCommonQPixmap(unittest2.TestCase):
    """
        This file test the Common QPixmap funtions
    """

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_get_icon_item(self):
        """Get Icon Item"""

        item_types = ['host', 'service', 'problem']
        under_test = None

        i = -3
        for item in item_types:
            under_test = get_icon_item(item, i)
            i += 1

        self.assertIsInstance(under_test, QPixmap)

    def test_get_icon_pixmap(self):
        """Get Icon Pixmap"""

        under_test_true = get_icon_pixmap(True, ['first', 'second'])
        under_test_false = get_icon_pixmap(False, ['first', 'second'])

        self.assertIsInstance(under_test_true, QPixmap)
        self.assertIsInstance(under_test_false, QPixmap)
