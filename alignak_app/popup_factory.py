#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    States_factory manage the creation of QWidget who display:
        icon | state | number in this state | changes | progress_bar
"""

from alignak_app.utils import get_image_path

try:
    __import__('PyQt5')
    from PyQt5.Qt import QWidget, QLabel, QGridLayout  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap, QProgressBar  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QWidget, QLabel, QGridLayout  # pylint: disable=import-error
    from PyQt4.Qt import QPixmap, QProgressBar  # pylint: disable=import-error


class StateFactory(QWidget):
    """
    Class who generate a QWidget for notification content
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.main_layout = QGridLayout()
        self.pos = 0
        self.setLayout(self.main_layout)
        self.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; }"
            "QLabel {color: black; }"
        )
        self.state = {}

    def create_state(self, name):
        """
        Create QLabels and QProgressBar for state:
            icon | label | state | change | progressbar

        :param name: name of the state
        :type name: str
        """

        icon = QLabel()
        icon.setFixedSize(16, 16)
        img = QPixmap(get_image_path(name))
        icon.setPixmap(img)
        icon.setScaledContents(True)

        label = QLabel(self.define_label(name))

        state = QLabel('0')

        change = QLabel('<b>(0)</b>')

        progress_bar = QProgressBar()
        progress_bar.setValue(0)

        self.main_layout.addWidget(icon, self.pos, 0)
        self.main_layout.addWidget(label, self.pos, 1)
        self.main_layout.addWidget(state, self.pos, 2)
        self.main_layout.addWidget(change, self.pos, 3)
        self.main_layout.addWidget(progress_bar, self.pos, 4)

        self.state[name] = {
            'state': state,
            'change': change,
            'progress_bar': progress_bar
        }

        self.pos += 1

    def update_states(self, name, state, change, percent):
        """

        :param name: name of the state to update
        :type name: str
        :param state:
        :param change:
        :param percent:
        :return:
        """

        self.state[name]['state'].setText(str(state))
        self.state[name]['change'].setText('<b>(' + str(change) + ')</b>')
        self.state[name]['progress_bar'].setValue(int(percent))

    @staticmethod
    def define_label(name):
        """

        :param name:
        :return:
        """

        if "hosts_up" in name:
            label = "Hosts UP:"
        elif "hosts_down" in name:
            label = "Hosts DOWN:"
        elif "hosts_unreach" in name:
            label = "Hosts UNREACHABLE:"
        elif "services_ok" in name:
            label = "Services OK:"
        elif "services_warning" in name:
            label = "Hosts DOWN:"
        elif "services_critical" in name:
            label = "Hosts DOWN:"
        elif "services_unknown" in name:
            label = "Hosts DOWN:"
        else:
            label = "Unknown field"

        return label
