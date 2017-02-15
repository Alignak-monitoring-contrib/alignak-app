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
    Utils manage configurations
"""

import os
import sys
import datetime
import time

from logging import getLogger

import configparser
from configparser import NoOptionError


logger = getLogger(__name__)


# Application Home
def get_app_root():
    """
    Return user home.
    """

    # Get HOME and USER
    if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
        app_root = '%s/.local' % os.environ['HOME']
    elif 'win32' in sys.platform:  # pragma: no cover - not testable
        app_root = '%s\\AppData\\Roaming\\Python\\' % os.environ['USERPROFILE']
    else:  # pragma: no cover - not testable
        sys.exit('Application can\'t find the user HOME.')

    # Prevent from root user
    if 'root' in app_root or not app_root:
        logger.error('Application can\'t find the user HOME or maybe you are connected as ROOT.')
        sys.exit('Application can\'t find the user HOME or maybe you are connected as ROOT.')

    return app_root


# Application Configuration
default_parameters = {
    'check_interval': 30,
    'duration': 8,
    'notifications': True,
    'position': 'top:right',
    'debug': False,
    'username': '',
    'password': '',
    'alignak_url': 'http://127.0.0.1',
    'webui_url': 'http://127.0.0.1:5001',
    'path': '/alignak_app',
    'img': '/images',
    'tpl': '/templates',
    'icon': 'alignak.svg',
    'about': 'about.svg',
    'exit': 'exit.svg',
    'checked': 'checked.svg',
    'unvalid': 'unvalid.svg',
    'hosts_up': 'host_up.svg',
    'hosts_down': 'host_down.svg',
    'hosts_unreachable': 'host_unreachable.svg',
    'services_ok': 'service_ok.svg',
    'services_critical': 'service_critical.svg',
    'services_unknown': 'service_unknown.svg',
    'services_warning': 'service_warning.svg',
}

# Global variable, access by function
app_config = None


def get_filenames():  # pylint: disable=redefined-variable-type
    """
    Return filenames depending platform

    :return: filenames str or list
    :rtype: str|list
    """

    if 'linux' in sys.platform or 'sunos5' in sys.platform:
        config_filenames = '%s/alignak_app/settings.cfg' % get_app_root()
    elif 'win32' in sys.platform:  # pragma: no cover - not testable
        config_filenames = [  # pylint: disable=redefined-variable-type
            '%s\\alignak_app\\settings.cfg' % get_app_root(),
            'C:\\Program Files (x86)\\Alignak-app\\settings.cfg',
            'C:\\Program Files\\Alignak-app\\settings.cfg'
        ]
    else:
        config_filenames = '%s/alignak_app/settings.cfg' % get_app_root()

    return config_filenames


def init_config():
    """
    Initialize configuration

    """

    # Define "app_config" as "global" to access it from anywhere
    global app_config  # pylint: disable=global-statement

    app_config = configparser.ConfigParser()

    logger.info('Read configuration file...')
    try:
        app_config.read(get_filenames())
        logger.info('Configuration file is OK.')
    except Exception as e:
        logger.error('Configuration file is missing in [%s] !', str(get_filenames()))
        logger.error(str(e))
        sys.exit('Configuration file is missing in [%s] !' % str(get_filenames()))


def get_app_config(section, option, boolean=False):
    """
    Return global application configuration

    """

    if boolean:
        try:
            return app_config.getboolean(section, option)
        except NoOptionError as e:
            logger.error('Missing Option in configuration file : %s', str(e))
            logger.error('Replace by > %s: %s', option, str(default_parameters[option]))
            return default_parameters[option]
    else:
        try:
            return app_config.get(section, option)
        except NoOptionError as e:
            logger.error('Missing Option in configuration file : %s', str(e))
            logger.error('Replace by > %s: %s', option, str(default_parameters[option]))
            return default_parameters[option]


def set_app_config(section, option, new_value):
    """
    Set an option in configuration file

    :param section:
    :param option:
    :param new_value:
    """

    try:
        # Read configuration file and store in list
        file_to_write = ''
        if 'linux' in sys.platform or 'sunos5' in sys.platform:
            with open(get_filenames(), 'r') as config_file:
                data = config_file.readlines()
                file_to_write = get_filenames()  # pylint: disable=redefined-variable-type
        elif 'win32' in sys.platform:  # pragma: no cover - not testable
            for cfg_files in get_filenames():
                try:
                    with open(cfg_files, 'r') as config_file:
                        data = config_file.readlines()
                    file_to_write = cfg_files
                except IOError as e:
                    logger.warning(e)
        # Update values
        for d in data:
            if option in d[0:len(option)]:
                data[data.index(d)] = option + ' = ' + new_value + '\n'
        app_config.set(section, option, new_value)
        with open(file_to_write, 'w') as new_config_file:
            new_config_file.writelines(data)

    except NoOptionError as e:
        logger.error('Can\'t set Option in configuration file : ' + str(e))


def get_image_path(name):
    """
    Return the path of wanted image

    :param name: name of image
    :type name: str
    :return: full path of image
    :rtype: str
    """

    img_path = get_app_root() \
        + app_config.get('Config', 'path') \
        + app_config.get('Config', 'img') \
        + '/'

    try:
        img = img_path + app_config.get('Images', name)
        return img
    except NoOptionError as e:
        logger.error('Bad Option : ' + str(e))
        return img_path + app_config.get('Images', 'unvalid')


def get_diff_since_last_check(last_check):
    """
    Return the diff between the last time stamp

    :param last_check: timestamp of the last check
    :type last_check: float
    :return: time difference formatted
    :rtype: str
    """

    # Get current time
    cur_time = time.time()

    format_time = '%H:%M:%S'
    ft_check = datetime.datetime.fromtimestamp(last_check).strftime(format_time)
    ft_time = datetime.datetime.fromtimestamp(cur_time).strftime(format_time)

    time_delta = \
        datetime.datetime.strptime(ft_time, format_time) - \
        datetime.datetime.strptime(ft_check, format_time)

    # Calculate hours, minutes and seconds
    hours = time_delta.seconds // 3600
    # remaining seconds
    s = time_delta.seconds - (hours * 3600)
    minutes = s // 60
    seconds = s - (minutes * 60)

    if hours == 0:
        delta = '%sm %s ago' % (str(minutes), str(seconds))
    else:
        delta = '%sh %sm %s ago' % (str(hours), str(minutes), str(seconds))

    return delta


def get_css():
    """
    Read css file and return its content

    :return: css text
    :rtype: str
    """

    try:
        with open('%s/css/style.css' % (get_app_root() + app_config.get('Config', 'path'))) as css:
            return css.read()
    except IOError as e:
        logger.error('CSS File is missing : %s', str(e))
        return ""
