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
    Buttons QWidget manage the buttons for:
     host, problems, user and webui
"""

from logging import getLogger

from PyQt5.Qt import QPushButton, QWidget, QIcon, QHBoxLayout, QTimer

from alignak_app.core.utils.config import get_image, app_css, get_app_config, open_url
from alignak_app.pyqt.dock.widgets.user import UserQWidget
from alignak_app.pyqt.panel.widgets.panel import PanelQWidget

logger = getLogger(__name__)


class ButtonsQWidget(QWidget):
    """
        Class who create buttons for Dock QWidget
    """

    def __init__(self, parent=None):
        super(ButtonsQWidget, self).__init__(parent)
        self.setStyleSheet(app_css)
        # Fields
        self.user_widget = UserQWidget()
        self.panel_widget = PanelQWidget()
        self.update_timer = QTimer()
        self.webui_btn = QPushButton()
        self.profile_btn = QPushButton()
        self.problems_btn = QPushButton()
        self.host_btn = QPushButton()
        self.dashboard_btn = QPushButton()

    def initialize(self, dock_width, spy_widget):
        """
        Initialize QWidget

        :param dock_width: width of dock, needed for PanelQWidget
        :type dock_width: int
        :param spy_widget: SpyQWidget to allow HostQWidget add spied host
        :type spy_widget: alignak_app.widgets.dock.spy.SpyQWidget
        """

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.panel_widget.initialize(dock_width, spy_widget)
        self.host_btn.setIcon(QIcon(get_image('host')))
        self.host_btn.setFixedSize(40, 40)
        self.host_btn.clicked.connect(self.open_host_widget)
        layout.addWidget(self.host_btn)

        self.problems_btn.setIcon(QIcon(get_image('problem')))
        self.problems_btn.setFixedSize(40, 40)
        self.problems_btn.setToolTip(_('See current problems'))
        self.problems_btn.clicked.connect(self.open_problems_widget)
        layout.addWidget(self.problems_btn)

        self.user_widget.initialize()
        self.profile_btn.setIcon(QIcon(get_image('user')))
        self.profile_btn.setFixedSize(40, 40)
        self.profile_btn.clicked.connect(self.open_user_widget)
        layout.addWidget(self.profile_btn)

        self.webui_btn.setIcon(QIcon(get_image('web')))
        self.webui_btn.setFixedSize(40, 40)
        self.webui_btn.clicked.connect(
            lambda: open_url('livestate')
        )
        layout.addWidget(self.webui_btn)

        self.update_widget()

        update_buttons = int(get_app_config('Alignak-app', 'update_buttons')) * 1000
        self.update_timer.setInterval(update_buttons)
        self.update_timer.start()
        self.update_timer.timeout.connect(self.update_widget)

    def update_widget(self):
        """
        Update the QWidget buttons

        """

        logger.info('Update Buttons QWidget...')

        if get_app_config('Alignak', 'webui'):
            self.webui_btn.setEnabled(True)
            self.webui_btn.setToolTip(_("Open WebUI in browser"))
        else:
            self.webui_btn.setEnabled(False)
            self.webui_btn.setToolTip(_("WebUI is not set in configuration file."))

    def open_host_widget(self):
        """
        Show HostQWidget

        """

        self.panel_widget.app_widget.show()
        self.panel_widget.tab_widget.setCurrentIndex(0)

    def open_problems_widget(self):
        """
        Show ProblemsQWidget

        """

        self.panel_widget.app_widget.show()
        self.panel_widget.tab_widget.setCurrentIndex(1)

    def open_user_widget(self):
        """
        Show UserQWidget

        """

        self.user_widget.update_widget()
        self.user_widget.app_widget.show_widget()
