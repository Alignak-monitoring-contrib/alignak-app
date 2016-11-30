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

from alignak_app.utils import get_image_path, get_template

try:
    __import__('PyQt5')
    from PyQt5.Qt import QWidget, QLabel, QGridLayout  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap, QProgressBar, QFrame  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QWidget, QLabel, QGridLayout  # pylint: disable=import-error
    from PyQt4.Qt import QPixmap, QProgressBar, QFrame  # pylint: disable=import-error


class PopupFactory(QWidget):
    """
    Class who generate a QWidget with 4 QLabels and 1 QProgressBar.

    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.main_layout = QGridLayout()
        self.pos = 0
        self.setLayout(self.main_layout)
        self.setStyleSheet("QLabel {color: black;}")
        self.state_data = {}

    def create_state(self, state_name):
        """
        Generate 4 QLabel and 1 QProgressBar and store in "state_data"
        QLabels are icon | state_label | nb_items | diff
        QProgressBar get value of percent.
        All are added horizontally.

        :param state_name: name of the state to be stored
        :type state_name: str
        """

        # Icon
        icon = QPixmap(get_image_path(state_name))
        label_icon = QLabel()
        label_icon.setFixedSize(16, 16)
        label_icon.setScaledContents(True)
        label_icon.setPixmap(icon)

        # Initialize Labels
        state_label = QLabel(self.define_label(state_name))

        nb_items = QLabel('0')

        diff = QLabel('<b>(0)</b>')

        # QProgressBar
        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setFixedHeight(22)

        # Add all to layout
        self.main_layout.addWidget(label_icon, self.pos, 0)
        self.main_layout.addWidget(state_label, self.pos, 1)
        self.main_layout.addWidget(nb_items, self.pos, 2)
        self.main_layout.addWidget(diff, self.pos, 3)
        self.main_layout.addWidget(progress_bar, self.pos, 4)

        # Store state
        self.state_data[state_name] = {
            'nb_items': nb_items,
            'diff': diff,
            'progress_bar': progress_bar
        }

        self.bar_style_sheet(state_name)

        # Increment vertically position for next widget
        self.pos += 1

    def add_separator(self):
        """
        Add an horizontal line to layout.
        """

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setMinimumSize(self.width(), 5)

        # Add to layout
        self.main_layout.addWidget(separator, self.pos, 0)

        # Increment vertically position for next widget
        self.pos += 1

    def update_states(self, state_name, nb_items, diff, percent):
        """
        Update nb_items, diff and progress_bar value.

        :param state_name: name of the state to be update
        :type state_name: str
        :param nb_items: state
        :type nb_items: str
        :param diff: str
        :type diff: str
        :param percent: value of progress bar
        :type percent: int
        """

        self.state_data[state_name]['nb_items'].setText(str(nb_items))

        if isinstance(diff, int):
            self.state_data[state_name]['diff'].setText('<b>(' + "{0:+d}".format(diff) + ')</b>')
        else:
            self.state_data[state_name]['diff'].setText('<b>(' + diff + ')</b>')

        self.state_data[state_name]['progress_bar'].setFormat('%.01f%%' % percent)
        self.state_data[state_name]['progress_bar'].setValue(float(percent))

    @staticmethod
    def get_states_states(hosts_states, services_states):
        """
        Calculates and return the sum of the items and their percentages

        :param hosts_states: number of hosts for each states
        :type hosts_states: dict
        :param services_states: number of services for each states
        :type services_states: dict
        :return: percentages
        :rtype: dict
        """

        # Initialize percentage
        percentages = {}

        # Get sum for hosts and services
        hosts_sum = hosts_states['up'] \
            + hosts_states['down'] \
            + hosts_states['unreachable']
        services_sum = services_states['ok'] \
            + services_states['warning'] \
            + services_states['critical'] \
            + services_states['unknown']

        # Calculates the percentage
        percentages['up'] = float((hosts_states['up'] * 100) / hosts_sum)
        percentages['down'] = float((hosts_states['down'] * 100) / hosts_sum)
        percentages['unreachable'] = float((hosts_states['unreachable'] * 100) / hosts_sum)

        percentages['ok'] = float((services_states['ok'] * 100) / services_sum)
        percentages['warning'] = float((services_states['warning'] * 100) / services_sum)
        percentages['critical'] = float((services_states['critical'] * 100) / services_sum)
        percentages['unknown'] = float((services_states['unknown'] * 100) / services_sum)

        return percentages

    @staticmethod
    def define_label(name):
        """
        Define label text for QLabel "label_state"

        :param name: name of state
        :type name: str
        :return: label text
        :rtype: str
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
            label = "Services WARNING:"
        elif "services_critical" in name:
            label = "Services CRITICAL:"
        elif "services_unknown" in name:
            label = "Services UNKNOWN:"
        else:
            label = "Unknown field"

        return label

    def bar_style_sheet(self, label_state):
        """
        Define the color of QProgressBar

        :param label_state: type of state
        :type label_state: str
        """

        if "hosts_up" in label_state or "services_ok" in label_state:
            bar_color = "#27ae60"
        elif "hosts_down" in label_state or "services_critical" in label_state:
            bar_color = "#e74c3c"
        elif "hosts_unreach" in label_state or "services_warning" in label_state:
            bar_color = "#e67e22"
        elif "services_unknown" in label_state:
            bar_color = "#2980b9"
        else:
            bar_color = "grey"

        self.state_data[label_state]['progress_bar'].setStyleSheet(
            get_template('popup_css.tpl', dict(bar_color=bar_color))
        )
