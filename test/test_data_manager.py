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

from alignak_app.backend.datamanager import DataManager
from alignak_app.items.event import Event
from alignak_app.items.host import Host
from alignak_app.items.livesynthesis import LiveSynthesis
from alignak_app.items.service import Service
from alignak_app.items.user import User
from alignak_app.items.realm import Realm
from alignak_app.items.period import Period


class TestDataManager(unittest2.TestCase):
    """
        This file test the DataManager class.
    """

    # Host data test
    host_list = []
    for i in range(0, 10):
        host = Host()
        host.create(
            '_id%d' % i,
            {
                'name': 'host%d' % i,
                'ls_state': 'DOWN',
                'ls_acknowledged': False,
                'ls_downtimed': False,
             },
            'host%d' % i
        )
        host_list.append(host)

    # Service data test
    service_list = []
    for i in range(0, 10):
        service = Service()
        service.create(
            '_id%d' % i,
            {
                'name': 'service%d' % i,
                'host': '_id%d' % i,
                'ls_state': 'CRITICAL',
                'ls_acknowledged': False,
                'ls_downtimed': False,
            },
            'service%d' % i
        )
        service_list.append(service)
        service = Service()
        service.create(
            'other_id2%d' % i,
            {
                'name': 'other_service2%d' % i,
                'host': '_id%d' % i,
                'ls_state': 'UP',
                'ls_acknowledged': True,
                'ls_downtimed': False,
            },
            'other_service%d' % i
        )
        service_list.append(service)

    # User data test
    user = User()
    user.create('_id', {'name': 'admin'}, 'admin')

    # Synthesis data test
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

    # Event data test
    event_data = [
        {
            '_created': 'Thu, 12 Oct 2017 13:27:02 GMT', '_id': '59df6da635d17b0277ddaaed',
            '_updated': 'Thu, 12 Oct 2017 13:27:02 GMT',
            '_etag': '70a7fd01040ce20cd84d4059849b548d493e9703',
            'message': 'HOST NOTIFICATION: imported_admin;charnay;DOWN;notify-host-by-email;Alarm timeout',
            'host': 'host1'
        },
        {
            '_created': 'Thu, 12 Oct 2017 13:27:02 GMT', '_id': '59df6da635d1j5k77dd3aed',
            '_updated': 'Thu, 12 Oct 2017 13:27:02 GMT',
            '_etag': '70a7fd01040ce20c4df459t65g9b548d493e9703',
            'message': 'HOST NOTIFICATION: imported_admin;charnay;WARNING;notify-host-by-email;Alarm timeout',
            'host': 'host2'
        },
        {
            '_created': 'Thu, 12 Oct 2017 13:27:02 GMT', '_id': '59df6tg5721j5k77dd3aed',
            '_updated': 'Thu, 12 Oct 2017 13:27:02 GMT',
            '_etag': '70a7fd01040ce20c4df459t65g9b548d493e9703',
            'message': 'SERVICE: imported_admin;charnay;alarm check;OK;notify-host-by-email;All ok',
            'host': 'host3'
        }

    ]
    event_list = []
    for data in event_data:
        event = Event()
        event.create(data['_id'], data)
        event_list.append(event)

    # Realm data test
    realm_list = []
    for i in range(0, 10):
        realm = Realm()
        realm.create(
            '_id%d' % i,
            {
                'name': 'realm%d' % i,
                'alias': 'My Realm %d' % i,
            },
            'realm%d' % i
        )
        realm_list.append(realm)

    realm_noalias = Realm()
    realm_noalias.create(
        '_id',
        {
            'name': 'realm',
        },
        'realm'
    )
    realm_list.append(realm_noalias)

    # TimePeriod data test
    period_list = []
    for i in range(0, 10):
        period = Realm()
        period.create(
            '_id%d' % i,
            {
                'name': 'period%d' % i,
                'alias': 'My Time Period %d' % i,
            },
            'period%d' % i
        )
        period_list.append(period)

    period_noalias = Period()
    period_noalias.create(
        '_id',
        {
            'name': 'period',
        },
        'period'
    )
    period_list.append(period_noalias)

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
        self.assertFalse(under_test.ready)
        self.assertNotEqual('READY', under_test.is_ready())

    def test_update_item_database(self):
        """Update DataManager Database"""

        under_test = DataManager()

        under_test.update_database('host', self.host_list)

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

        under_test.update_database('service', self.service_list)

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

        # Get item who's not here
        item3 = under_test.get_item('service', 'service10')

        self.assertIsNone(item3)

    def test_remove_item(self):
        """Remove Item from Database"""

        under_test = DataManager()

        service_1 = Service()
        service_1.create(
            'id1',
            {'name': 'service_one'},
            'name1'
        )
        service_2 = Service()
        service_2.create(
            'id2',
            {'name': 'service_two'},
            'name2'
        )
        under_test.update_database('service', [service_1, service_2])

        # Assert first service is returned
        service = under_test.get_item(
            'service',
            service_1.item_id
        )
        self.assertTrue(service)

        # Remove item
        under_test.remove_item(
            'service',
            service_1.item_id
        )

        # Item is removed
        service = under_test.get_item(
            'service',
            service_1.item_id
        )
        self.assertFalse(service)

    def test_get_realm_name(self):
        """Get Realm in db"""

        under_test = DataManager()

        self.assertFalse(under_test.database['realm'])

        under_test.update_database('realm', self.realm_list)

        self.assertTrue(under_test.database['realm'])

        realm_test = under_test.get_realm_name('_id2')

        self.assertEqual('My Realm 2', realm_test)

        noalias_realm_test = under_test.get_realm_name('_id')

        self.assertEqual('Realm', noalias_realm_test)

        no_realm_test = under_test.get_realm_name('no_realm')

        self.assertEqual('n/a', no_realm_test)

    def test_get_period_name(self):
        """Get Time Period in db"""

        under_test = DataManager()

        self.assertFalse(under_test.database['timeperiod'])

        under_test.update_database('timeperiod', self.period_list)

        self.assertTrue(under_test.database['timeperiod'])

        period_test = under_test.get_period_name('_id4')

        self.assertEqual('My Time Period 4', period_test)

        noalias_period_test = under_test.get_period_name('_id')

        self.assertEqual('Period', noalias_period_test)

        no_period_test = under_test.get_period_name('no_period')

        self.assertEqual('n/a', no_period_test)

    def test_get_livesynthesis(self):
        """Get Livesynthesis in db"""

        under_test = DataManager()

        synth_test = under_test.database['livesynthesis']

        self.assertFalse(synth_test)

        under_test.update_database('livesynthesis', self.livesynth_list)

        self.assertTrue(under_test.database['livesynthesis'])

        synthesis_count_test = LiveSynthesis.get_synthesis_count_model()

        livesynthesis = under_test.get_synthesis_count()

        # Assert Synthesis model is respected
        for key in synthesis_count_test:
            self.assertTrue(key in livesynthesis)
            for state in synthesis_count_test[key]:
                self.assertTrue(state in livesynthesis[key])

    def test_get_all_hotsnames(self):
        """Gel all Hostnames in db"""

        under_test = DataManager()

        under_test.update_database('host', self.host_list)

        hostnames_test = under_test.get_all_hostnames()

        self.assertTrue('host0' in hostnames_test)
        self.assertTrue('host1' in hostnames_test)
        self.assertTrue('host2' in hostnames_test)
        self.assertTrue('host3' in hostnames_test)
        self.assertTrue('host4' in hostnames_test)
        self.assertTrue('host5' in hostnames_test)
        self.assertTrue('host6' in hostnames_test)
        self.assertTrue('host7' in hostnames_test)
        self.assertTrue('host8' in hostnames_test)
        self.assertTrue('host9' in hostnames_test)
        self.assertTrue('host10' not in hostnames_test)

    def test_get_host_services(self):
        """Get Services of Host"""

        under_test = DataManager()

        under_test.update_database('host', self.host_list)
        under_test.update_database('service', self.service_list)

        host_services_test = under_test.get_host_services('_id1')

        for item in host_services_test:
            self.assertIsInstance(item, Service)
            self.assertTrue(item.data['host'] == '_id1')

        self.assertTrue(2 == len(host_services_test))

    def test_get_host_with_services(self):
        """Get Host with Services"""

        under_test = DataManager()

        under_test.update_database('host', self.host_list)
        under_test.update_database('service', self.service_list)

        host_with_services_test = under_test.get_host_with_services('host5')

        for _ in host_with_services_test:
            self.assertTrue('host' in host_with_services_test)
            self.assertTrue('services' in host_with_services_test)

            self.assertTrue(2 == len(host_with_services_test['services']))
            self.assertIsInstance(host_with_services_test['host'], Host)
            for service in host_with_services_test['services']:
                self.assertIsInstance(service, Service)

    def test_get_events(self):
        """Get Events to send"""

        under_test = DataManager()

        under_test.update_database('notifications', self.event_list)

        events = under_test.get_events()

        self.assertEqual(3, len(events))

        for event in events:
            self.assertTrue('message' in event)
            self.assertTrue('event_type' in event)

            if event['event_type'] == 'DOWN':
                self.assertTrue('DOWN' in event['message'])
            if event['event_type'] == 'WARNING':
                self.assertTrue('WARNING' in event['message'])
            if event['event_type'] == 'OK':
                self.assertTrue('OK' in event['message'])

    def test_is_ready(self):
        """Database is Ready"""

        under_test = DataManager()

        self.assertTrue('Collecting' in under_test.is_ready())
        under_test.db_is_ready['livesynthesis'] = True
        self.assertFalse(under_test.ready)

        self.assertTrue('Collecting' in under_test.is_ready())
        under_test.db_is_ready['user'] = True
        self.assertFalse(under_test.ready)

        self.assertTrue('Collecting' in under_test.is_ready())
        under_test.db_is_ready['realm'] = True
        self.assertFalse(under_test.ready)

        self.assertTrue('Collecting' in under_test.is_ready())
        under_test.db_is_ready['timeperiod'] = True
        self.assertFalse(under_test.ready)

        self.assertTrue('Collecting' in under_test.is_ready())
        under_test.db_is_ready['host'] = True
        self.assertFalse(under_test.ready)

        self.assertTrue('Collecting' in under_test.is_ready())
        under_test.db_is_ready['problems'] = [True, True, True]
        self.assertFalse(under_test.ready)

        self.assertTrue('Collecting' in under_test.is_ready())
        under_test.db_is_ready['alignakdaemon'] = True
        self.assertFalse(under_test.ready)

        self.assertEqual('READY', under_test.is_ready())
        self.assertTrue(under_test.ready)

    def test_update_problems(self):
        """Update Problems in Database"""

        under_test = DataManager()

        host_test = Host()
        host_test.create(
            'id_1',
            {
                'name': 'host_1',
                'ls_state': 'UP',
                'ls_acknowledged': False,
                'ls_downtimed': False,
            },
            'host_1'
        )
        service_test = Service()
        service_test.create(
            'id_2',
            {
                'name': 'service_1',
                'host': 'id_1',
                'ls_state': 'OK',
                'ls_acknowledged': False,
                'ls_downtimed': False,
            },
            'service_1'
        )
        under_test.database['host'].append(host_test)
        under_test.database['service'].append(service_test)

        under_test.update_problems()

        # Items are not problems, so not in problems database
        self.assertFalse(host_test in under_test.database['problems'])
        self.assertFalse(service_test in under_test.database['problems'])

        # Update the host to make it a problem
        under_test.update_item_data('host', 'id_1', {'ls_state': 'DOWN'})

        under_test.update_problems()

        # Host is added but not the service
        self.assertTrue(host_test in under_test.database['problems'])
        self.assertFalse(service_test in under_test.database['problems'])

        # Update the service to make it a problem, update host in host database
        under_test.update_item_data('service', 'id_2', {'ls_state': 'CRITICAL'})
        under_test.update_item_data('host', 'id_1', {'ls_state': 'OK'})

        under_test.update_problems()

        # Services is added in problems and host have been removed from problems
        self.assertFalse(host_test in under_test.database['problems'])
        self.assertTrue(service_test in under_test.database['problems'])

        # Add host with same _id in problems, but DOWN and acknowledged
        host_test_2 = Host()
        host_test_2.create(
            'id_1',
            {
                'name': 'host_1',
                'ls_state': 'DOWN',
                'ls_acknowledged': True,
                'ls_downtimed': False,
            },
            'host_1'
        )
        under_test.database['problems'].append(host_test_2)
        # New data for host in "host" database, DOWN but NOT acknowledged
        under_test.update_item_data('host', 'id_1', {'ls_state': 'DOWN'})

        under_test.update_problems()

        # Host should be in "problems" database, and not ACK.
        self.assertTrue(under_test.get_item('problems', 'id_1'))
        self.assertEqual(
            under_test.get_item('host', 'id_1').data['ls_acknowledged'],
            under_test.get_item('problems', 'id_1').data['ls_acknowledged'],
        )
        # Service still in problems
        self.assertTrue(service_test in under_test.database['problems'])

    def test_get_problems(self):
        """Get Database Problems"""

        under_test = DataManager()

        for item in self.host_list:
            under_test.database['problems'].append(item)
        for item in self.service_list:
            under_test.database['problems'].append(item)

        problems_test = under_test.get_problems()

        self.assertEqual(problems_test['hosts_nb'], 10)
        self.assertEqual(problems_test['services_nb'], 20)
        self.assertIsNotNone(problems_test['problems'])

    def test_update_item_data(self):
        """Update Item Data"""

        under_test = DataManager()
        under_test.update_database('host', self.host_list)

        self.assertEqual('DOWN', under_test.get_item('host', '_id1').data['ls_state'])

        # Update item data "ls_state"
        under_test.update_item_data(
            'host',
            '_id1',
            {
                'name': 'host1',
                'ls_state': 'UP',
                'ls_acknowledged': False,
                'ls_downtimed': False,
             }
        )

        self.assertEqual('UP', under_test.get_item('host', '_id1').data['ls_state'])
