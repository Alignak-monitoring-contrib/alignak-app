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
    Buttons
    +++++++
    Buttons manage creation of QWidgets with QPush butttons for:

    * Hosts Synthesys View
    * Problems view
    * User widget
    * Webui to reach Alignak-Webui

"""

from logging import getLogger

from PyQt5.Qt import QPushButton, QWidget, QIcon, QHBoxLayout, QTimer

from alignak_app.utils.config import settings, open_url

from alignak_app.qobjects.dock.user import UserQWidget

logger = getLogger(__name__)


class ButtonsQWidget(QWidget):
    """
        Class who create buttons for Dock QWidget
    """

    def __init__(self, parent=None):
        super(ButtonsQWidget, self).__init__(parent)
        # Fields
        self.user_widget = UserQWidget()
        self.update_timer = QTimer()
        self.webui_btn = QPushButton()
        self.profile_btn = QPushButton()
        self.problems_btn = QPushButton()
        self.host_btn = QPushButton()
        self.dashboard_btn = QPushButton()

    def initialize(self):
        """
        Initialize QWidget

        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.host_btn.setIcon(QIcon(settings.get_image('host')))
        self.host_btn.setFixedSize(40, 40)
        layout.addWidget(self.host_btn)

        self.problems_btn.setIcon(QIcon(settings.get_image('problem')))
        self.problems_btn.setFixedSize(40, 40)
        self.problems_btn.setToolTip(_('See current problems'))
        layout.addWidget(self.problems_btn)

        self.user_widget.initialize()
        self.profile_btn.setIcon(QIcon(settings.get_image('user')))
        self.profile_btn.setFixedSize(40, 40)
        self.profile_btn.clicked.connect(self.open_user_widget)
        self.profile_btn.setToolTip(_('User'))
        layout.addWidget(self.profile_btn)

        self.webui_btn.setIcon(QIcon(settings.get_image('web')))
        self.webui_btn.setFixedSize(40, 40)
        self.webui_btn.clicked.connect(
            lambda: open_url('livestate')
        )
        layout.addWidget(self.webui_btn)

        self.update_widget()

        update_buttons = int(settings.get_config('Alignak-app', 'update_buttons')) * 1000
        self.update_timer.setInterval(update_buttons)
        self.update_timer.start()
        self.update_timer.timeout.connect(self.update_widget)

    def update_widget(self):
        """
        Update the QWidget buttons

        """

        if settings.get_config('Alignak', 'webui'):
            self.webui_btn.setEnabled(True)
            self.webui_btn.setToolTip(_("Open WebUI in browser"))
        else:
            self.webui_btn.setEnabled(False)
            self.webui_btn.setToolTip(_("WebUI is not set in configuration file."))

    def open_user_widget(self):
        """
        Show UserQWidget

        """

        self.user_widget.update_widget()
        self.user_widget.app_widget.show_widget()
