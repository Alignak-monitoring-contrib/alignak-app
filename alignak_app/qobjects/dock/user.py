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
    User
    ++++
    User manage creation of QWidget who display user profile who use Alignak-app
"""

from logging import getLogger

from PyQt5.Qt import QGridLayout, QVBoxLayout, QIcon, Qt, QLabel, QWidget, QPushButton, QScrollArea

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.frames import AppQFrame, get_frame_separator
from alignak_app.qobjects.common.labels import get_icon_pixmap
from alignak_app.qobjects.common.buttons import ToggleQWidgetButton
from alignak_app.qobjects.dock.events import send_event
from alignak_app.qobjects.dock.password import PasswordQDialog
from alignak_app.qobjects.dock.token import TokenQDialog
from alignak_app.qobjects.dock.user_notes import UserNotesQDialog
from alignak_app.qobjects.dock.user_options import show_options_dialog

logger = getLogger(__name__)


class UserQWidget(QWidget):
    """
        Class who create QWidget for User profile.
    """

    def __init__(self, parent=None):
        super(UserQWidget, self).__init__(parent)
        # Fields
        self.labels = {
            'realm': QLabel(),
            'role': QLabel(),
            'email': QLabel(),
            'is_admin': QLabel(),
            'can_submit_commands': QLabel(),
            'alias': QLabel(),
            'notes': QLabel(),
            'host_notifications_enabled': QLabel(),
            'host_notification_period': QLabel(),
            'service_notifications_enabled': QLabel(),
            'service_notification_period': QLabel(),
        }
        self.app_widget = None
        self.hostnotif_toggle_btn = None
        self.servicenotif_toggle_btn = None
        self.password_btn = QPushButton()
        self.token_btn = QPushButton()
        self.notes_btn = QPushButton()

    def initialize(self):
        """
        Initialize User QWidget

        """

        # Initialize AppQWidget
        self.app_widget = AppQFrame()
        self.app_widget.initialize(_('User View'))
        self.app_widget.add_widget(self)
        self.app_widget.setMinimumHeight(500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.get_informations_widget())
        layout.addWidget(self.get_notifications_widget())

    def get_informations_widget(self):
        """
        Create and return QWidget with user informations

        :return: main QWidget
        :rtype: QWidget
        """

        information_widget = QWidget()
        info_layout = QGridLayout()
        information_widget.setLayout(info_layout)

        # Main title
        main_title = QLabel(_('User informations:'))
        main_title.setObjectName("itemtitle")
        info_layout.addWidget(main_title, 0, 0, 1, 6)
        info_layout.setAlignment(main_title, Qt.AlignCenter)

        # Realm & Is Admin & Notes title and button
        line = 2
        realm_title = QLabel(_('Realm:'))
        realm_title.setObjectName("subtitle")
        info_layout.addWidget(realm_title, line, 0, 1, 1)
        info_layout.addWidget(self.labels['realm'], line, 1, 1, 1)

        admin_title = QLabel(_('Administrator:'))
        admin_title.setObjectName("subtitle")
        admin_title.setMinimumHeight(32)
        info_layout.addWidget(admin_title, line, 2, 1, 1)
        self.labels['is_admin'].setFixedSize(14, 14)
        self.labels['is_admin'].setScaledContents(True)
        info_layout.addWidget(self.labels['is_admin'], line, 3, 1, 1)
        info_layout.setAlignment(self.labels['is_admin'], Qt.AlignCenter)

        notes_title = QLabel(_('Notes:'))
        notes_title.setObjectName("title")
        info_layout.addWidget(notes_title, line, 4, 1, 1)

        self.notes_btn.setIcon(QIcon(settings.get_image('edit')))
        self.notes_btn.setToolTip(_("Edit your notes."))
        self.notes_btn.setObjectName("notes")
        self.notes_btn.setFixedSize(32, 32)
        self.notes_btn.clicked.connect(self.patch_data)
        info_layout.addWidget(self.notes_btn, line, 5, 1, 1)
        line += 1

        # Role & Can submit commands
        role_title = QLabel(_('Role:'))
        role_title.setObjectName("subtitle")
        info_layout.addWidget(role_title, line, 0, 1, 1)
        info_layout.addWidget(self.labels['role'], line, 1, 1, 1)

        command_title = QLabel(_('Commands:'))
        command_title.setObjectName("subtitle")
        command_title.setMinimumHeight(32)
        info_layout.addWidget(command_title, line, 2, 1, 1)
        self.labels['can_submit_commands'].setFixedSize(14, 14)
        self.labels['can_submit_commands'].setScaledContents(True)
        info_layout.addWidget(self.labels['can_submit_commands'], line, 3, 1, 1)
        info_layout.setAlignment(self.labels['can_submit_commands'], Qt.AlignCenter)

        # Create QLabel for notes
        info_layout.addWidget(self.get_notes_scrollarea(), line, 4, 3, 2)
        info_layout.setAlignment(Qt.AlignTop)
        line += 1

        # Mail & Password
        mail_title = QLabel(_('Email:'))
        mail_title.setObjectName("subtitle")
        info_layout.addWidget(mail_title, line, 0, 1, 1)
        info_layout.addWidget(self.labels['email'], line, 1, 1, 1)

        password_title = QLabel(_('Password:'))
        password_title.setObjectName("subtitle")
        info_layout.addWidget(password_title, line, 2, 1, 1)

        self.password_btn.setObjectName("password")
        self.password_btn.clicked.connect(self.patch_data)
        self.password_btn.setIcon(QIcon(settings.get_image('password')))
        self.password_btn.setToolTip(_('Change my password'))
        self.password_btn.setFixedSize(32, 32)
        info_layout.addWidget(self.password_btn, line, 3, 1, 1)
        line += 1

        # Alias & Token (only for administrators)
        alias_title = QLabel(_('Alias:'))
        alias_title.setObjectName("subtitle")
        info_layout.addWidget(alias_title, line, 0, 1, 1)
        info_layout.addWidget(self.labels['alias'], line, 1, 1, 1)

        token_title = QLabel(_('Token:'))
        token_title.setObjectName("subtitle")
        info_layout.addWidget(token_title, line, 2, 1, 2)

        self.token_btn.setIcon(QIcon(settings.get_image('token')))
        self.token_btn.setFixedSize(32, 32)
        self.token_btn.clicked.connect(self.show_token_dialog)
        info_layout.addWidget(self.token_btn, line, 3, 1, 1)

        return information_widget

    def get_notes_scrollarea(self):
        """
        Return QScrollArea widget for user notes

        :return: user notes QScrollArea
        :rtype: QScrollArea
        """

        # Create QLabel for notes
        self.labels['notes'].setText(data_manager.database['user'].data['notes'])
        self.labels['notes'].setWordWrap(True)
        self.labels['notes'].setTextInteractionFlags(Qt.TextSelectableByMouse)
        notes_scrollarea = QScrollArea()
        notes_scrollarea.setWidget(self.labels['notes'])
        notes_scrollarea.setWidgetResizable(True)
        notes_scrollarea.setObjectName('notes')

        return notes_scrollarea

    @staticmethod
    def show_token_dialog():
        """
        Show TokenQDialog

        """

        token_dialog = TokenQDialog()
        token_dialog.initialize()

        token_dialog.exec_()

    def patch_data(self):  # pragma: no cover
        """
        Hide and show QLabel for notes or PATCH password

        """

        btn = self.sender()

        if "notes" in btn.objectName():
            notes_dialog = UserNotesQDialog()
            notes_dialog.initialize(data_manager.database['user'].data['notes'])
            if notes_dialog.exec_() == UserNotesQDialog.Accepted:
                data = {'notes': str(notes_dialog.notes_edit.toPlainText())}
                headers = {'If-Match': data_manager.database['user'].data['_etag']}
                endpoint = '/'.join(['user', data_manager.database['user'].item_id])

                patched = app_backend.patch(endpoint, data, headers)

                if patched:
                    data_manager.database['user'].update_data(
                        'notes', notes_dialog.notes_edit.toPlainText()
                    )
                    self.labels['notes'].setText(notes_dialog.notes_edit.toPlainText())
                    message = _(
                        _("Your notes have been edited.")
                    )
                    send_event('INFO', message)
                else:
                    send_event(
                        'ERROR',
                        _("Backend PATCH failed, please check your logs !")
                    )
        elif "password" in btn.objectName():
            pass_dialog = PasswordQDialog()
            pass_dialog.initialize()

            if pass_dialog.exec_() == PasswordQDialog.Accepted:
                new_password = pass_dialog.pass_edit.text()

                data = {'password': str(new_password)}
                headers = {'If-Match': data_manager.database['user'].data['_etag']}
                endpoint = '/'.join(['user', data_manager.database['user'].item_id])

                patched = app_backend.patch(endpoint, data, headers)

                if patched:
                    message = _("Your password has been updated !")
                    send_event('OK', message)
                else:
                    send_event(
                        'ERROR', _("Backend PATCH failed, please check your logs !")
                    )
        else:
            logger.error("Wrong sender in UserQWidget.patch_data() !")

    def get_notifications_widget(self):
        """
        Create and return notification QWidget for hosts and services

        :return: notifications QWidget
        :rtype: QWidget
        """

        notification_widget = QWidget()
        notification_layout = QGridLayout()
        notification_widget.setLayout(notification_layout)

        host_notif_widget = self.get_hosts_notif_widget()
        notification_layout.addWidget(host_notif_widget, 0, 0, 1, 1)

        services_notif_widget = self.get_services_notif_widget()
        notification_layout.addWidget(services_notif_widget, 0, 1, 1, 1)

        return notification_widget

    def get_hosts_notif_widget(self):
        """
        Create and return notification QWidget for hosts

        :return: hosts notification QWidget
        :rtype: QWidget
        """

        host_notif_widget = QWidget()
        host_notif_layout = QGridLayout()
        host_notif_widget.setLayout(host_notif_layout)

        notif_title = QLabel(_('Hosts notifications configurations'))
        notif_title.setObjectName('itemtitle')
        host_notif_layout.addWidget(notif_title, 0, 0, 1, 2)

        state_title = QLabel(_("Notification enabled:"))
        state_title.setObjectName("subtitle")
        host_notif_layout.addWidget(state_title, 2, 0, 1, 1)
        self.hostnotif_toggle_btn = ToggleQWidgetButton()
        self.hostnotif_toggle_btn.initialize()
        self.hostnotif_toggle_btn.update_btn_state(
            data_manager.database['user'].data['host_notifications_enabled']
        )
        self.hostnotif_toggle_btn.toggle_btn.clicked.connect(lambda: self.enable_notifications(
            'host_notifications_enabled', self.hostnotif_toggle_btn.get_btn_state()
        ))
        self.hostnotif_toggle_btn.setObjectName('host_notifications_enabled')
        host_notif_layout.addWidget(self.hostnotif_toggle_btn, 2, 1, 1, 1)

        period_title = QLabel(_('Notification period:'))
        period_title.setObjectName('subtitle')
        host_notif_layout.addWidget(period_title, 3, 0, 1, 1)
        self.labels['host_notification_period'].setText(
            data_manager.get_period_name(
                data_manager.database['user'].data['host_notification_period']
            )
        )
        host_notif_layout.addWidget(self.labels['host_notification_period'], 3, 1, 1, 1)

        option_btn = QPushButton()
        option_btn.setIcon(QIcon(settings.get_image('options')))
        option_btn.setFixedSize(64, 32)
        option_btn.clicked.connect(lambda: show_options_dialog(
            'host',
            data_manager.database['user'].data['host_notification_options']
        ))

        host_notif_layout.addWidget(option_btn, 4, 0, 1, 2)
        host_notif_layout.setAlignment(option_btn, Qt.AlignCenter)

        return host_notif_widget

    def get_services_notif_widget(self):
        """
        Create and return notification QWidget for services

        :return: services notification QWidget
        :rtype: QWidget
        """

        service_notif_widget = QWidget()
        service_notif_layout = QGridLayout()
        service_notif_widget.setLayout(service_notif_layout)

        notif_title = QLabel(_('Services notifications configurations'))
        notif_title.setObjectName('itemtitle')
        service_notif_layout.addWidget(notif_title, 0, 0, 1, 2)

        state_title = QLabel(_('Notification enabled:'))
        state_title.setObjectName("subtitle")
        service_notif_layout.addWidget(state_title, 2, 0, 1, 1)
        self.servicenotif_toggle_btn = ToggleQWidgetButton()
        self.servicenotif_toggle_btn.initialize()
        self.servicenotif_toggle_btn.update_btn_state(
            data_manager.database['user'].data['service_notifications_enabled']
        )
        self.servicenotif_toggle_btn.toggle_btn.clicked.connect(lambda: self.enable_notifications(
            'service_notifications_enabled', self.servicenotif_toggle_btn.get_btn_state()
        ))
        service_notif_layout.addWidget(self.servicenotif_toggle_btn, 2, 1, 1, 1)

        period_title = QLabel(_('Notification period:'))
        period_title.setObjectName('subtitle')
        service_notif_layout.addWidget(period_title, 3, 0, 1, 1)
        self.labels['service_notification_period'].setText(
            data_manager.get_period_name(
                data_manager.database['user'].data['service_notification_period']
            )
        )
        service_notif_layout.addWidget(self.labels['service_notification_period'], 3, 1, 1, 1)

        option_btn = QPushButton()
        option_btn.setIcon(QIcon(settings.get_image('options')))
        option_btn.setFixedSize(64, 32)
        option_btn.clicked.connect(lambda: show_options_dialog(
            'service',
            data_manager.database['user'].data['service_notification_options']
        ))

        service_notif_layout.addWidget(option_btn, 4, 0, 1, 2)
        service_notif_layout.setAlignment(option_btn, Qt.AlignCenter)

        return service_notif_widget

    def enable_notifications(self, notification_type, btn_state):  # pragma: no cover
        """
        Enable notification for the wanted type: hosts or services

        """

        notification_enabled = btn_state

        data = {notification_type: notification_enabled}
        headers = {'If-Match': data_manager.database['user'].data['_etag']}
        endpoint = '/'.join(['user', data_manager.database['user'].item_id])

        patched = app_backend.patch(endpoint, data, headers)

        if patched:
            data_manager.database['user'].update_data(notification_type, notification_enabled)
            enabled = 'enabled' if notification_enabled else 'disabled'
            message = _("Notifications for %ss are %s") % (
                notification_type.replace('_notifications_enabled', ''),
                enabled
            )
            if 'host' in notification_type:
                self.hostnotif_toggle_btn.update_btn_state(btn_state)
            else:
                self.servicenotif_toggle_btn.update_btn_state(btn_state)
            send_event('INFO', message, timer=True)
        else:
            send_event(
                'ERROR',
                _("Backend PATCH failed, if problem persist, please check your logs !")
            )

    def update_widget(self):
        """
        Update UserQWidget

        """

        # Realm, Role, Email
        self.labels['realm'].setText(
            data_manager.get_realm_name(data_manager.database['user'].data['_realm'])
        )
        self.labels['role'].setText(data_manager.database['user'].get_role().capitalize())
        self.labels['email'].setText(data_manager.database['user'].data['email'])

        # Admin, Commands
        self.labels['is_admin'].setPixmap(
            get_icon_pixmap(data_manager.database['user'].data['is_admin'], ['checked', 'error'])
        )
        self.labels['can_submit_commands'].setPixmap(
            get_icon_pixmap(
                data_manager.database['user'].data['can_submit_commands'],
                ['checked', 'error']
            )
        )

        # Alias, Notes, Token
        self.labels['alias'].setText(data_manager.database['user'].data['alias'])

        if data_manager.database['user'].data['is_admin']:
            self.token_btn.setEnabled(True)
            self.token_btn.setToolTip(_('See my token'))
        else:
            self.token_btn.setEnabled(False)
            self.token_btn.setToolTip(_('Token is only available for Administrators !'))
