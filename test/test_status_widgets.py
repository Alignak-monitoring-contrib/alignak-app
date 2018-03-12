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
from PyQt5.Qt import QApplication, QLabel, QSize

from alignak_app.backend.datamanager import data_manager
from alignak_app.items.daemon import Daemon
from alignak_app.utils.config import settings
from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.alignak.status import StatusQDialog


class TestStatusQDialog(unittest2.TestCase):
    """
        This file test methods of StatusQDialog class object
    """

    settings.init_config()
    init_localization()

    daemons_list = []
    for i in range(0, 10):
        daemon = Daemon()
        daemon.create(
            '_id%d' % i,
            {
                'name': 'daemon%d' % i,
                'alive': True,
                'address': '127.0.0.%d' % i,
                'port': '700%d' % i,
                'reachable': True,
                'spare': True,
                'passive': True,
                'last_check': 100000
            },
            'daemon%d' % i
        )
        daemons_list.append(daemon)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except:
            pass

    def test_initialize_status_qdialog(self):
        """Initialize StatusQDialog"""

        under_test = StatusQDialog()

        self.assertIsNotNone(under_test.app_widget)
        self.assertIsNotNone(under_test.layout)
        self.assertFalse(under_test.labels)

        under_test.initialize()

    def test_set_daemons_labels(self):
        """Set Daemons QLabels"""

        under_test = StatusQDialog()
        labels_test = [
            'alive', 'name', 'reachable', 'spare', 'address', 'passive', 'last_check'
        ]

        daemon_test = Daemon()
        daemon_test.create(
            '_id1',
            {
                'alive': True
            },
            'daemon-name'
        )

        under_test.set_daemons_labels([daemon_test])

        self.assertTrue('daemon-name' in under_test.labels)

        for lbl_test in labels_test:
            self.assertTrue(lbl_test in under_test.labels['daemon-name'])

    def test_add_daemon_titles_labels(self):
        """Add Daemon QLabels"""

        under_test = StatusQDialog()

        daemon_test = Daemon()
        daemon_test.create(
            '_id1',
            {
                'alive': True
            },
            'daemon-name'
        )

        under_test.set_daemons_labels([daemon_test])
        under_test.add_daemon_labels(daemon_test, 2)

        self.assertEqual(QSize(18, 18), under_test.labels['daemon-name']['alive'].size())
        self.assertEqual(QSize(14, 14), under_test.labels['daemon-name']['reachable'].size())
        self.assertEqual(QSize(14, 14), under_test.labels['daemon-name']['spare'].size())
        self.assertEqual(QSize(14, 14), under_test.labels['daemon-name']['passive'].size())

    def test_update_dialog(self):
        """Update Status QDialog"""

        # Fill databse with sample daemons
        data_manager.update_database('alignakdaemon', self.daemons_list)

        # Init widget
        under_test = StatusQDialog()

        # Labels are empty
        self.assertFalse(under_test.labels)

        under_test.initialize()
        under_test.update_dialog()

        # Labels are filled
        i = 0
        for daemon_labels in under_test.labels:
            self.assertTrue('daemon%d' % i in under_test.labels)
            i += 1
            for label in under_test.labels[daemon_labels]:
                self.assertIsInstance(under_test.labels[daemon_labels][label], QLabel)

        daemon_labels = under_test.labels['daemon0']
        self.assertEqual('127.0.0.0:7000', daemon_labels['address'].text())
