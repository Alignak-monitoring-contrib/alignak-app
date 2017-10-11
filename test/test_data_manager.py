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

import unittest2

from alignak_app.core.items.item_host import Host
from alignak_app.core.items.item_service import Service
from alignak_app.core.items.item_user import User
from alignak_app.core.items.item_livesynthesis import LiveSynthesis
from alignak_app.core.data_manager import DataManager


class TestDataManager(unittest2.TestCase):
    """
        This file test the DataManager class.
    """

    host_list = []
    for i in range(0, 10):
        host = Host()
        host.create('_id%d' % i, {'name': 'host%d' % i}, 'host%d' % i)
        host_list.append(host)

    service_list = []
    for i in range(0, 10):
        service = Service()
        service.create('_id%d' % i, {'name': 'service%d' % i}, 'service%d' % i)
        service_list.append(service)

    user = User()
    user.create('_id', {'name': 'admin'}, 'admin')

    synthesis_data = [
        {
         'hosts_total': 2, 'hosts_unreachable_hard': 0, '_id': '59c4e40635d17b8e0c6accaf',
         '_etag': '809a1cf43eaf858de1ef48df38ced9bb5875a3c8', 'services_business_impact': 0,
         'hosts_down_hard': 1, 'hosts_in_downtime': 0, 'services_unreachable_soft': 0,
         'services_unreachable_hard': 8, 'services_warning_hard': 0, 'hosts_up_hard': 0,
         'services_unknown_soft': 0, 'services_acknowledged': 4, 'services_ok_soft': 0,
         'hosts_business_impact': 0, 'hosts_acknowledged': 1, '_realm': '59c4e40435d17b8e0c6acc60',
         '_created': 'Thu, 01 Jan 1970 00:00:00 GMT', 'hosts_unreachable_soft': 0,
         'services_in_downtime': 0, '_updated': 'Thu, 01 Jan 1970 00:00:00 GMT',
         'services_ok_hard': 1, 'services_total': 14, 'services_critical_soft': 0,
         'services_warning_soft': 0, 'hosts_down_soft': 0, 'hosts_up_soft': 0,
         'services_critical_hard': 0, 'hosts_flapping': 0, 'services_flapping': 0,
         'services_unknown_hard': 1},
        {
         'hosts_total': 34, 'hosts_unreachable_hard': 0, '_id': '59c4e40635d17b8e0c6accb0',
         '_etag': '6999aaa6d1b8ebe867f2f6d55c01a7dc71330f73', 'services_business_impact': 0,
         'hosts_down_hard': -7, 'hosts_in_downtime': 0, 'services_unreachable_soft': 0,
         'services_unreachable_hard': 71, 'services_warning_hard': 3, 'hosts_up_hard': 39,
         'services_unknown_soft': 0, 'services_acknowledged': 76, 'services_ok_soft': 0,
         'hosts_business_impact': 0, 'hosts_acknowledged': 2, '_realm': '59c4e38535d17b8dcb0bed42',
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

    def test_initialize(self):
        """Initialize DataManager"""

        under_test = DataManager()

        self.assertTrue('history' in under_test.database)
        self.assertTrue('notifications' in under_test.database)
        self.assertTrue('livesynthesis' in under_test.database)
        self.assertTrue('alignakdaemon' in under_test.database)
        self.assertTrue('host' in under_test.database)
        self.assertTrue('service' in under_test.database)
        self.assertTrue('user' in under_test.database)

        self.assertFalse(under_test.old_notifications)
        self.assertFalse(under_test.is_ready())

    def test_update_item_database(self):
        """Update DataManager Database"""

        under_test = DataManager()

        under_test.update_item_database('host', self.host_list)

        # Assert only "host' databse is filled
        self.assertFalse(under_test.database['history'])
        self.assertFalse(under_test.database['notifications'])
        self.assertFalse(under_test.database['livesynthesis'])
        self.assertFalse(under_test.database['alignakdaemon'])
        self.assertFalse(under_test.database['service'])
        self.assertFalse(under_test.database['user'])
        self.assertTrue(under_test.database['host'])

    def test_get_item(self):
        """Get Item from Database"""

        under_test = DataManager()

        under_test.update_item_database('service', self.service_list)

        self.assertTrue(under_test.database['service'])

        # Get item with value
        item = under_test.get_item('service', 'name', 'service2')

        self.assertEqual('service2', item.name)
        self.assertEqual('_id2', item.item_id)
        self.assertEqual('service2', item.data['name'])

        # Get item with only key
        item2 = under_test.get_item('service', 'service3')

        self.assertEqual('service3', item2.name)
        self.assertEqual('_id3', item2.item_id)
        self.assertEqual('service3', item2.data['name'])

    def test_get_livesynthesis(self):
        """Get Livesynthesis"""

        under_test = DataManager()

        synth_test = under_test.database['livesynthesis']

        self.assertFalse(synth_test)

        under_test.update_item_database('livesynthesis', self.livesynth_list)

        self.assertTrue(under_test.database['livesynthesis'])

        synthesis_count_test = LiveSynthesis.get_synthesis_count_model()

        livesynthesis = under_test.get_synthesis_count()

        for key in synthesis_count_test:
            self.assertTrue(key in livesynthesis)
            for state in synthesis_count_test[key]:
                self.assertTrue(state in livesynthesis[key])
