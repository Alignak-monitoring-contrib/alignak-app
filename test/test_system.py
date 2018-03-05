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
import configparser

from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.backend.backend import app_backend
from alignak_app.utils.system import *
from alignak_app.backend.datamanager import data_manager

from alignak_app.items.daemon import Daemon
from alignak_app.items.event import Event
from alignak_app.items.history import History
from alignak_app.items.host import Host
from alignak_app.items.item import *
from alignak_app.items.livesynthesis import LiveSynthesis
from alignak_app.items.service import Service
from alignak_app.items.user import User
from alignak_app.items.realm import Realm


class TestSystem(unittest2.TestCase):
    """
        This file test methods of System package
    """

    def test_mkdir(self):
        """Mkdir: create directories"""

        # Create folder with permisson return True
        under_test = mkdir('/tmp/test-app')
        self.assertTrue(under_test)

        # Try to create folder already exists, return True
        under_test = mkdir('/tmp/test-app')
        self.assertTrue(under_test)

        # Cleaning...
        os.rmdir('/tmp/test-app')

        # Create folder with no permisson return False
        under_test = mkdir('/usr/local/test-app')
        self.assertFalse(under_test)

    def test_install_file(self):
        """Install (Copy) Origin and Sample Files"""

        # Assert files are no present
        self.assertFalse(os.path.isfile('/tmp/images.ini'))
        self.assertFalse(os.path.isfile('/tmp/images.ini.sample'))

        install_file('etc', '/tmp', 'images.ini')

        # Assert files are installed
        self.assertTrue(os.path.isfile('/tmp/images.ini'))
        self.assertTrue(os.path.isfile('/tmp/images.ini.sample'))

        # Cleaning
        os.remove('/tmp/images.ini')
        os.remove('/tmp/images.ini.sample')

    def test_read_config_file(self):
        """Read Configuration File"""

        parser_test = configparser.ConfigParser()
        under_test = read_config_file(parser_test, 'etc/settings.cfg')

        # Return filename
        self.assertTrue(under_test)
        self.assertEqual('etc/settings.cfg', under_test)

        # Assert parser have been read
        self.assertTrue(parser_test.sections())
        self.assertEqual(['Alignak', 'Alignak-app', 'Log'], parser_test.sections())

        under_test = read_config_file(parser_test, 'etc/no-settings.cfg')

        # No config file returned
        self.assertIsNone(under_test)
        # Parser have not been mofidied
        self.assertTrue(parser_test.sections())

    def test_file_executable(self):
        """Make File Executable"""

        install_file('etc', '/tmp', 'images.ini')

        filename = '/tmp/images.ini'
        file_executable(filename)

        st = os.stat(filename)
        self.assertTrue(stat.S_IEXEC, st.st_mode)

        # Cleaning
        os.remove(filename)
        os.remove(filename + '.sample')
