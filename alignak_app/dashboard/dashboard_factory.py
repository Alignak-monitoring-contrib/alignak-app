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

import webbrowser
from logging import getLogger
from alignak_app.core.utils import get_image_path, get_css, get_app_config

from PyQt5.Qt import QWidget, QLabel, QGridLayout, QPushButton  # pylint: disable=no-name-in-module
from PyQt5.Qt import QPixmap, QProgressBar, QFrame, Qt, QIcon  # pylint: disable=no-name-in-module

logger = getLogger(__name__)


class DashboardFactory(QWidget):
    """
        Class who help to create Dashboard QWidget.
    """

    def __init__(self, parent=None):
        super(DashboardFactory, self).__init__(parent)
        self.row = 0
        self.setMaximumWidth(parent.width())
        self.state_data = {}
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setStyleSheet(get_css())

    def create_state_labels(self, state_name):
        """
        Generate 4 QLabel and 1 QProgressBar and store them in "state_data"
        QLabels are: state_icon | state_text | state_number | state_diff
        QProgressBar get value of percent.
        All are added on one row define by "row" value

        :param state_name: name of the state to be stored
        :type state_name: str
        """

        # Icon
        icon = QPixmap(get_image_path(state_name))
        state_icon = QLabel()
        state_icon.setFixedSize(16, 16)
        state_icon.setScaledContents(True)
        state_icon.setPixmap(icon)

        # Initialize Labels
        state_text = QLabel(self.define_label(state_name))
        state_number = QLabel()
        state_diff = QLabel()

        # QProgressBar
        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setFixedHeight(20)
        progress_bar.setObjectName(state_name)

        # WebUI Button
        button = QPushButton()
        button.setIcon(QIcon(get_image_path('eye')))
        button.setToolTip(_("See in WebUI ?"))
        button.setObjectName(self.define_label(state_name))
        button.setMaximumSize(20, 20)
        button.released.connect(self.open_url)

        # Layout
        self.main_layout.addWidget(state_icon, self.row, 0)
        self.main_layout.addWidget(state_text, self.row, 1)
        self.main_layout.addWidget(state_number, self.row, 2)
        self.main_layout.setAlignment(state_number, Qt.AlignCenter)
        self.main_layout.addWidget(state_diff, self.row, 3)
        self.main_layout.addWidget(progress_bar, self.row, 4)
        self.main_layout.addWidget(button, self.row, 5)

        # Store state
        self.state_data[state_name] = {
            'icon': state_icon,
            'state_number': state_number,
            'diff': state_diff,
            'progress_bar': progress_bar
        }

        # Increment vertically position for next widget
        self.row += 1

    def open_url(self):  # pragma: no cover
        """
        Add a link to Alignak-WebUI on every menu

        """

        webui_url = get_app_config('Alignak', 'webui')
        # Define each filter for items
        if "UP" in self.sender().objectName():
            endurl = '/hosts/table?search=ls_state:UP'
        elif "DOWN" in self.sender().objectName():
            endurl = '/hosts/table?search=ls_state:DOWN'
        elif "UNREACHABLE" in self.sender().objectName():
            if 'Hosts' in self.sender().objectName():
                endurl = '/hosts/table?search=ls_state:UNREACHABLE'
            else:
                endurl = '/services/table?search=ls_state:UNREACHABLE'
        elif 'OK' in self.sender().objectName():
            endurl = '/services/table?search=ls_state:OK'
        elif 'CRITICAL' in self.sender().objectName():
            endurl = '/services/table?search=ls_state:CRITICAL'
        elif 'WARNING' in self.sender().objectName():
            endurl = '/services/table?search=ls_state:WARNING'
        elif 'UNKNOWN' in self.sender().objectName():
            endurl = '/services/table?search=ls_state:UNKNOWN'
        elif "ACKNOWLEDGE" in self.sender().objectName():
            if 'Hosts' in self.sender().objectName():
                endurl = '/hosts/table?search=ls_acknowledged:yes'
            else:
                endurl = '/services/table?search=ls_acknowledged:yes'
        else:
            endurl = '/dashboard'

        if "DOWNTIME" in self.sender().objectName():
            if 'Hosts' in self.sender().objectName():
                endurl = '/hosts/table?search=ls_downtime:yes'
            else:
                endurl = '/services/table?search=ls_downtime:yes'

        logger.debug('Open url : ' + webui_url + endurl)
        webbrowser.open(webui_url + endurl)

    def add_separator(self):
        """
        Add an horizontal line to layout.
        """

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setMinimumSize(self.width(), 2)

        # Add to layout
        self.main_layout.addWidget(separator, self.row, 0, 1, 5)

        # Increment vertically position for next widget
        self.row += 1

    def update_states(self, state_name, nb_items, diff, percent):
        """
        Update nb_items, diff and progress_bar value for the given "state_name"

        :param state_name: name of the state to be update
        :type state_name: str
        :param nb_items: state
        :type nb_items: str
        :param diff: str
        :type diff: str
        :param percent: value of progress bar
        :type percent: int
        """

        # State number
        self.state_data[state_name]['state_number'].setText(str(nb_items))

        # Icon
        if nb_items == 0 and 'downtime' not in state_name and 'acknowledge' not in state_name:
            if 'hosts' in state_name:
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

        # Diff between last check
        if diff != 0:
            self.state_data[state_name]['diff'].setText('<b>(%s)</b>' % "{0:+d}".format(diff))
        else:
            self.state_data[state_name]['diff'].setText('')

        # ProgressBar
        if percent == 0.0:
            self.state_data[state_name]['progress_bar'].setFormat('-')
            self.state_data[state_name]['progress_bar'].setValue(0)
        else:
            self.state_data[state_name]['progress_bar'].setFormat('%.02f%%' % percent)
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
        for h_state in synthesis['hosts']:
            hosts_sum += synthesis['hosts'][h_state]
        services_sum = 0
        for s_state in synthesis['services']:
            services_sum += synthesis['services'][s_state]

        # Calculates the percentage
        try:
            for state in synthesis['hosts']:
                percentages['hosts'][state] = \
                    float(synthesis['hosts'][state]) * 100.0 / float(hosts_sum)
            # Services
            for state in synthesis['services']:
                percentages['services'][state] = \
                    float(synthesis['services'][state]) * 100.0 / float(services_sum)
        except ZeroDivisionError as e:
            logger.error(str(e))

        # Fill percentages if not filled before
        host_states = ['up', 'unreachable', 'down', 'acknowledge', 'downtime']
        service_states = [
            'ok', 'warning', 'critical', 'unknown', 'unreachable', 'acknowledge', 'downtime'
        ]
        for host_state in host_states:
            if host_state not in percentages['hosts']:
                percentages['hosts'][host_state] = 0.0
        for service_state in service_states:
            if service_state not in percentages['services']:
                percentages['services'][service_state] = 0.0

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
            logger.error('Bad label state name: %s', name)
            logger.error(str(e))
            return 'Unknown field'
