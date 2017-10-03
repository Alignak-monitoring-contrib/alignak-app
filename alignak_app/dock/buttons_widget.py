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
     dashboard, host, problems, user and webui
"""

from alignak_app.core.utils import get_image_path, get_css

from PyQt5.Qt import QPushButton, QWidget, QIcon, QHBoxLayout  # pylint: disable=no-name-in-module


class ButtonsQWidget(QWidget):
    """
        Class who create buttons for Dock QWidget
    """

    def __init__(self):
        super(ButtonsQWidget, self).__init__()
        self.setStyleSheet(get_css())
        # Fields
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

        self.dashboard_btn.setIcon(QIcon(get_image_path('dashboard')))
        self.dashboard_btn.setFixedSize(40, 40)
        layout.addWidget(self.dashboard_btn)

        self.host_btn.setIcon(QIcon(get_image_path('host')))
        self.host_btn.setFixedSize(40, 40)
        layout.addWidget(self.host_btn)

        self.problems_btn.setIcon(QIcon(get_image_path('problem')))
        self.problems_btn.setFixedSize(40, 40)
        layout.addWidget(self.problems_btn)

        self.profile_btn.setIcon(QIcon(get_image_path('user')))
        self.profile_btn.setFixedSize(40, 40)
        layout.addWidget(self.profile_btn)

        self.webui_btn.setIcon(QIcon(get_image_path('web')))
        self.webui_btn.setFixedSize(40, 40)
        layout.addWidget(self.webui_btn)
