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
from PyQt5.QtWidgets import QApplication

from alignak_app.utils.config import settings

from alignak_app.qobjects.common.frames import AppQFrame


class TestAppQFrame(unittest2.TestCase):
    """
        This file test the AppQFrame class.
    """

    settings.init_config()

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_create_widget(self):
        """Inititalize AppQWidget"""

        under_test = AppQFrame()

        self.assertIsNone(under_test.offset)

        self.assertTrue('app_widget' not in under_test.objectName())
        self.assertTrue('MyTitle' not in under_test.windowTitle())

        under_test.initialize('MyTitle')

        self.assertTrue('app_widget' in under_test.objectName())
        self.assertTrue('MyTitle' in under_test.windowTitle())
