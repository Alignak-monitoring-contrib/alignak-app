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

"""
    Backend Thread
    ++++++++++++++
    Backend Thread manage creation of QThreads for backend requests
"""

from logging import getLogger

from PyQt5.Qt import QThread

from alignak_app.backend.backend import app_backend

logger = getLogger(__name__)


class BackendQThread(QThread):  # pylint: disable=too-few-public-methods
    """
        Class who create a QThread to trigger requests
    """

    problem_states = ['CRITICAL', 'WARNING', 'UNKNOWN']

    def __init__(self, thread, data=None):
        super(BackendQThread, self).__init__()
        self.thread_name = thread
        self.data = data

    def run(self):  # pragma: no cover
        """
        Run the QThread. Trigger actions depending on the selected thread_name

        """

        if app_backend.connected:
            logger.debug('Launch a new thread request for backend: %s', self.thread_name)
            if 'user' in self.thread_name:
                app_backend.query_user()
            elif 'host' in self.thread_name:
                app_backend.query_hosts()
            elif 'service' in self.thread_name:
                app_backend.query_services()
            elif self.thread_name in self.problem_states:
                app_backend.query_services_problems(self.thread_name)
            elif 'alignakdaemon' in self.thread_name:
                app_backend.query_alignakdaemons()
            elif 'livesynthesis' in self.thread_name:
                app_backend.query_livesynthesis()
            elif 'realm' in self.thread_name:
                app_backend.query_realms()
            elif 'timeperiod' in self.thread_name:
                app_backend.query_timeperiods()
            elif self.thread_name == 'history':
                if self.data:
                    app_backend.query_history(self.data['hostname'], self.data['host_id'])
                else:
                    app_backend.query_history()
            elif 'notifications' in self.thread_name:
                app_backend.query_notifications()
            else:
                logger.error("Thread is unknown: %s", self.thread_name)
        else:
            logger.warning('The app is offline, the threads can not be launched !')
            self.quit()
