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
    Profile
    +++++++
    Profile manage creation of QWidget who display user profile who use Alignak-app
"""

from logging import getLogger

from PyQt5.Qt import QGridLayout, QVBoxLayout, QIcon, Qt, QLabel, QWidget, QPushButton, QScrollArea

from alignak_app.backend.backend import app_backend
from alignak_app.backend.datamanager import data_manager
from alignak_app.utils.config import settings

from alignak_app.qobjects.common.frames import AppQFrame
from alignak_app.qobjects.common.labels import get_icon_pixmap
from alignak_app.qobjects.common.buttons import ToggleQWidgetButton
from alignak_app.qobjects.common.dialogs import MessageQDialog, EditQDialog

from alignak_app.qobjects.events.events import send_event
from alignak_app.qobjects.user.password import PasswordQDialog
from alignak_app.qobjects.user.options import show_options_dialog

logger = getLogger(__name__)


class ProfileQWidget(QWidget):
    """
        Class who create QWidget for User profile.
    """

    def __init__(self, parent=None):
        super(ProfileQWidget, self).__init__(parent)
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
        self.token_btn = QPushButton()

    def initialize(self):
        """
        Initialize User QWidget

        """

        # Initialize AppQWidget
        self.app_widget = AppQFrame()
        self.app_widget.initialize(_('User View'))
        self.app_widget.add_widget(self)
        self.app_widget.setMinimumHeight(500)

        user_layout = QGridLayout()
        self.setLayout(user_layout)

        user_title = QLabel(_('User informations:'))
        user_title.setObjectName('itemtitle')
        user_layout.addWidget(user_title, 0, 0, 1, 2)

        user_layout.addWidget(self.get_informations_widget(), 1, 0, 1, 1)
        user_layout.addWidget(self.get_notes_mail_widget(), 1, 1, 1, 1)
        user_layout.addWidget(self.get_notifications_widget(), 2, 0, 1, 2)

    def get_informations_widget(self):
        """
        Create and return QWidget with user informations

        :return: main QWidget
        :rtype: QWidget
        """

        information_widget = QWidget()
        info_layout = QGridLayout()
        information_widget.setLayout(info_layout)

        title_labels = {
            'realm': QLabel(_('Realm:')),
            'is_admin': QLabel(_('Administrator:')),
            'role': QLabel(_('Role:')),
            'command': QLabel(_('Commands:')),
            'password': QLabel(_('Password')),
            'alias': QLabel(_('Alias:')),
            'token': QLabel(_('Token:')),
        }

        for label in title_labels:
            title_labels[label].setObjectName('subtitle')

        # Alias, role and realm
        info_layout.addWidget(title_labels['alias'], 0, 0, 1, 2)
        info_layout.addWidget(self.labels['alias'], 0, 1, 1, 2)

        info_layout.addWidget(title_labels['role'], 1, 0, 1, 2)
        info_layout.addWidget(self.labels['role'], 1, 1, 1, 2)

        info_layout.addWidget(title_labels['realm'], 2, 0, 1, 2)
        info_layout.addWidget(self.labels['realm'], 2, 1, 1, 2)

        # Administrator
        title_labels['is_admin'].setMinimumHeight(32)
        info_layout.addWidget(title_labels['is_admin'], 3, 0, 1, 1)
        self.labels['is_admin'].setFixedSize(14, 14)
        self.labels['is_admin'].setScaledContents(True)
        info_layout.addWidget(self.labels['is_admin'], 3, 1, 1, 1)
        info_layout.setAlignment(self.labels['is_admin'], Qt.AlignCenter)

        # Commands
        title_labels['command'].setMinimumHeight(32)
        info_layout.addWidget(title_labels['command'], 3, 2, 1, 1)
        self.labels['can_submit_commands'].setFixedSize(14, 14)
        self.labels['can_submit_commands'].setScaledContents(True)
        info_layout.addWidget(self.labels['can_submit_commands'], 3, 3, 1, 1)
        info_layout.setAlignment(self.labels['can_submit_commands'], Qt.AlignCenter)

        # Password
        info_layout.addWidget(title_labels['password'], 4, 0, 1, 1)
        password_btn = QPushButton()
        password_btn.setIcon(QIcon(settings.get_image('password')))
        password_btn.setToolTip(_('Change my password'))
        password_btn.setFixedSize(32, 32)
        password_btn.clicked.connect(lambda: self.patch_data('password'))
        info_layout.addWidget(password_btn, 4, 1, 1, 1)

        # Token (only for administrators)
        info_layout.addWidget(title_labels['token'], 4, 2, 1, 1)
        self.token_btn.setIcon(QIcon(settings.get_image('token')))
        self.token_btn.setFixedSize(32, 32)
        self.token_btn.clicked.connect(self.show_token_dialog)
        info_layout.addWidget(self.token_btn, 4, 3, 1, 1)

        return information_widget

    def get_notes_mail_widget(self):
        """
        Return QWidget with notes and email areas and edition buttons

        :return: notes and email QWidget
        :rtype: QWidget
        """

        notes_widget = QWidget()
        notes_layout = QGridLayout(notes_widget)

        # Notes title and button
        notes_label = QLabel(_('Notes:'))
        notes_label.setObjectName('subtitle')
        notes_layout.addWidget(notes_label, 0, 0, 1, 1)

        notes_btn = QPushButton()
        notes_btn.setIcon(QIcon(settings.get_image('edit')))
        notes_btn.setToolTip(_("Edit your notes."))
        notes_btn.setFixedSize(32, 32)
        notes_btn.clicked.connect(lambda: self.patch_data('notes'))
        notes_layout.addWidget(notes_btn, 0, 2, 1, 1)

        # Notes scroll area
        self.labels['notes'].setText(data_manager.database['user'].data['notes'])
        self.labels['notes'].setWordWrap(True)
        self.labels['notes'].setTextInteractionFlags(Qt.TextSelectableByMouse)
        notes_scrollarea = QScrollArea()
        notes_scrollarea.setWidget(self.labels['notes'])
        notes_scrollarea.setWidgetResizable(True)
        notes_scrollarea.setObjectName('notes')
        notes_layout.addWidget(notes_scrollarea, 1, 0, 1, 3)

        # Mail
        mail_label = QLabel(_('Email:'))
        mail_label.setObjectName('subtitle')
        notes_layout.addWidget(mail_label, 2, 0, 1, 1)
        notes_layout.addWidget(self.labels['email'], 2, 1, 1, 1)
        mail_btn = QPushButton()
        mail_btn.setIcon(QIcon(settings.get_image('edit')))
        mail_btn.setFixedSize(32, 32)
        notes_layout.addWidget(mail_btn, 2, 2, 1, 1)

        notes_layout.setAlignment(Qt.AlignTop)

        return notes_widget

    @staticmethod
    def show_token_dialog():
        """
        Show Token QDialog

        """

        token_dialog = MessageQDialog()
        token_dialog.initialize(
            _('See Token'),
            'text',
            _("<b>Token:</b> %s") % data_manager.database['user'].name.capitalize(),
            data_manager.database['user'].data['token']
        )

        token_dialog.exec_()

    def patch_data(self, patch_type):  # pragma: no cover
        """
        Display QDialogs for patches

        :param patch_type: type of patch ("notes" or "password")
        :type patch_type: str
        """

        if "notes" in patch_type:
            notes_dialog = EditQDialog()
            notes_dialog.initialize(
                _('Edit User Notes'),
                data_manager.database['user'].data['notes']
            )
            if notes_dialog.exec_() == EditQDialog.Accepted:
                data = {'notes': str(notes_dialog.text_edit.toPlainText())}
                headers = {'If-Match': data_manager.database['user'].data['_etag']}
                endpoint = '/'.join(['user', data_manager.database['user'].item_id])

                patched = app_backend.patch(endpoint, data, headers)

                if patched:
                    data_manager.database['user'].update_data(
                        'notes', notes_dialog.text_edit.toPlainText()
                    )
                    self.labels['notes'].setText(notes_dialog.text_edit.toPlainText())
                    message = _(
                        _("Your notes have been edited.")
                    )
                    send_event('INFO', message)
                else:
                    send_event(
                        'ERROR',
                        _("Backend PATCH failed, please check your logs !")
                    )
        elif "password" in patch_type:
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
        notification_widget.setMinimumHeight(150)

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
        host_notif_layout.addWidget(state_title, 1, 0, 1, 1)
        self.hostnotif_toggle_btn = ToggleQWidgetButton()
        self.hostnotif_toggle_btn.initialize()
        self.hostnotif_toggle_btn.update_btn_state(
            data_manager.database['user'].data['host_notifications_enabled']
        )
        self.hostnotif_toggle_btn.toggle_btn.clicked.connect(lambda: self.enable_notifications(
            'host_notifications_enabled', self.hostnotif_toggle_btn.is_checked()
        ))
        self.hostnotif_toggle_btn.setObjectName('host_notifications_enabled')
        host_notif_layout.addWidget(self.hostnotif_toggle_btn, 1, 1, 1, 1)
        host_notif_layout.setAlignment(self.hostnotif_toggle_btn, Qt.AlignRight)

        period_title = QLabel(_('Notification period:'))
        period_title.setObjectName('subtitle')
        host_notif_layout.addWidget(period_title, 2, 0, 1, 1)
        self.labels['host_notification_period'].setText(
            data_manager.get_period_name(
                data_manager.database['user'].data['host_notification_period']
            )
        )
        host_notif_layout.addWidget(self.labels['host_notification_period'], 2, 1, 1, 1)

        option_btn = QPushButton()
        option_btn.setIcon(QIcon(settings.get_image('options')))
        option_btn.setFixedSize(64, 32)
        option_btn.clicked.connect(lambda: show_options_dialog(
            'host',
            data_manager.database['user'].data['host_notification_options']
        ))

        host_notif_layout.addWidget(option_btn, 3, 0, 1, 2)
        host_notif_layout.setAlignment(option_btn, Qt.AlignCenter)

        return host_notif_widget

    def get_services_notif_widget(self):
        """
        Create and return notification QWidget for services

        :return: services notification QWidget
        :rtype: QWidget
        """

        svc_notif_widget = QWidget()
        svc_notif_layout = QGridLayout()
        svc_notif_widget.setLayout(svc_notif_layout)

        notif_title = QLabel(_('Services notifications configurations'))
        notif_title.setObjectName('itemtitle')
        svc_notif_layout.addWidget(notif_title, 0, 0, 1, 2)

        state_title = QLabel(_('Notification enabled:'))
        state_title.setObjectName("subtitle")
        svc_notif_layout.addWidget(state_title, 1, 0, 1, 1)
        self.servicenotif_toggle_btn = ToggleQWidgetButton()
        self.servicenotif_toggle_btn.initialize()
        self.servicenotif_toggle_btn.update_btn_state(
            data_manager.database['user'].data['service_notifications_enabled']
        )
        self.servicenotif_toggle_btn.toggle_btn.clicked.connect(lambda: self.enable_notifications(
            'service_notifications_enabled', self.servicenotif_toggle_btn.is_checked()
        ))
        svc_notif_layout.addWidget(self.servicenotif_toggle_btn, 1, 1, 1, 1)
        svc_notif_layout.setAlignment(self.servicenotif_toggle_btn, Qt.AlignRight)

        period_title = QLabel(_('Notification period:'))
        period_title.setObjectName('subtitle')
        svc_notif_layout.addWidget(period_title, 2, 0, 1, 1)
        self.labels['service_notification_period'].setText(
            data_manager.get_period_name(
                data_manager.database['user'].data['service_notification_period']
            )
        )
        svc_notif_layout.addWidget(self.labels['service_notification_period'], 2, 1, 1, 1)

        option_btn = QPushButton()
        option_btn.setIcon(QIcon(settings.get_image('options')))
        option_btn.setFixedSize(64, 32)
        option_btn.clicked.connect(lambda: show_options_dialog(
            'service',
            data_manager.database['user'].data['service_notification_options']
        ))

        svc_notif_layout.addWidget(option_btn, 3, 0, 1, 2)
        svc_notif_layout.setAlignment(option_btn, Qt.AlignCenter)

        return svc_notif_widget

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
            enabled = _('enabled') if notification_enabled else _('disabled')
            event_type = 'OK' if notification_enabled else 'WARN'
            message = _("Notifications for %ss are %s") % (
                notification_type.replace('_notifications_enabled', ''),
                enabled
            )
            if 'host' in notification_type:
                self.hostnotif_toggle_btn.update_btn_state(btn_state)
            else:
                self.servicenotif_toggle_btn.update_btn_state(btn_state)
            send_event(event_type, message, timer=True)
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
