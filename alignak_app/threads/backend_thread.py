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

"""
    BackendQThread manage backend threads and requests
"""

from logging import getLogger

from alignak_app.core.backend import app_backend

from PyQt5.Qt import QThread, pyqtSignal  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class BackendQThread(QThread):  # pylint: disable=too-few-public-methods
    """
        Class who create a QThread to trigger requests
    """

    quit_thread = pyqtSignal(name='close_thread')

    def __init__(self, task):
        super(BackendQThread, self).__init__()
        self.task = task

    def run(self):  # pragma: no cover
        """
        Run the QThread. Trigger actions depending on the selected task

        """

        self.quit_thread.connect(self.quit)

        if 'user' in self.task:
            app_backend.query_user_data()
        elif 'host' in self.task:
            app_backend.query_hosts_data()
        elif 'service' in self.task:
            app_backend.query_services_data()
        elif 'alignakdaemon' in self.task:
            app_backend.query_daemons_data()
        elif 'livesynthesis' in self.task:
            app_backend.query_livesynthesis_data()
        elif 'history' in self.task:
            app_backend.query_history_data()
        elif 'notifications' in self.task:
            app_backend.query_notifications_data()
        else:
            logger.error("Tasks is unknown: %s", self.task)
