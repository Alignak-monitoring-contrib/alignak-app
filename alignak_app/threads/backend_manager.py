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
    BackendManager manage backend data and threads
"""


from PyQt5.Qt import QTimer, QObject

from alignak_app.core.backend import AppBackend
from alignak_app.core.data_manager import DataManager
from alignak_app.core.locales import init_localization
from alignak_app.core.utils import init_config
from alignak_app.threads.backend_thread import BackendThread

init_config()
init_localization()


class BackendManager(QObject):
    """
        Class who create QThreads to periodically request on Alignak Backend
        Store also data received by requests.
    """

    def __init__(self, parent=None):
        super(BackendManager, self).__init__(parent)
        self.app_backend = AppBackend()
        self.app_backend.login()
        self.backend_thread = BackendThread(self.app_backend, parent=self)

    def start(self):
        """
        Start the manager

        """
        print("Start backend Manager")
        timer = QTimer(self)
        timer.setInterval(30000)
        timer.start()
        self.backend_thread.trigger.connect(self.update_data)
        timer.timeout.connect(self.backend_thread.start)

    def update_data(self, data_manager):
        """
        Update data stored.

        :param data_manager: DataManager who store all data, updated by BackendThread
        :type data_manager: DataManager
        """

        for item in data_manager.database:
            print("Item: %s : %s" % (item, str(data_manager.database[item])))

        test = data_manager.get_item('host', '59ca454035d17b9607d66c52')
        print(test)


if __name__ == '__main__':
    import sys
    from PyQt5.Qt import QApplication

    app = QApplication(sys.argv)

    mainwindow = BackendManager()
    mainwindow.start()

    sys.exit(app.exec_())