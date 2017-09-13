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
    Actions display QDialog's for actions : Acknowledge and Downtime
"""


import datetime
from logging import getLogger

from alignak_app.core.utils import get_image_path, get_css


from PyQt5.QtWidgets import QDialog, QWidget  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QTimeEdit, QDateTimeEdit  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QPushButton, QLabel  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QVBoxLayout, QTextEdit  # pylint: disable=no-name-in-module
from PyQt5.Qt import QIcon, QPixmap, QCheckBox, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtCore import QTime  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


def get_logo_widget(widget):
    """
    Return the logo QWidget

    :return: logo QWidget
    :rtype: QWidget
    """

    logo_widget = QWidget()
    logo_widget.setFixedHeight(45)
    logo_widget.setObjectName('title')
    logo_layout = QHBoxLayout()
    logo_widget.setLayout(logo_layout)

    logo_label = QLabel()
    logo_label.setPixmap(QPixmap(get_image_path('alignak')))
    logo_label.setFixedSize(121, 35)
    logo_label.setScaledContents(True)

    logo_layout.addWidget(logo_label, 0)

    minimize_btn = QPushButton()
    minimize_btn.setIcon(QIcon(get_image_path('minimize')))
    minimize_btn.setFixedSize(24, 24)
    minimize_btn.setObjectName('app_widget')
    minimize_btn.clicked.connect(widget.showMinimized)
    logo_layout.addStretch(widget.width())
    logo_layout.addWidget(minimize_btn, 1)

    maximize_btn = QPushButton()
    maximize_btn.setIcon(QIcon(get_image_path('maximize')))
    maximize_btn.setFixedSize(24, 24)
    maximize_btn.setObjectName('app_widget')
    maximize_btn.clicked.connect(widget.showMaximized)
    logo_layout.addWidget(maximize_btn, 2)

    close_btn = QPushButton()
    close_btn.setIcon(QIcon(get_image_path('exit')))
    close_btn.setObjectName('app_widget')
    close_btn.setFixedSize(24, 24)
    close_btn.clicked.connect(widget.close)
    logo_layout.addWidget(close_btn, 3)

    return logo_widget


class Acknowledge(QDialog):
    """
        Class who create Acknowledge QDialog for hosts/services
    """

    def __init__(self, parent=None):
        super(Acknowledge, self).__init__(parent)
        self.setWindowTitle('Request an Acknowledge')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setMinimumSize(360, 460)
        # Fields
        self.sticky = True
        self.notify = False
        self.ack_comment_edit = None

    def initialize(self, item_type, item_name, comment):
        """
        Initialize Acknowledge QDialog

        :param item_type: type of item to acknowledge : host | service
        :type item_type: str
        :param item_name: name of the item to acknowledge
        :type item_name: str
        :param comment: the default comment of action
        :type comment: str
        """

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(get_logo_widget(self))

        ack_widget = QWidget()
        ack_widget.setObjectName('login')
        ack_layout = QGridLayout(ack_widget)

        ack_title = QLabel('<h2>Request an acknowledge</h2>')
        ack_layout.addWidget(ack_title, 0, 0, 1, 2)

        host_label = QLabel('<h2>%s: %s</h2>' % (item_type.capitalize(), item_name))
        ack_layout.addWidget(host_label, 1, 0, 1, 1)

        sticky_label = QLabel('Acknowledge is sticky:')
        sticky_label.setObjectName('actions')
        ack_layout.addWidget(sticky_label, 2, 0, 1, 1)

        sticky_checkbox = QCheckBox()
        sticky_checkbox.setObjectName('actions')
        sticky_checkbox.setChecked(self.sticky)
        sticky_checkbox.setFixedSize(18, 18)
        ack_layout.addWidget(sticky_checkbox, 2, 1, 1, 1)

        sticky_info = QLabel(
            '<i>If checked, '
            'the acknowledge will remain until the element returns to an "OK" state.</i>'
        )
        sticky_info.setWordWrap(True)
        ack_layout.addWidget(sticky_info, 3, 0, 1, 2)

        notify_label = QLabel('Acknowledge notifies:')
        notify_label.setObjectName('actions')
        ack_layout.addWidget(notify_label, 4, 0, 1, 1)

        notify_checkbox = QCheckBox()
        notify_checkbox.setObjectName('actions')
        notify_checkbox.setChecked(self.notify)
        notify_checkbox.setFixedSize(18, 18)
        ack_layout.addWidget(notify_checkbox, 4, 1, 1, 1)

        notify_info = QLabel(
            '<i>If checked, a notification will be sent out to the concerned contacts.'
        )
        notify_info.setWordWrap(True)
        ack_layout.addWidget(notify_info, 5, 0, 1, 2)

        ack_comment = QLabel('Acknowledge comment:')
        ack_comment.setObjectName('actions')
        ack_layout.addWidget(ack_comment, 6, 0, 1, 1)

        self.ack_comment_edit = QTextEdit()
        self.ack_comment_edit.setText(comment)
        self.ack_comment_edit.setMaximumHeight(60)
        ack_layout.addWidget(self.ack_comment_edit, 7, 0, 1, 2)

        request_btn = QPushButton('REQUEST ACKNOWLEDGE', self)
        request_btn.clicked.connect(self.accept)
        request_btn.setObjectName('valid')
        request_btn.setMinimumHeight(30)
        request_btn.setDefault(True)
        ack_layout.addWidget(request_btn, 8, 0, 1, 2)

        main_layout.addWidget(ack_widget)

    def mousePressEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))


class Downtime(QDialog):
    """
        Class who create Downtime QDialog for hosts/services
    """

    def __init__(self, parent=None):
        super(Downtime, self).__init__(parent)
        self.setWindowTitle('Request a Downtime')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(get_css())
        self.setWindowIcon(QIcon(get_image_path('icon')))
        self.setMinimumSize(360, 460)
        # Fields
        self.fixed = True
        self.duration = QTimeEdit()
        self.start_time = QDateTimeEdit()
        self.end_time = QDateTimeEdit()
        self.comment_edit = QTextEdit()

    def initialize(self, item_type, item_name, comment):
        """
        Initialize Downtime QDialog

        :param item_type: type of item to acknowledge : host | service
        :type item_type: str
        :param item_name: name of the item to acknowledge
        :type item_name: str
        :param comment: the default comment of action
        :type comment: str
        """

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(get_logo_widget(self))

        downtime_widget = QWidget()
        downtime_widget.setObjectName('login')
        downtime_layout = QGridLayout(downtime_widget)

        ack_title = QLabel('<h2>Request a downtime</h2>')
        downtime_layout.addWidget(ack_title, 0, 0, 1, 3)

        host_label = QLabel('<h2>%s: %s</h2>' % (item_type.capitalize(), item_name))
        downtime_layout.addWidget(host_label, 1, 0, 1, 1)

        options_label = QLabel('Downtime options:')
        options_label.setObjectName('actions')
        downtime_layout.addWidget(options_label, 2, 0, 1, 1)

        fixed_checkbox = QCheckBox()
        fixed_checkbox.setObjectName('actions')
        fixed_checkbox.setChecked(self.fixed)
        fixed_checkbox.setFixedSize(18, 18)
        downtime_layout.addWidget(fixed_checkbox, 2, 1, 1, 1)

        fixed_label = QLabel('Fixed')
        fixed_label.setObjectName('actions')
        downtime_layout.addWidget(fixed_label, 2, 2, 1, 1)

        fixed_info = QLabel(
            '<i>If checked, downtime will start and end at the times specified'
            ' by the “start time” and “end time” fields.</i>'
        )
        fixed_info.setWordWrap(True)
        downtime_layout.addWidget(fixed_info, 3, 0, 1, 3)

        duration_label = QLabel('Duration')
        duration_label.setObjectName('actions')
        downtime_layout.addWidget(duration_label, 4, 0, 1, 1)

        duration_clock = QLabel()
        duration_clock.setPixmap(QPixmap(get_image_path('clock')))
        downtime_layout.addWidget(duration_clock, 4, 1, 1, 1)
        duration_clock.setFixedSize(16, 16)
        duration_clock.setScaledContents(True)

        self.duration.setTime(QTime(4, 00))
        self.duration.setDisplayFormat("HH'h'mm")
        downtime_layout.addWidget(self.duration, 4, 2, 1, 1)

        duration_info = QLabel(
            '<i>Sets the duration if it is a non-fixed downtime.</i>'
        )
        downtime_layout.addWidget(duration_info, 5, 0, 1, 3)

        date_range_label = QLabel('Downtime date range')
        date_range_label.setObjectName('actions')
        downtime_layout.addWidget(date_range_label, 6, 0, 1, 1)

        calendar_label = QLabel()
        calendar_label.setPixmap(QPixmap(get_image_path('calendar')))
        calendar_label.setFixedSize(16, 16)
        calendar_label.setScaledContents(True)
        downtime_layout.addWidget(calendar_label, 6, 1, 1, 1)

        start_time_label = QLabel('Start time:')
        downtime_layout.addWidget(start_time_label, 7, 0, 1, 1)

        self.start_time.setCalendarPopup(True)
        self.start_time.setDateTime(datetime.datetime.now())
        self.start_time.setDisplayFormat("dd/MM/yyyy HH'h'mm")
        downtime_layout.addWidget(self.start_time, 7, 1, 1, 2)

        end_time_label = QLabel('End time:')
        downtime_layout.addWidget(end_time_label, 8, 0, 1, 1)

        self.end_time.setCalendarPopup(True)
        self.end_time.setDateTime(datetime.datetime.now() + datetime.timedelta(hours=2))
        self.end_time.setDisplayFormat("dd/MM/yyyy HH'h'mm")
        downtime_layout.addWidget(self.end_time, 8, 1, 1, 2)

        self.comment_edit.setText(comment)
        self.comment_edit.setMaximumHeight(60)
        downtime_layout.addWidget(self.comment_edit, 9, 0, 1, 3)

        request_btn = QPushButton('REQUEST DOWNTIME', self)
        request_btn.clicked.connect(self.handle_accept)
        request_btn.setObjectName('valid')
        request_btn.setMinimumHeight(30)
        request_btn.setDefault(True)
        downtime_layout.addWidget(request_btn, 10, 0, 1, 3)

        main_layout.addWidget(downtime_widget)

    def duration_to_seconds(self):
        """
        Return "duration" QTimeEdit value in seconds

        :return: "duration" in seconds
        :rtype: int
        """

        return QTime(0, 0).secsTo(self.duration.time())

    def handle_accept(self):
        """
        Check if end_time timestamp is not lower than start_time

        """

        if self.start_time.dateTime().toTime_t() > self.end_time.dateTime().toTime_t():
            logger.warning('Try to add Downtime with "End Time" lower than "Start Time"')
        else:
            self.accept()

    def mousePressEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """ QWidget.mousePressEvent(QMouseEvent) """

        try:
            x = event.globalX()
            y = event.globalY()
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x - x_w, y - y_w)
        except AttributeError as e:
            logger.warning('Move Event %s: %s', self.objectName(), str(e))


if __name__ == '__main__':  # pylint: disable-all
    from PyQt5.QtWidgets import QApplication
    from alignak_app.core.utils import init_config
    import sys

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    init_config()

    if 0:
        ack_dialog = Acknowledge()
        ack_dialog.initialize('host', 'pi2', 'Acknowledge requested by App')

        if ack_dialog.exec_() == ack_dialog.Accepted:
            print('Ok')
        else:
            print('Out')
    else:
        downtime_dialog = Downtime()
        downtime_dialog.initialize('host', 'pi2', 'Downtime requested by App')

        if downtime_dialog.exec_() == downtime_dialog.Accepted:
            print('Fixed: ', downtime_dialog.fixed)
            print('Duration: ', downtime_dialog.duration_to_seconds())
            print('Start Time: ', downtime_dialog.start_time.dateTime().toTime_t())
            print('End Time: ', downtime_dialog.end_time.dateTime().toTime_t())
            print('Comment: ', downtime_dialog.comment_edit.toPlainText())
        else:
            print('Out')

    sys.exit(app.exec_())
