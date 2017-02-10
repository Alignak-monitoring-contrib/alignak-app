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

from alignak_app.core.utils import get_image_path

try:
    __import__('PyQt5')
    from PyQt5.QtWidgets import QHBoxLayout, QApplication  # pylint: disable=no-name-in-module
    from PyQt5.QtWidgets import QWidget, QPushButton, QLabel  # pylint: disable=no-name-in-module
    from PyQt5.Qt import Qt, QIcon, QTimer, QPoint  # pylint: disable=no-name-in-module
    from PyQt5.Qt import QObject, pyqtSignal  # pylint: disable=no-name-in-module
    from PyQt5.QtCore import QPropertyAnimation  # pylint: disable=no-name-in-module
except ImportError:  # pragma: no cover
    from PyQt4.Qt import QHBoxLayout, QApplication  # pylint: disable=import-error
    from PyQt4.Qt import QWidget, QPushButton, QLabel  # pylint: disable=import-error
    from PyQt4.Qt import Qt, QTimer, QPoint, QIcon  # pylint: disable=import-error
    from PyQt4.Qt import QObject, pyqtSignal  # pylint: disable=import-error
    from PyQt4.QtCore import QPropertyAnimation  # pylint: disable=import-error


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

                self.banners_to_send.remove(banner)
                self.banners.append(banner)

    def add_banner(self, level, message):
        """
        Add Banner() to send in BannerManager

        :param level: OK, WARN, or ALERT
        :type level: str
        :param message: message to display
        :type message: str
        """

        banner = Banner()
        banner.create_banner(level, message)
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

    banner_closed = pyqtSignal(QObject)
    banner_height = 50
    banner_width = 400

    def __init__(self, parent=None):
        super(Banner, self).__init__(parent)
        self.setFixedSize(self.banner_width, self.banner_height)
        self.setWindowFlags(Qt.SplashScreen)
        # Animation
        self.animation = QPropertyAnimation(self, b'pos')
        # Color model
        self.color_levels = {
            'OK': {
                'color': '#27ae60',
                'title': 'OK'
            },
            'INFO': {
                'color': '#3884c3',
                'title': 'INFO'
            },
            'WARN': {
                'color': '#e67e22',
                'title': 'WARN'
            },
            'ALERT': {
                'color': '#e74c3c',
                'title': 'ALERT'
            }
        }

    def create_banner(self, level, message):
        """
        Create banner QWidget and QPropertyAnimation

        :param level: OK, WARN, or ALERT defines color of banner
        :type level: str
        :param message: message to display in banner
        :type message: str
        """

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setToolTip(message)

        try:
            color = self.color_levels[level]['color']
            title = self.color_levels[level]['title']
        except KeyError:
            color = '#383838'
            title = 'ERROR'

        self.setStyleSheet(
            """
            QWidget {
                background-color: %s;
                color: white;
                border: 1px solid #d2d2d2;
                font-size: 14px;
            }
            """ % color)

        valid_btn = QPushButton()
        valid_btn.setMaximumSize(self.banner_height, self.banner_height)
        valid_btn.setStyleSheet(
            """
                border: 1px solid #d2d2d2;
                border-radius: 0px;
            """
        )
        valid_btn.clicked.connect(self.close_banner)
        valid_btn.setIcon(QIcon(get_image_path('banner')))

        layout.addWidget(valid_btn)

        if len(message) > 80:
            message = message[:80] + '...'

        banner_qlabel = QLabel('<b>%s</b>: %s' % (title, message))
        banner_qlabel.setWordWrap(True)
        layout.addWidget(banner_qlabel)

        # Animation
        start_value = QPoint(0, 0)
        self.animation.setDuration(1000)
        self.animation.setStartValue(start_value)

        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        end_position = QApplication.desktop().screenGeometry(screen).topRight()
        end_value = QPoint(
            end_position.x() - self.width(),
            end_position.y()
        )
        self.animation.setEndValue(end_value)

    def close_banner(self):
        """
        Send signal to manager to close banner

        """

        self.banner_closed.emit(self)

# Main instance of BannerManager()
bannerManager = BannerManager()


def send_banner(level, message):
    """
    Direct access to send a banner

    :param level: INFO, OK, WARN or ALERT defines color of banner
    :type level: str
    :param message: message to display in banner
    :type message: str
    """

    bannerManager.add_banner(level, message)
