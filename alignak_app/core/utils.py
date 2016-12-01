#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2016:
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
    Application logs
"""

import os
import sys

from logging import getLogger
from logging import Formatter
from logging import DEBUG, INFO
from logging.handlers import TimedRotatingFileHandler

from string import Template
import configparser
from configparser import NoOptionError


logger = getLogger(__name__)


# Application Logger
def create_logger(root_logger):  # pragma: no cover
    """
    Create the logger for Alignak-App

    :param root_logger: the main logger.
    :type root_logger: :class:`~logging.RootLogger`
    """

    # Define path and file for "file_handler"
    path = get_app_root() + '/alignak_app'
    filename = 'alignakapp.log'

    if not os.path.isdir(path):
        # noinspection PyBroadException
        try:  # pragma: no cover - not testable
            os.makedirs(path)
        except Exception:
            path = '.'

    if not os.access(path, os.W_OK):
        path = '.'

    formatter = Formatter('[%(asctime)s] - %(name)-12s - %(levelname)s - %(message)s')

    # Create "file_handler"
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(path, filename),
        when="D",
        interval=1,
        backupCount=6
    )

    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)

    # Initialize configuration
    set_app_config()

    # Define level of logger
    if app_config.getboolean('Alignak-App', 'debug'):
        root_logger.setLevel(DEBUG)
    else:
        root_logger.setLevel(INFO)


# Application Home
def get_app_root():
    """
    Return user home.
    """

    # Get HOME and USER
    if 'linux' in sys.platform or 'sunos5' in sys.platform:
        alignak_home = os.environ['HOME']
        alignak_home += '/.local'
    elif 'win32' in sys.platform:  # pragma: no cover - not testable
        alignak_home = os.environ['USERPROFILE']
        alignak_home += '\\AppData\\Roaming\\Python\\'
    else:  # pragma: no cover - not testable
        sys.exit('Application can\'t find the user HOME.')

    # Prevent from root user
    if 'root' in alignak_home or not alignak_home:
        sys.exit('Application can\'t find the user HOME or maybe you are connected as ROOT.')

    return alignak_home

# Application Configuration

default_parameters = {
    'check_interval': 30,
    'duration': 8,
    'notifications': True,
    'position': 'top:right',
    'debug': False,
    'username': 'admin',
    'password': 'admin',
    'backend_url': 'http://127.0.0.1:5000',
    'web_service_status': False,
    'web_service_url': 'http://127.0.0.1:8888',
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
    'hosts_unreach': 'host_unreach.svg',
    'services_ok': 'service_ok.svg',
    'services_critical': 'service_critical.svg',
    'services_unknown': 'service_unknown.svg',
    'services_warning': 'service_warning.svg',
}

# Global variable, access by function
app_config = None


def set_app_config():
    """
    Create app_config

    """

    config_file = get_app_root() + '/alignak_app/settings.cfg'

    # Define "app_config" as "global" to access it from anywhere
    global app_config  # pylint: disable=global-statement
    app_config = configparser.ConfigParser()

    logger.info('Read configuration file...')
    if os.path.isfile(config_file):
        app_config.read(config_file)
        logger.info('Configuration file is OK.')
    else:
        logger.error('Configuration file is missing in [' + config_file + '] !')
        sys.exit('Configuration file is missing in [' + config_file + '] !')


def get_app_config(section, option, boolean=False):
    """
    Return global application configuration

    """

    if boolean:
        try:
            return app_config.getboolean(section, option)
        except NoOptionError as e:
            logger.error('Missing Option in configuration file : ' + str(e))
            logger.error('Replace by : ' + option + ': ' + str(default_parameters[option]))
            return default_parameters[option]
    else:
        try:
            return app_config.get(section, option)
        except NoOptionError as e:
            logger.error('Missing Option in configuration file : ' + str(e))
            logger.error('Replace by : ' + option + ': ' + str(default_parameters[option]))
            return default_parameters[option]


# Application Templates
def get_template(name, values):
    """
        Return content of the choosen template with its values.

    :param name: name of the template.
    :type name: str
    :param values: dict of values to substitute.
    :type values: dict
    :return: content of a template
    :rtype: str
    """

    tpl_content = ''

    tpl_path = get_app_root() \
        + app_config.get('Config', 'path') \
        + app_config.get('Config', 'tpl') \
        + '/'

    try:
        tpl_file = open(tpl_path + name)
    except IOError as e:  # pragma: no cover - not testable
        sys.exit('Failed open template : ' + str(e))

    if tpl_file:
        tpl = Template(tpl_file.read())
        tpl_content = tpl.safe_substitute(values)

    return tpl_content


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
