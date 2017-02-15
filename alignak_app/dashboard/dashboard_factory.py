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
    Dashboard Factory manage the creation of Dashboard Qwidget
"""

from logging import getLogger
from alignak_app.core.utils import get_image_path, get_css

try:
    __import__('PyQt5')
    from PyQt5.Qt import QWidget, QLabel, QGridLayout, QIcon  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QPixmap, QProgressBar, QFrame  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import Qt  # pylint: disable=import-error
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QWidget, QLabel, QGridLayout, QIcon  # pylint: disable=import-error
    from PyQt4.Qt import QPixmap, QProgressBar, QFrame  # pylint: disable=import-error
    from PyQt4.QtCore import Qt  # pylint: disable=import-error

logger = getLogger(__name__)


class DashboardFactory(QWidget):
    """
        Class who help to create Dashboard QWidget.
    """

    def __init__(self, parent=None):
        super(DashboardFactory, self).__init__(parent)
        self.pos = 0
        self.setMaximumWidth(parent.width())
        self.state_data = {}
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setStyleSheet(get_css())

    def create_state_labels(self, state_name, item_type=None):
        """
        Generate 4 QLabel and 1 QProgressBar and store in "state_data"
        QLabels are: icon | state_label | nb_items | diff
        QProgressBar get value of percent.
        All are added horizontally.

        :param state_name: name of the state to be stored
        :type state_name: str
        :param item_type: if needed, precise if "hosts" or "services"
        :type item_type: str
        """

        # Icon
        icon = QPixmap(get_image_path(state_name))
        label_icon = QLabel()
        label_icon.setFixedSize(16, 16)
        label_icon.setScaledContents(True)
        label_icon.setPixmap(icon)

        if item_type:
            state_name = item_type + '_' + state_name

        # Initialize Labels
        state_label = QLabel(self.define_label(state_name))

        nb_items = QLabel('0')

        diff = QLabel('<b>(0)</b>')

        # QProgressBar
        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setFixedHeight(20)

        # Layout
        self.main_layout.addWidget(label_icon, self.pos, 0)
        self.main_layout.addWidget(state_label, self.pos, 1)
        self.main_layout.addWidget(nb_items, self.pos, 2)
        self.main_layout.setAlignment(nb_items, Qt.AlignCenter)
        self.main_layout.addWidget(diff, self.pos, 3)
        self.main_layout.addWidget(progress_bar, self.pos, 4)

        # Store state
        self.state_data[state_name] = {
            'icon': label_icon,
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
        separator.setMinimumSize(self.width(), 2)

        # Add to layout
        self.main_layout.addWidget(separator, self.pos, 0, 1, 5)

        # Increment vertically position for next widget
        self.pos += 1

    def update_states(self, state_name, nb_items, diff, percent):
        """
        Update nb_items, diff and progress_bar value for hte given "state_name"

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

        if nb_items == 0 and 'downtime' not in state_name and 'acknowledge' not in state_name:
            if "hosts" in state_name:
                self.state_data[state_name]['icon'].setPixmap(
                    QPixmap(get_image_path('hosts_none'))
                )
            else:
                self.state_data[state_name]['icon'].setPixmap(
                    QPixmap(get_image_path('services_none'))
                )
        else:
            self.state_data[state_name]['icon'].setPixmap(
                QPixmap(get_image_path(state_name))
            )

        if diff != 0:
            self.state_data[state_name]['diff'].setText('<b>(' + "{0:+d}".format(diff) + ')</b>')
        else:
            self.state_data[state_name]['diff'].setText('')

        self.state_data[state_name]['progress_bar'].setFormat('%.01f%%' % percent)
        self.state_data[state_name]['progress_bar'].setValue(float(percent))

    @staticmethod
    def get_percentages_states(synthesis):
        """
        Calculates and return the sum of the items and their percentages

        :param synthesis: backend synthesis data
        :type synthesis: dict
        :return: percentages of each states
        :rtype: dict
        """

        # Initialize percentage
        percentages = {
            'hosts': {},
            'services': {},
        }

        # Get sum for hosts and services
        hosts_sum = 0
        services_sum = 0
        for h_state in synthesis['hosts']:
            hosts_sum += synthesis['hosts'][h_state]
        for s_state in synthesis['services']:
            services_sum += synthesis['services'][s_state]

        # Calculates the percentage
        try:
            # Hosts
            for state in synthesis['hosts']:
                percentages['hosts'][state] = float(
                    (synthesis['hosts'][state] * 100) / hosts_sum
                )
            # Services
            for state in synthesis['services']:
                percentages['services'][state] = float(
                    (synthesis['services'][state] * 100) / services_sum
                )
        except ZeroDivisionError as e:
            logger.error(str(e))

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

        label_model = {
            "hosts_up": "Hosts UP:",
            "hosts_down": "Hosts DOWN:",
            "hosts_unreachable": "Hosts UNREACHABLE:",
            "hosts_acknowledge": "Hosts ACKNOWLEDGED:",
            "hosts_downtime": "Hosts DOWNTIMED:",
            "services_ok": "Services OK:",
            "services_warning": "Services WARNING:",
            "services_critical": "Services CRITICAL:",
            "services_unknown": "Services UNKNOWN:",
            "services_unreachable": "Services UNREACHABLE:",
            "services_acknowledge": "Services ACKNOWLEDGED:",
            "services_downtime": "Services DOWNTIMED:",
        }

        try:
            return label_model[name]
        except KeyError as e:
            logger.error('Notification name : ' + name)
            logger.error(str(e))
            return 'Unknow field'

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
        elif "hosts_unreachable" in label_state or "services_warning" in label_state:
            bar_color = "#e67e22"
        elif "services_unknown" in label_state:
            bar_color = "#2980b9"
        else:
            bar_color = "grey"

        self.state_data[label_state]['progress_bar'].setStyleSheet(
            """QProgressBar::chunk {
                background-color: %s;
}           """ % bar_color
        )
