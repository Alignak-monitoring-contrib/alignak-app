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
from PyQt5.Qt import QApplication, QTimer

from alignak_app.utils.config import settings
from alignak_app.items.livesynthesis import LiveSynthesis

from alignak_app.locales.locales import init_localization

from alignak_app.qobjects.dock.livestate import LivestateQWidget


class TestLivestateQWidget(unittest2.TestCase):
    """
        This file test the LivestateQWidget class.
    """

    settings.init_config()
    init_localization()

    # Synthesis data test
    synthesis_data = [
        {
            'hosts_total': 2, 'hosts_unreachable_hard': 0, '_id': '59c4e40635d17b8e0c6accaf',
            '_etag': '809a1cf43eaf858de1ef48df38ced9bb5875a3c8', 'services_business_impact': 0,
            'hosts_down_hard': 1, 'hosts_in_downtime': 0, 'services_unreachable_soft': 0,
            'services_unreachable_hard': 8, 'services_warning_hard': 0, 'hosts_up_hard': 0,
            'services_unknown_soft': 0, 'services_acknowledged': 4, 'services_ok_soft': 0,
            'hosts_business_impact': 0, 'hosts_acknowledged': 1,
            '_realm': '59c4e40435d17b8e0c6acc60',
            '_created': 'Thu, 01 Jan 1970 00:00:00 GMT', 'hosts_unreachable_soft': 0,
            'services_in_downtime': 0, '_updated': 'Thu, 01 Jan 1970 00:00:00 GMT',
            'services_ok_hard': 1, 'services_total': 14, 'services_critical_soft': 0,
            'services_warning_soft': 0, 'hosts_down_soft': 0, 'hosts_up_soft': 0,
            'services_critical_hard': 0, 'hosts_flapping': 0, 'services_flapping': 0,
            'services_unknown_hard': 1},
        {
            'hosts_total': 34, 'hosts_unreachable_hard': 0, '_id': '59c4e40635d17b8e0c6accb0',
            '_etag': '6999aaa6d1b8ebe867f2f6d55c01a7dc71330f73', 'services_business_impact': 0,
            'hosts_down_hard': 7, 'hosts_in_downtime': 0, 'services_unreachable_soft': 0,
            'services_unreachable_hard': 71, 'services_warning_hard': 3, 'hosts_up_hard': 39,
            'services_unknown_soft': 0, 'services_acknowledged': 76, 'services_ok_soft': 0,
            'hosts_business_impact': 0, 'hosts_acknowledged': 2,
            '_realm': '59c4e38535d17b8dcb0bed42',
            '_created': 'Thu, 01 Jan 1970 00:00:00 GMT', 'hosts_unreachable_soft': 0,
            'services_in_downtime': 0, '_updated': 'Fri, 22 Sep 2017 10:20:54 GMT',
            'services_ok_hard': 209, 'services_total': 404, 'services_critical_soft': 1,
            'services_warning_soft': 0, 'hosts_down_soft': 0, 'hosts_up_soft': 0,
            'services_critical_hard': 26, 'hosts_flapping': 0, 'services_flapping': 0,
            'services_unknown_hard': 18}
    ]
    livesynth_list = []
    for data in synthesis_data:
        livesynth = LiveSynthesis()
        livesynth.create(data['_id'], data)
        livesynth_list.append(livesynth)

    @classmethod
    def setUpClass(cls):
        """Create QApplication"""
        try:
            cls.app = QApplication(sys.argv)
        except Exception as e:
            print(e)
            pass

    def test_create_livestate_widget(self):
        """Inititalize LivestateQWidget"""

        under_test = LivestateQWidget()

        self.assertIsInstance(under_test.timer, QTimer)

        self.assertTrue('host' in under_test.labels)
        self.assertTrue('problem' in under_test.labels)
        self.assertTrue('service' in under_test.labels)

        for label_grp in under_test.labels:
            self.assertIsNone(under_test.labels[label_grp])

        under_test.initialize()

        for label_grp in under_test.labels:
            self.assertTrue('problem' in under_test.labels[label_grp])
            self.assertTrue('total' in under_test.labels[label_grp])
            self.assertTrue('icon' in under_test.labels[label_grp])

    def test_update_livestate_labels(self):
        """Update LivestateQWidget QLabels"""

        # No problems in datamanager
        from alignak_app.backend.datamanager import data_manager
        data_manager.database['livesynthesis'] = []
        self.assertFalse(data_manager.database['livesynthesis'])

        under_test = LivestateQWidget()
        under_test.initialize()

        for label_grp in under_test.labels:
            self.assertEqual('ok', under_test.labels[label_grp]['problem'].objectName())

        data_manager.update_database('livesynthesis', self.livesynth_list)

        under_test.update_labels()

        # QLabels for 'host' and 'service' should change to 'ko'
        for label_grp in under_test.labels:
            self.assertEqual('ko', under_test.labels[label_grp]['problem'].objectName())
