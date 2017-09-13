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
    Banner send some banner notifications with a message.
"""

from logging import getLogger

from datetime import datetime

from alignak_app.core.utils import get_image_path, get_app_config, get_css

from PyQt5.QtWidgets import QHBoxLayout, QApplication  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel  # pylint: disable=no-name-in-module
from PyQt5.Qt import Qt, QIcon, QTimer, QPoint  # pylint: disable=no-name-in-module
from PyQt5.Qt import pyqtSignal  # pylint: disable=no-name-in-module
from PyQt5.QtCore import QPropertyAnimation  # pylint: disable=no-name-in-module


logger = getLogger(__name__)


class BannerManager(object):
    """
        Class who send and manage banners
    """

    def __init__(self):
        self.banners = []
        self.banners_to_send = []
        self.timer = None

    def start(self):
        """
        Start manager. Manager checks if there is banner to send or not.

        """

        self.timer = QTimer()
        self.timer.start(4000)
        self.timer.timeout.connect(self.check_banners)

    def check_banners(self):
        """
        Check banners to send

        """

        total_height_banner = len(self.banners) * Banner.banner_height

        if self.banners_to_send:
            if total_height_banner > QApplication.desktop().screenGeometry().height():
                pass
            else:
                for visible_banner in self.banners:
                    pos = visible_banner.pos()
                    visible_banner.move(pos.x(), pos.y() + visible_banner.height())

                banner = self.banners_to_send[0]
                banner.animation.start()
                banner.banner_closed.connect(self.banner_listener)

                banner.show()
                if banner.timer:
                    banner.start_timer()

                self.banners_to_send.remove(banner)
                self.banners.append(banner)

    def add_banner(self, level, message, duration=0):
        """
        Add Banner() to send in BannerManager

        :param level: OK, INFO, WARN, ALERT or ERROR
        :type level: str
        :param message: message to display
        :type message: str
        :param duration: duration before close banner
        :type duration: int
        """

        banner = Banner()
        banner.create_banner(level, message)
        if duration:
            banner.timer = duration
        self.banners_to_send.append(banner)

    def banner_listener(self, sender):
        """
        Listener who listen if banner is "banner_closed"

        :param sender: the banner who emit "banner_closed" signal
        :type sender: Banner
        """

        self.remove_banner(sender)

    def remove_banner(self, banner):
        """
        Close and remove a banner. Move leaving banners
        :param banner: banner to remove
        :type banner: Banner
        """

        # Shift banners when one is removed
        if banner in self.banners:
            self.banners.remove(banner)

        for visible_banner in self.banners:
            if (visible_banner.pos().y() - banner.pos().y()) >= Banner.banner_height:
                pos = visible_banner.pos()
                visible_banner.move(pos.x(), pos.y() - visible_banner.height())

        banner.close()


class Banner(QWidget):
    """
        Class who create a banner.
    """

    banner_closed = pyqtSignal(QWidget, name='banner')
    banner_height = 50
    banner_width = 450

    def __init__(self, parent=None):
        super(Banner, self).__init__(parent)
        self.setFixedSize(self.banner_width, self.banner_height)
        self.setWindowFlags(Qt.SplashScreen)
        # Animation
        self.animation = QPropertyAnimation(self, b'pos')
        self.banner_type = ['OK', 'INFO', 'WARN', 'ALERT']
        self.timer = 0

    def create_banner(self, banner_type, message):
        """
        Create banner QWidget and its QPropertyAnimation

        :param banner_type: defines type of banner: OK, INFO, WARN, or ALERT
        :type banner_type: str
        :param message: message to display in banner
        :type message: str
        """

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        event_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.setToolTip(event_date)

        if banner_type not in self.banner_type:
            banner_type = 'ERROR'

        self.setStyleSheet(get_css())
        self.setObjectName('banner%s' % banner_type)

        valid_btn = QPushButton()
        valid_btn.setMaximumSize(self.banner_height, self.banner_height)
        valid_btn.setObjectName('banner')
        valid_btn.clicked.connect(self.close_banner)
        valid_btn.setIcon(QIcon(get_image_path(banner_type.lower())))

        layout.addWidget(valid_btn)

        if len(message) > 170:
            message = message[:170] + '...'

        if get_app_config('Banners', 'title', boolean=True):
            banner_qlabel = QLabel('<b>%s</b>: %s' % (banner_type, message))
        else:
            banner_qlabel = QLabel('%s' % message)

        banner_qlabel.setWordWrap(True)
        banner_qlabel.setObjectName('banner')
        layout.addWidget(banner_qlabel)

        # Animation
        banner_duration = int(get_app_config('Banners', 'animation'))
        if banner_duration < 0:
            logger.debug('Banner animation: %sms', str(banner_duration))
            logger.error(
                '"animation" option must be equal or greater than 0. Replace by default: 1000ms'
            )
            banner_duration = 1000
        self.animation.setDuration(banner_duration)

        start_value = QPoint(0, 0)
        self.animation.setStartValue(start_value)

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        end_position = QApplication.desktop().screenGeometry(screen).topRight()
        end_value = QPoint(
            end_position.x() - self.width(),
            end_position.y()
        )
        self.animation.setEndValue(end_value)

    def start_timer(self):
        """
        Start timer to close banner

        """

        timer = QTimer(self)

        timer.timeout.connect(self.close_banner)
        timer.setSingleShot(True)
        timer.start(int(self.timer))

    def close_banner(self):
        """
        Send signal to manager to close banner

        """

        self.banner_closed.emit(self)

# Main instance of BannerManager()
bannerManager = BannerManager()


def send_banner(level, message, duration=0):
    """
    Direct access to send a banner

    :param level: INFO, OK, WARN or ALERT defines color of banner
    :type level: str
    :param message: message to display in banner
    :type message: str
    :param duration: duration before close banner
    :type duration: int
    """

    bannerManager.add_banner(level, message, duration)


def get_hosts_level_banner(msg):
    """
    Return the level of the banner for hosts

    :param msg: msg to parse
    :type msg: str
    :return: the level of banner
    :rtype: str
    """

    if 'UP: <b>+' in msg:
        level = 'OK'
    elif 'UNREACHABLE: <b>+' in msg:
        level = 'WARN'
    elif 'DOWN: <b>+' in msg:
        level = 'ALERT'
    else:
        level = 'INFO'

    return level


def get_services_level_banner(msg):
    """
    Return the level of the banner for services

    :param msg: msg to parse
    :type msg: str
    :return: the level of banner
    :rtype: str
    """

    if 'OK: <b>+' in msg:
        level = 'OK'
    elif 'WARNING: <b>+' in msg or 'UNKNOWN: <b>+' in msg:
        level = 'WARN'
    elif 'CRITICAL: <b>+' in msg or 'UNREACHABLE: <b>+' in msg:
        level = 'ALERT'
    else:
        level = 'INFO'

    return level


def send_diff_banners(diff):
    """
    Send banners for hosts and services diff since the last check

    :param diff: dict of diff for hosts and services
    :type diff: dict
    """

    hi = 1
    hosts_msg = ''
    for host_state in diff['hosts']:
        if diff['hosts'][host_state]:
            if hi % 2:
                hosts_msg += 'Hosts %s: <b>%s</b>, ' % (
                    str(host_state).upper(),
                    "{0:+d}".format(diff['hosts'][host_state])
                )
            else:
                hosts_msg += 'Hosts %s: <b>%s</b><br>' % (
                    str(host_state).upper(),
                    "{0:+d}".format(diff['hosts'][host_state])
                )
            hi += 1

    si = 1
    services_msg = ''
    for service_state in diff['services']:
        if diff['services'][service_state]:
            if si % 2:
                services_msg += 'Services %s: <b>%s</b>, ' % (
                    str(service_state).upper(),
                    "{0:+d}".format(diff['services'][service_state])
                )
            else:
                services_msg += 'Services %s: <b>%s</b><br>' % (
                    str(service_state).upper(),
                    "{0:+d}".format(diff['services'][service_state])
                )
            si += 1

    hosts_lvl = get_hosts_level_banner(hosts_msg)
    services_lvl = get_services_level_banner(services_msg)

    duration = int(get_app_config('Banners', 'duration'))
    if bool(duration) and duration > 0:
        duration *= 1000
    else:
        duration = 0

    if hosts_msg:
        send_banner(hosts_lvl, hosts_msg, duration=duration)
    if services_msg:
        send_banner(services_lvl, services_msg, duration=duration)
