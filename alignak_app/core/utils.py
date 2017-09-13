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
from configparser import NoOptionError, NoSectionError, DuplicateOptionError, DuplicateSectionError
from datetime import datetime
from alignak_app import __project_url__

logger = getLogger(__name__)


# Application Home
def get_app_workdir():
    """
    Return user home.

    :return: application workdir
    :rtype: str
    """

    root_config = configparser.ConfigParser(os.environ)
    try:
        if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
            root_config.read('%s/.local/alignak_app/app_workdir.ini' % os.environ['HOME'])
        elif 'win32' in sys.platform:  # pragma: no cover - not testable:
            root_config.read('%s\\Alignak-app\\app_workdir.ini' % os.environ['PROGRAMFILES'])
        else:
            sys.exit('Your system seems not compatible. Please consult: %s' % __project_url__)
    except (IOError, NoSectionError) as e:
        sys.exit(e)

    app_workdir = root_config.get('app_workdir', 'workdir')

    if not app_workdir:
        logger.info('App Workdir is empty. Application use %s instead !', get_main_folder())
        app_workdir = get_main_folder()
    if app_workdir[:1] == '~':
        logger.error('You can\'t use "tilde" in this file. Please use $HOME instead !')
        logger.warning('App Workdir is not valid. Application use %s instead !', get_main_folder())
        app_workdir = get_main_folder()

    if app_workdir[len(app_workdir) - 1:] == '/':
        app_workdir = app_workdir.rstrip('/')
    if app_workdir[len(app_workdir) - 1:] == '\\':
        app_workdir = app_workdir.rstrip('\\')

    return app_workdir


def get_main_folder():
    """
    Return the main folder of Application

    :return: main path
    :rtype: str
    """

    if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
        main_folder = '%s/.local/alignak_app' % os.environ['HOME']
    elif 'win32' in sys.platform:  # pragma: no cover - not testable
        main_folder = '%s\\Alignak-app' % os.environ['PROGRAMFILES']
    else:
        sys.exit('Your system seems not compatible. Please consult: %s' % __project_url__)

    return main_folder


# Application Configuration
default_parameters = {
    'synthesis_interval': 30,
    'daemon_interval': 60,
    'item_interval': 30,
    'duration': 8,
    'position': 'top:right',
    'animation': 1000,
    'filename': 'alignakapp',
    'location': False,
    'debug': True,
    'username': '',
    'password': '',
    'url': 'http://127.0.0.1',
    'backend': 'http://127.0.0.1:5000',
    'webui': 'http://127.0.0.1:5001',
    'processes': '1',
    'bi_less': 0,
    'path': '/alignak_app',
    'img': '/images',
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


def get_filenames():
    """
    Return filenames depending platform

    :return: filenames str or list
    :rtype: str|list
    """

    if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
        config_filenames = '%s/settings.cfg' % get_app_workdir()
    elif 'win32' in sys.platform:  # pragma: no cover - not testable
        config_filenames = '%s\\settings.cfg' % get_app_workdir()
    else:
        sys.exit('Your system seems not compatible. Please consult: %s' % __project_url__)

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
    except (DuplicateOptionError, DuplicateSectionError) as e:  # pragma: no cover - not testable
        logger.error('Duplicate Option/Section in file [%s] !', str(get_filenames()))
        logger.error(str(e))
        sys.exit('Duplicate Option/Section in file [%s] !' % str(get_filenames()))
    except Exception as f:
        logger.error('Configuration file is missing in [%s] !', str(get_filenames()))
        logger.error(str(f))
        sys.exit('Configuration file is missing in [%s] !' % str(get_filenames()))


def get_app_config(section, option, boolean=False):
    """
    Return global application configuration

    """

    if boolean:
        try:
            return app_config.getboolean(section, option)
        except (NoOptionError, NoSectionError) as e:
            logger.error('Missing Option in configuration file : %s', str(e))
            logger.error('Replace by > %s: %s', option, str(default_parameters[option]))
            return default_parameters[option]
    else:
        try:
            return app_config.get(section, option)
        except (NoOptionError, NoSectionError) as e:
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


error_config = 0


def get_image_path(name):
    """
    Return the path of wanted image

    :param name: name of image
    :type name: str
    :return: full path of image
    :rtype: str
    """

    global error_config  # pylint: disable=global-statement

    img_path = get_main_folder()

    try:
        img = '%s/images/%s' % (img_path, app_config.get('Images', name))

        return img
    except (NoOptionError, NoSectionError) as e:
        logger.error('Bad Option : ' + str(e))

        error_config += 1
        if error_config < 7:
            return img_path + '/images/error.svg'
        else:  # pragma: no cover - not testable
            if img_path:
                error_msg = 'Alignak has stop because too many error. We can\'t load files.\n' \
                            ' Make sure that the settings file is present in the directory %s !' \
                            % get_app_workdir()
            else:
                error_msg = 'Your system seems not compatible. Please consult: %s' % __project_url__
            logger.error(error_msg)
            sys.exit(error_msg)


def get_css():
    """
    Read css file and return its content

    :return: css text
    :rtype: str
    """

    try:
        if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
            with open('%s/css/style.css' % (get_main_folder())) as css:
                return css.read()
        else:
            with open('%s/css/style.css' % get_main_folder()) as css:
                return css.read()
    except (IOError, NoSectionError) as e:
        logger.error('CSS File is missing : %s', str(e))
        return ""


def get_diff_since_last_check(last_check):  # pragma: no cover - not testable
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


def get_date_from_timestamp(timestamp):
    """
    Return date from timestamp
    :param timestamp: timestamp to convert to date
    :type timestamp: int
    :return: corresponding date
    :rtype: str
    """

    if timestamp:
        return datetime.fromtimestamp(timestamp)

    return 'n/a'
