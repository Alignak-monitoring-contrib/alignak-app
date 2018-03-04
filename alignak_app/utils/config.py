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
    Settings
    ++++++++
    Settings manage configurations of Alignak-app

    * ``settings.cfg``: contains configurations of Alignak-app (stored in ``ALIGNAKAPP_USR_DIR``)
    * ``images.ini``: contains all images names (stored in ``ALIGNAKAPP_APP_DIR``)
    * ``style.css``: contains css of Alignak-app (stored in ``ALIGNAKAPP_APP_DIR``)
"""

import os
import webbrowser

from logging import getLogger

import configparser
from configparser import NoOptionError, NoSectionError

from alignak_app.utils.system import read_config_file

logger = getLogger(__name__)


class Settings(object):
    """
        Class who read and create configuration for Alignak-app
    """

    # Default configurations
    default_parameters = {
        'Alignak': {
            'username': '',
            'password': '',
            'backend': 'http://127.0.0.1:5000',
            'url': 'http://127.0.0.1',
            'webui': 'http://127.0.0.1:80',
            'processes': '1'

        },
        'Alignak-app': {
            'requests_interval': 30,
            'notification_duration': 30,
            'spy_interval': 30,
            'update_status': 30,
            'update_buttons': 30,
            'update_livestate': 30,
            'update_dashboard': 30,
            'update_host': 30,
            'update_service': 30,
        },
        'Log': {
            'filename': 'alignakapp',
            'debug': True
        }
    }

    def __init__(self):
        self.app_config = configparser.ConfigParser(os.environ)
        self.img_config = configparser.ConfigParser()
        self.css_style = ''
        self.settings = {
            'settings': '',
            'images': ''
        }

    def init_config(self):
        """
        Initialize configurations

        """

        settings_cfg = '%s/settings.cfg' % os.environ['ALIGNAKAPP_USR_DIR']
        images_ini = '%s/images.ini' % os.environ['ALIGNAKAPP_APP_DIR']

        self.settings['settings'] = read_config_file(self.app_config, settings_cfg)
        self.settings['images'] = read_config_file(self.img_config, images_ini)

    def get_config(self, section, option, boolean=False):
        """
        Return global application configuration values

        :param section: wanted configuration section
        :type section: str
        :param option: wanted configuration option
        :type option: str
        :param boolean: define if velue is boolean or not
        :type boolean: bool
        :return: configuration value
        :rtype: str | bool
        """

        if boolean:
            try:
                if self.app_config.get(section, option):
                    return self.app_config.getboolean(section, option)

                return self.default_parameters[section][option]
            except (NoOptionError, NoSectionError) as e:  # pragma: no cover - not testable
                logger.error('%s', str(e))
                logger.error('Replace by default %s: %s',
                             section, self.default_parameters[section][option])
                return self.default_parameters[section][option]
        else:
            try:
                if self.app_config.get(section, option):
                    return self.app_config.get(section, option)

                return self.default_parameters[section][option]
            except (NoOptionError, NoSectionError) as e:  # pragma: no cover - not testable
                print("failed section")
                logger.error('%s', str(e))
                logger.error('Replace by default %s: %s',
                             section, self.default_parameters[section][option])
                return self.default_parameters[section][option]

    def edit_setting_value(self, section, option, new_value):
        """
        Set an option in configuration file

        :param section: section to edit
        :type section: str
        :param option: option to edit, corresponding to the wanted section
        :type option: str
        :param new_value: new value to set in place of old
        :type new_value: str
        """

        try:
            # Read configuration file and store in list
            with open(self.settings['settings'], 'r') as config_file:
                data = config_file.readlines()
                file_to_write = self.settings['settings']
            # Update values
            for d in data:
                if option in d[0:len(option)]:
                    data[data.index(d)] = option + ' = ' + new_value + '\n'
            # Setting the current configuration
            self.app_config.set(section, option, new_value)
            try:
                with open(file_to_write, 'w') as new_config_file:
                    new_config_file.writelines(data)
            except PermissionError as e:
                print('Not permission to write inside [%s] !' % file_to_write)
                exit(e)

        except NoOptionError as e:  # pragma: no cover
            logger.error('Can\'t set Option in configuration file : %s', e)

    def get_image(self, name):
        """
        Return the path of wanted image

        :param name: name of image
        :type name: str
        :return: full path of image
        :rtype: str
        """

        try:
            return '%s/images/%s' % \
                   (os.environ['ALIGNAKAPP_APP_DIR'], self.img_config.get('Images', name))
        except (NoOptionError, NoSectionError) as e:
            logger.error('Image not found or not set in [images.ini] : %s', e)
            return '%s/images/error.svg' % os.environ['ALIGNAKAPP_APP_DIR']

    def init_css(self):
        """
        Init the css file and fill app_css

        """

        try:
            css = open('%s/css/style.css' % os.environ['ALIGNAKAPP_APP_DIR'])
            self.css_style = css.read()
        except IOError as e:
            logger.error('CSS File is missing : %s', str(e))
            self.css_style = ''


# Initialize Settings object
settings = Settings()


def open_url(endpoint='login'):  # pragma: no cover
    """
    Open web browser on wanted endpoint

    :param endpoint: endpoint of webui
    :type endpoint: str
    """

    if settings.get_config('Alignak', 'webui'):
        logger.debug('Open url : ' + settings.get_config('Alignak', 'webui') + '/' + endpoint)
        webbrowser.open(settings.get_config('Alignak', 'webui') + '/' + endpoint)


def get_url_endpoint_from_icon_name(icon_name):
    """
    Return endpoint depending of "icon_name"

    :param icon_name: naem of icon
    :type icon_name: str
    """

    available_endpoints = {
        'hosts_up': 'ls_state:UP',
        'hosts_unreachable': 'ls_state:UNREACHABLE',
        'hosts_down': 'ls_state:DOWN',
        'services_ok': 'ls_state:OK',
        'services_warning': 'ls_state:WARNING',
        'services_critical': 'ls_state:CRITICAL',
        'services_unknown': 'ls_state:UNKNOWN',
        'services_unreachable': 'ls_state:UNREACHABLE',
        'acknowledge': 'ls_acknowledged:yes',
        'downtime': 'ls_downtimed:yes'
    }

    try:
        final_endpoint = '/table?search=%s' % available_endpoints[icon_name]
    except KeyError as e:
        logger.warning('Endpoint not available: %s', e)
        final_endpoint = '/table'

    return final_endpoint
