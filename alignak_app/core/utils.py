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
        app_root = '%s\\Alignak-app\\' % os.environ['PROGRAMFILES']
    else:  # pragma: no cover - not testable
        sys.exit('Application can\'t find the user HOME.')

    # Prevent from root user
    if 'root' in app_root or not app_root:
        logger.error('Application can\'t find the user HOME or maybe you are connected as ROOT.')
        sys.exit('Application can\'t find the user HOME or maybe you are connected as ROOT.')

    return app_root


# Application Configuration
default_parameters = {
    'synthesis_interval': 30,
    'daemon_interval': 60,
    'item_interval': 30,
    'duration': 8,
    'position': 'top:right',
    'animation': 1000,
    'debug': False,
    'username': '',
    'password': '',
    'url': 'http://127.0.0.1',
    'backend': 'http://127.0.0.1:5000',
    'webui': 'http://127.0.0.1:5001',
    'processes': '1',
    'path': '/alignak_app',
    'img': '/images',
    'tpl': '/templates',
    'icon': 'alignak.svg',
    'about': 'about.svg',
    'exit': 'exit.svg',
    'checked': 'checked.svg',
    'error': 'error.svg',
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
        config_filenames = '%s\\settings.cfg' % get_app_root()
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
        with open(get_filenames(), 'r') as config_file:
            data = config_file.readlines()
            file_to_write = get_filenames()
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

    if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
        img_path = get_app_root() \
                   + app_config.get('Config', 'path') \
                   + app_config.get('Config', 'img') \
                   + '/'
    elif 'win32' in sys.platform:  # pragma: no cover - not testable
        img_path = get_app_root() \
            + app_config.get('Config', 'img') \
            + '/'
    else:
        img_path = '.'

    try:
        img = img_path + app_config.get('Images', name)
        return img
    except NoOptionError as e:
        logger.error('Bad Option : ' + str(e))
        return img_path + app_config.get('Images', 'error')


def get_diff_since_last_check(last_check):
    """
    Return the diff between the last time stamp

    :param last_check: timestamp of the last check
    :type last_check: float
    :return: time difference formatted
    :rtype: str
    """

    if not last_check:
        return 'n/a'

    time_delta = int(time.time()) - int(last_check)

    # If it's now, say it :)
    if time_delta < 3:
        if 0 > time_delta > -4:
            return 'Very soon'
        if time_delta >= 0:
            return 'Just now'

    seconds = int(round(time_delta))
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    months, weeks = divmod(weeks, 4)
    years, months = divmod(months, 12)

    duration = []
    if years > 0:
        duration.append('%dy' % years)
    else:
        if months > 0:
            duration.append('%dM' % months)
        if weeks > 0:
            duration.append('%dw' % weeks)
        if days > 0:
            duration.append('%dd' % days)
        if hours > 0:
            duration.append('%dh' % hours)
        if minutes > 0:
            duration.append('%dm' % minutes)
        if seconds > 0:
            duration.append('%ds' % seconds)

    return ' ' + ' '.join(duration) + ' ago'


def get_css():
    """
    Read css file and return its content

    :return: css text
    :rtype: str
    """

    try:
        if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
            with open('%s/css/style.css' % (
                        get_app_root() + app_config.get('Config', 'path'))
                      ) as css:
                return css.read()
        else:
            with open('%s/css/style.css' % get_app_root()) as css:
                return css.read()
    except IOError as e:
        logger.error('CSS File is missing : %s', str(e))
        return ""
