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
    User manage QWidget who display User Profile.
"""

from logging import getLogger

from PyQt5.Qt import QIcon, QPixmap, Qt, pyqtSignal  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QLabel, QLineEdit, QDialog  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox  # pylint: disable=no-name-in-module

from alignak_app.core.utils import get_image_path, get_css
from alignak_app.user.password import PasswordDialog
from alignak_app.widgets.app_widget import AppQWidget
from alignak_app.widgets.banner import send_banner

logger = getLogger(__name__)


class UserProfile(QWidget):
    """
        Class who create QWidget for User Profile.
    """

    update_profile = pyqtSignal(name='userprofile')

    def __init__(self, app_backend, parent=None):
        super(UserProfile, self).__init__(parent)
        self.setStyleSheet(get_css())
        # Fields
        self.app_backend = app_backend
        self.user = {}
        self.app_widget = None
        self.host_notif_state = None
        self.service_notif_state = None
        self.password_btn = None
        self.notes_btn = None
        self.notes_data = None
        self.notes_edit = None

    def initialize(self):
        """
        Initialize User QWidget

        """

        # Get user data first to prevent user is None
        self.get_user_data()

        # Initialize AppQWidget
        self.app_widget = AppQWidget()
        self.app_widget.initialize(_('User View'))
        self.app_widget.add_widget(self)

        # first creation of QWidget
        self.create_widget(True)

    def create_widget(self, first=False):
        """
        Create or update the user QWidget. Separate function from initialize() for pyqtSignal

        """

        # Refresh the user data if not first start
        if not first:
            self.get_user_data()

        if self.layout():
            # Clean layout
            for i in reversed(range(self.layout().count())):
                self.layout().itemAt(i).widget().deleteLater()
            layout = self.layout()
        else:
            layout = QVBoxLayout()
            self.setLayout(layout)

        layout.addWidget(self.get_main_user_widget())
        layout.addWidget(self.get_notes_widget())

        layout.addWidget(self.get_notifications_widget())

    def get_user_data(self):
        """
        Get and set the user data

        """

        projection = [
            '_realm',
            'is_admin',
            'back_role_super_admin',
            'alias',
            'name',
            'notes',
            'email',
            'can_submit_commands',
            'token',
            'host_notifications_enabled',
            'service_notifications_enabled',
            'host_notification_period',
            'service_notification_period',
            'host_notification_options',
            'service_notification_options',
        ]

        self.user = self.app_backend.get_user(projection)

        if not self.user:
            for key in projection:
                self.user[key] = 'n/a'

    def get_main_user_widget(self):
        """
        Create and return QWidget with main informations

        :return: main QWidget
        :rtype: QWidget
        """

        main_user_widget = QWidget()
        main_layout = QGridLayout()
        main_user_widget.setLayout(main_layout)

        main_title = QLabel(_('Main informations:'))
        main_title.setObjectName("usertitle")
        main_layout.addWidget(main_title, 0, 0, 1, 2)

        rights_title = QLabel(_('Rights:'))
        rights_title.setObjectName("usertitle")
        main_layout.addWidget(rights_title, 0, 2, 1, 2)

        main_layout.addWidget(self.get_information_widget(), 1, 0, 1, 2)
        main_layout.addWidget(self.get_rights_widget(), 1, 2, 1, 2)

        return main_user_widget

    def get_information_widget(self):
        """
        Return informations QWidget

        :return: information QWidget
        :rtype: QWidget
        """

        information_widget = QWidget()
        info_layout = QGridLayout()
        information_widget.setLayout(info_layout)

        realm_title = QLabel(_('Realm:'))
        realm_title.setObjectName("usersubtitle")
        info_layout.addWidget(realm_title, 0, 0, 1, 1)
        realm_data = QLabel(self.get_realm_name())
        info_layout.addWidget(realm_data, 0, 1, 1, 1)

        role_title = QLabel(_('Role:'))
        role_title.setObjectName("usersubtitle")
        info_layout.addWidget(role_title, 1, 0, 1, 1)
        role_data = QLabel(self.get_role().capitalize())
        info_layout.addWidget(role_data, 1, 1, 1, 1)

        mail_title = QLabel(_('Email:'))
        mail_title.setObjectName("usersubtitle")
        info_layout.addWidget(mail_title, 2, 0, 1, 1)
        mail_data = QLabel(self.user['email'])
        info_layout.addWidget(mail_data, 2, 1, 1, 1)

        return information_widget

    def get_rights_widget(self):
        """
        Create and return Rights QWidget

        :return: rights QWidget
        :rtype: QWidget
        """

        rights_widget = QWidget()
        rights_layout = QGridLayout()
        rights_widget.setLayout(rights_layout)

        admin_title = QLabel(_('Administrator:'))
        admin_title.setObjectName("usersubtitle")
        admin_title.setMinimumHeight(32)
        rights_layout.addWidget(admin_title, 1, 0, 1, 1)
        admin_data = self.get_enable_label_icon(
            self.user['is_admin']
        )
        rights_layout.addWidget(admin_data, 1, 1, 1, 1)

        command_title = QLabel(_('Commands:'))
        command_title.setObjectName("usersubtitle")
        command_title.setMinimumHeight(32)
        rights_layout.addWidget(command_title, 2, 0, 1, 1)
        command_data = self.get_enable_label_icon(
            self.user['can_submit_commands']
        )
        rights_layout.addWidget(command_data, 2, 1, 1, 1)

        password_title = QLabel(_('Password:'))
        password_title.setObjectName("usersubtitle")
        rights_layout.addWidget(password_title, 3, 0, 1, 1)
        self.password_btn = QPushButton()
        self.password_btn.setObjectName("password")
        self.password_btn.clicked.connect(self.button_clicked)
        self.password_btn.setIcon(QIcon(get_image_path('password')))
        self.password_btn.setFixedSize(32, 32)
        rights_layout.addWidget(self.password_btn, 3, 1, 1, 1)

        return rights_widget

    def get_realm_name(self):
        """
        Return realm name or alias

        :return: realm name or alias
        :rtype: str
        """

        if '_realm' in self.user:
            endpoint = '/'.join(['realm', self.user['_realm']])
            projection = [
                'name',
                'alias'
            ]

            realm = self.app_backend.get(endpoint, projection=projection)

            if realm:
                if realm['alias']:
                    return realm['alias']

                return realm['name']

        return 'n/a'

    def get_role(self):
        """
        Get user role

        :return: role of user
        :rtype: str
        """

        role = _('user')

        if self.user['is_admin'] or self.user['back_role_super_admin']:
            role = _('administrator')
        if self.user['can_submit_commands'] and not \
                self.user['is_admin'] and not self.user['back_role_super_admin']:
            role = _('power')

        return role

    def get_notes_widget(self):
        """
        Create and return Notes QWidget

        :return: notes QWidget
        :rtype: QWidget
        """

        notes_widget = QWidget()
        notes_layout = QGridLayout()
        notes_widget.setLayout(notes_layout)

        main_notes_title = QLabel(_('Notes:'))
        main_notes_title.setObjectName("usertitle")
        notes_layout.addWidget(main_notes_title, 0, 0, 1, 3)

        # Alias
        alias_title = QLabel(_('Alias:'))
        alias_title.setObjectName("usersubtitle")
        notes_layout.addWidget(alias_title, 1, 0, 1, 1)
        alias_data = QLabel(self.user['alias'])
        notes_layout.addWidget(alias_data, 1, 1, 1, 2)

        # Token only for administrators
        if self.user['is_admin']:
            token_title = QLabel(_('Token:'))
            token_title.setObjectName("usersubtitle")
            notes_layout.addWidget(token_title, 2, 0, 1, 2)
            token_data = QLabel(self.user['token'])
            token_data.setTextInteractionFlags(Qt.TextSelectableByMouse)
            token_data.setCursor(Qt.IBeamCursor)
            notes_layout.addWidget(token_data, 2, 1, 1, 1)

        # Notes
        notes_title = QLabel(_('Notes:'))
        notes_title.setObjectName("usersubtitle")
        notes_layout.addWidget(notes_title, 3, 0, 1, 1)

        # Add and hide QLineEdit; Shown only when edited
        self.notes_edit = QLineEdit()
        self.notes_edit.hide()
        self.notes_edit.editingFinished.connect(self.patch_notes)
        self.notes_edit.setToolTip(_('Type enter to validate your notes.'))
        notes_layout.addWidget(self.notes_edit, 4, 1, 1, 1)

        # Create QLabel for notes
        self.notes_data = QLabel(self.user['notes'])
        notes_layout.addWidget(self.notes_data, 4, 1, 1, 1)

        # Edit button for notes
        self.notes_btn = QPushButton()
        self.notes_btn.setIcon(QIcon(get_image_path('edit')))
        self.notes_btn.setToolTip(_("Edit your notes."))
        self.notes_btn.setObjectName("notes")
        self.notes_btn.setFixedSize(32, 32)
        self.notes_btn.clicked.connect(self.button_clicked)

        notes_layout.addWidget(self.notes_btn, 4, 2, 1, 1)

        return notes_widget

    def button_clicked(self):
        """
        Hide and show QLabel for notes or PATCH password

        """

        btn = self.sender()

        if "notes" in btn.objectName():
            self.notes_data.hide()
            self.notes_edit.setText(self.notes_data.text())
            self.notes_edit.show()
            self.notes_edit.setFocus()
        elif "password" in btn.objectName():
            pass_dialog = PasswordDialog(self.app_backend)
            pass_dialog.initialize()

            if pass_dialog.exec_() == QDialog.Accepted:
                new_password = pass_dialog.pass_edit.text()

                data = {'password': str(new_password)}
                headers = {'If-Match': self.user['_etag']}
                endpoint = '/'.join(['user', self.user['_id']])

                patched = self.app_backend.patch(endpoint, data, headers)

                if patched:
                    message = _("Your password has been updated !")
                    send_banner('OK', message, duration=10000)
                else:
                    send_banner('ERROR', _("Backend PATCH failed, please check your logs !"))
        else:
            logger.error("Wrong sender in UserProfile.")

    def patch_notes(self):
        """
        Patch notes user when edition is finished

        """

        # Patch only if text have really changed
        if bool(self.notes_edit.text() != self.user['notes']):
            data = {'notes': str(self.notes_edit.text())}
            headers = {'If-Match': self.user['_etag']}
            endpoint = '/'.join(['user', self.user['_id']])

            patched = self.app_backend.patch(endpoint, data, headers)

            if patched:
                name = self.user['alias'] if self.user['alias'] else self.user['name']
                message = _("The notes for the %s have been edited.") % name
                send_banner('OK', message, duration=10000)
            else:
                send_banner('ERROR', _("Backend PATCH failed, please check your logs !"))

            self.update_profile.emit()
        else:
            self.notes_data.show()
            self.notes_edit.hide()

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
        notification_layout.setAlignment(host_notif_widget, Qt.AlignTop)

        services_notif_widget = self.get_services_notif_widget()
        notification_layout.addWidget(services_notif_widget, 0, 1, 1, 1)
        notification_layout.setAlignment(services_notif_widget, Qt.AlignTop)

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

        notif_title = QLabel(_("Hosts notifications configurations"))
        notif_title.setObjectName("usertitle")
        host_notif_layout.addWidget(notif_title, 0, 0, 1, 2)

        state_title = QLabel(_("State:"))
        state_title.setObjectName("usersubtitle")
        host_notif_layout.addWidget(state_title, 1, 0, 1, 1)
        self.host_notif_state = QCheckBox()
        self.host_notif_state.setChecked(self.user['host_notifications_enabled'])
        self.host_notif_state.stateChanged.connect(self.enable_notifications)
        self.host_notif_state.setObjectName('hostactions')
        self.host_notif_state.setFixedSize(18, 18)
        host_notif_layout.addWidget(self.host_notif_state, 1, 1, 1, 1)

        enable_title = QLabel(_("Notification enabled:"))
        enable_title.setMinimumHeight(32)
        enable_title.setObjectName("usersubtitle")
        host_notif_layout.addWidget(enable_title, 2, 0, 1, 1)
        enable_icon = self.get_enable_label_icon(
            self.user['host_notifications_enabled']
        )
        host_notif_layout.addWidget(enable_icon, 2, 1, 1, 1)

        period_title = QLabel(_("Notification period:"))
        period_title.setObjectName("usersubtitle")
        host_notif_layout.addWidget(period_title, 3, 0, 1, 1)
        period = self.get_period_name(self.user['host_notification_period'])
        period_data = QLabel(period.capitalize())
        host_notif_layout.addWidget(period_data, 3, 1, 1, 1)

        option_title = QLabel(_("Options:"))
        option_title.setObjectName("usersubtitle")
        host_notif_layout.addWidget(option_title, 4, 0, 1, 2)
        host_notif_layout.setAlignment(option_title, Qt.AlignCenter)

        option_widget = self.get_options_widget(
            'hosts',
            self.user['host_notification_options']
        )
        host_notif_layout.addWidget(option_widget, 5, 0, 1, 2)

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

        notif_title = QLabel(_("Services notifications configurations"))
        notif_title.setObjectName("usertitle")
        service_notif_layout.addWidget(notif_title, 0, 0, 1, 2)

        state_title = QLabel(_("State:"))
        state_title.setObjectName("usersubtitle")
        service_notif_layout.addWidget(state_title, 1, 0, 1, 1)
        self.service_notif_state = QCheckBox()
        self.service_notif_state.setObjectName('serviceactions')
        self.service_notif_state.setChecked(self.user['service_notifications_enabled'])
        self.service_notif_state.stateChanged.connect(self.enable_notifications)
        self.service_notif_state.checkState()
        self.service_notif_state.setFixedSize(18, 18)
        service_notif_layout.addWidget(self.service_notif_state, 1, 1, 1, 1)

        enable_title = QLabel(_("Notification enabled:"))
        enable_title.setObjectName("usersubtitle")
        enable_title.setMinimumHeight(32)
        service_notif_layout.addWidget(enable_title, 2, 0, 1, 1)
        enable_data = self.get_enable_label_icon(
            self.user['service_notifications_enabled']
        )
        service_notif_layout.addWidget(enable_data, 2, 1, 1, 1)

        period_title = QLabel(_("Notification period:"))
        period_title.setObjectName("usersubtitle")
        service_notif_layout.addWidget(period_title, 3, 0, 1, 1)
        period = self.get_period_name(self.user['service_notification_period'])
        period_data = QLabel(period.capitalize())
        service_notif_layout.addWidget(period_data, 3, 1, 1, 1)

        option_title = QLabel(_("Options:"))
        option_title.setObjectName("usersubtitle")
        service_notif_layout.addWidget(option_title, 4, 0, 1, 2)
        service_notif_layout.setAlignment(option_title, Qt.AlignCenter)

        option_widget = self.get_options_widget(
            'services',
            self.user['service_notification_options']
        )
        service_notif_layout.addWidget(option_widget, 5, 0, 1, 2)

        return service_notif_widget

    def enable_notifications(self):
        """
        Enable notification for the wanted type: hosts or services

        """

        check_btn = self.sender()

        notification_type = ''
        if 'hostactions' in check_btn.objectName():
            notification_type = 'host_notifications_enabled'
        elif 'serviceactions' in check_btn.objectName():
            notification_type = 'service_notifications_enabled'
        else:
            logger.error('Wrong caller %s', self.sender().objectName())

        if notification_type:
            # check_btn.checkState() is equal to 0 or 2
            notification_enabled = True if check_btn.checkState() else False
            data = {notification_type: notification_enabled}
            headers = {'If-Match': self.user['_etag']}
            endpoint = '/'.join(['user', self.user['_id']])

            patched = self.app_backend.patch(endpoint, data, headers)

            if patched:
                enabled = 'enabled' if notification_enabled else 'disabled'
                message = _("Notifications for %ss are %s") % (
                    check_btn.objectName().replace('actions', ''),
                    enabled
                )
                send_banner('OK', message, duration=10000)
            else:
                send_banner('ERROR', _("Backend PATCH failed, please check your logs !"))

        self.update_profile.emit()

    def get_options_widget(self, item_type, options):
        """
        Create and return QWidget with options and their icons

        :param item_type: hosts or services, define type of options
        :type item_type: str
        :param options: list of notification options
        :type options: list
        :return: QWidget with options and icons
        :rtype: QWidget
        """

        items_options = {
            'hosts': ['d', 'u', 'r', 'f', 's', 'n'],
            'services': ['w', 'u', 'c', 'r', 'f', 's', 'n']
        }

        available_options = items_options[item_type]

        selected_options = {}
        for opt in available_options:
            selected_options[opt] = bool(opt in options)

        option_names = {
            'hosts': {
                'd': 'DOWN',
                'u': 'UNREACHABLE',
                'r': 'RECOVERY',
                'f': 'FLAPPING',
                's': 'DOWNTIME',
                'n': 'NONE'
            },
            'services': {
                'w': 'WARNING',
                'u': 'UNKNOWN',
                'c': 'CRITICAL',
                'r': 'RECOVERY',
                'f': 'FLAPPING',
                's': 'DOWNTIME',
                'n': 'NONE'
            }
        }

        line = 0
        options_widget = QWidget()
        options_layout = QGridLayout()
        options_widget.setLayout(options_layout)
        for opt in selected_options:
            # Name of Option
            option_label = QLabel(option_names[item_type][opt])
            object_name = 'user' + str(selected_options[opt])
            option_label.setObjectName(object_name)
            options_layout.addWidget(option_label, line, 0, 1, 1)
            # Corresponding icon
            option_icon = self.get_enable_label_icon(
                selected_options[opt]
            )
            option_icon.setFixedSize(14, 14)
            options_layout.addWidget(option_icon, line, 1, 1, 1)
            line += 1

        return options_widget

    def get_period_name(self, uuid):
        """
        Get the period name or alias

        :param uuid: the Id of the timeperiod
        :type uuid: str
        :return: name or alias of timeperiod
        :rtype: str
        """

        projection = [
            'name',
            'alias'
        ]

        endpoint = '/'.join(['timeperiod', uuid])

        period = self.app_backend.get(endpoint, projection=projection)

        if period:
            if 'alias' in period:
                return period['alias']

            return period['name']

        return 'n/a'

    @staticmethod
    def get_enable_label_icon(state):
        """
        Return red crosse or green check QPixmap in QLabel, depending state is True of False

        :param state: state True of False
        :type state: bool
        :return: corresponding QLabel with QPixmap
        :rtype: QLabel
        """

        states = {
            True: 'checked',
            False: 'error'
        }

        # Should never happen
        if not isinstance(state, bool):
            state = False

        icon = QPixmap(get_image_path(states[state]))

        enable_icon = QLabel()
        enable_icon.setFixedSize(18, 18)
        enable_icon.setPixmap(icon)
        enable_icon.setScaledContents(True)

        return enable_icon
