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
    Config manage configurations of Alignak-app
"""

import os
import sys
import webbrowser

from logging import getLogger

import configparser
from configparser import NoOptionError, NoSectionError, DuplicateOptionError, DuplicateSectionError

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
    except (IOError, NoSectionError) as e:  # pragma: no cover
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
    'notification_elapsed': 30,
    'notification_duration': 30,
    'spy_interval': 60,
    'filename': 'alignakapp',
    'debug': True,
    'username': '',
    'password': '',
    'url': 'http://127.0.0.1',
    'backend': 'http://127.0.0.1:5000',
    'webui': 'http://127.0.0.1:5001',
    'processes': '1',
    'path': '/alignak_app',
    'img': '/images',
}

# Global variables, access by function
app_config = None
app_images = None
app_css = None
error_config = 0


def get_setting_file(filename):
    """
    Return wanted config file, depending platform

    :param filename: name of the setting file
    :type filename: str
    :return: filenames str or list
    :rtype: str|list
    """

    if 'linux' in sys.platform or 'sunos5' in sys.platform or 'bsd' in sys.platform:
        config_file = '%s/%s' % (get_app_workdir(), filename)
    elif 'win32' in sys.platform:  # pragma: no cover - not testable
        config_file = '%s\\%s' % (get_app_workdir(), filename)
    else:
        sys.exit('Your system seems not compatible. Please consult: %s' % __project_url__)

    return config_file


def init_config():
    """
    Initialize configuration

    """

    # Define "app_config" and "app_images" as "global" to access it from anywhere
    global app_config  # pylint: disable=global-statement
    global app_images  # pylint: disable=global-statement

    app_config = configparser.ConfigParser()
    app_images = configparser.ConfigParser()

    logger.info('Read configuration file...')
    try:
        app_config.read(get_setting_file('settings.cfg'))
        app_images.read(get_setting_file('images.ini'))
        logger.info('Configuration file is OK.')
    except (DuplicateOptionError, DuplicateSectionError) as e:  # pragma: no cover - not testable
        logger.error('Duplicate Option/Section in file [%s] !', e)
        sys.exit('Duplicate Option/Section in file [%s] !' % e)
    except Exception as f:  # pragma: no cover - not testable
        logger.error('Configuration file is missing in [%s] !', f)
        sys.exit('Configuration file is missing in [%s] !' % f)


def get_app_config(section, option, boolean=False):
    """
    Return global application configuration

    """

    if boolean:
        try:
            return app_config.getboolean(section, option)
        except (NoOptionError, NoSectionError) as e:  # pragma: no cover - not testable
            logger.error('Missing Option in configuration file : %s', str(e))
            logger.error('Replace by > %s: %s', option, str(default_parameters[option]))
            return default_parameters[option]
    else:
        try:
            return app_config.get(section, option)
        except (NoOptionError, NoSectionError) as e:  # pragma: no cover - not testable
            logger.error('Missing Option in configuration file : %s', str(e))
            logger.error('Replace by > %s: %s', option, str(default_parameters[option]))
            return default_parameters[option]


def edit_setting_value(section, option, new_value):
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
        with open(get_setting_file('settings.cfg'), 'r') as config_file:
            data = config_file.readlines()
            file_to_write = get_setting_file('settings.cfg')
        # Update values
        for d in data:
            if option in d[0:len(option)]:
                data[data.index(d)] = option + ' = ' + new_value + '\n'
        # Setting the current configuration
        app_config.set(section, option, new_value)
        with open(file_to_write, 'w') as new_config_file:
            new_config_file.writelines(data)

    except NoOptionError as e:  # pragma: no cover
        logger.error('Can\'t set Option in configuration file : %s', e)


def get_image(name):
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
        img = '%s/images/%s' % (img_path, app_images.get('Images', name))

        return img
    except (NoOptionError, NoSectionError) as e:
        logger.error('Bad Option : %s', e)

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


def init_css():
    """
    Init the css file and fill app_css

    """

    global app_css  # pylint: disable=global-statement

    try:
        css = open('%s/css/style.css' % (get_main_folder()))
        app_css = css.read()
    except (IOError, NoSectionError) as e:
        logger.error('CSS File is missing : %s', str(e))
        app_css = ""


init_css()


def open_url(endpoint='login'):  # pragma: no cover
    """
    Open web browser on wanted endpoint

    :param endpoint: endpoint of webui
    :type endpoint: str
    """

    if get_app_config('Alignak', 'webui'):
        logger.debug('Open url : ' + get_app_config('Alignak', 'webui') + '/' + endpoint)
        webbrowser.open(get_app_config('Alignak', 'webui') + '/' + endpoint)


def get_url_endpoint_from_icon_name(icon_name):
    """
    Return endpoint depending of "icon_name"

    :param icon_name: icon name: hosts_up, services_ok, acknowledge
    :return:
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
