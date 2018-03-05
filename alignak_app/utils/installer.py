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
    Installer
    +++++++++
    Installer check and manage installation of Alignak-app

    * Check ``ALIGNAKAPP_APP_DIR``, ``ALIGNAKAPP_USR_DIR`` and ``ALIGNAKAPP_LOG_DIR`` folders
    * Check required files for application and user
    * Install configuration and daemon files for user
"""

import os
import sys

from alignak_app import __project_url__, __doc_url__, __version__, __releasenotes__, __application__

from alignak_app.utils.system import install_file, write_file, write_rc_file, mkdir, file_executable


class Installer(object):
    """
        Class who create and check: folders, files and environment variables for Alignak-App
    """

    daemon_name = __application__.lower()
    app_folder = __application__.lower().replace('-', '_')

    if 'win32' in sys.platform:
        install_folders = [
            '%s\\Python\\%s' % (os.environ['APPDATA'], app_folder),
            '%s\\Alignak-app' % os.environ['PROGRAMFILES']
        ]
    else:
        install_folders = [
            '%s/.local/%s/bin' % (os.environ['HOME'], app_folder),
            '/usr/local/%s/bin' % app_folder
        ]

    states = {
        True: 'OK',
        False: 'Problem !'
    }

    def __init__(self):
        self.app_dir = ''
        self.usr_cfg = ''
        self.log_dir = ''

    def check_installation(self, mode='start'):
        """
        Check Alignak-app installation

        """

        self.init_environment()

        check_folder = self.check_install_folders()
        if 'install' in mode:
            print('- Check installation folders: %s' % self.states[check_folder])

        self.check_environment(mode)

        if 'start' in mode:
            self.check_user_installation()

        check_files = self.check_install_files()
        if 'install' in mode:
            print('- Check installation files: %s' % self.states[check_files])

    def check_install_folders(self):
        """
        Check Alignak-app folders

        :return: if all folders are present
        :rtype: bool
        """

        check_folders = True
        if not self.app_dir:
            for folder in self.install_folders:
                if os.path.exists(folder):
                    self.app_dir = folder.replace('/bin', '')

            if not self.app_dir:
                print('Alignak-App does not seem to be installed on your system.\n'
                      'Thank you for reading the documentation: %s' % __doc_url__)
                sys.exit(1)

        if not self.usr_cfg:
            if 'win32' in sys.platform:
                self.usr_cfg = '%s\\Alignak-app' % os.environ['PROGRAMFILES']
            else:
                self.usr_cfg = '%s/.local/%s' % (os.environ['HOME'], self.app_folder)
        if not self.log_dir:
            if 'win32' in sys.platform:
                self.log_dir = '%s\\Alignak-app' % os.environ['PROGRAMFILES']
            else:
                self.log_dir = '%s/.local/%s' % (os.environ['HOME'], self.app_folder)

        if not os.path.exists(self.usr_cfg):
            check_folders = mkdir(self.usr_cfg)
        if not os.path.exists(self.log_dir):
            check_folders = mkdir(self.log_dir)

        return check_folders

    def check_install_files(self):
        """
        Check Alignak-app files

        :return: if all files are present
        :rtype: bool
        """

        app_folders = [
            'css', 'images'
        ]
        app_files = [
            'images.ini', 'settings.cfg'
        ]

        if 'win32' not in sys.platform:
            app_folders.append('bin')
            app_folders.append('bin-samples')

            app_files.append('bin-samples/%s-auto.sample.sh' % self.daemon_name)
            app_files.append('bin-samples/%s.sample.sh' % self.daemon_name)

        # Check App folders and files
        for folder in app_folders:
            try:
                assert os.path.exists(os.path.join(os.environ['ALIGNAKAPP_APP_DIR'], folder))
            except AssertionError:
                print('The [%s] folder seems to be missing in "%s" !' %
                      (folder, self.app_dir))
                sys.exit(1)

        for app_file in app_files:
            try:
                assert os.path.isfile(os.path.join(os.environ['ALIGNAKAPP_APP_DIR'], app_file))
            except AssertionError:
                print('The [%s] file seems to be missing in "%s" !' %
                      (app_file, os.environ['ALIGNAKAPP_APP_DIR']))
                sys.exit(1)

        return True

    def init_environment(self):
        """
        Assign environment variables to fields if they exists

        """

        if 'ALIGNAKAPP_APP_DIR' in os.environ:
            self.app_dir = os.environ['ALIGNAKAPP_APP_DIR']

        if 'ALIGNAKAPP_USR_DIR' in os.environ:
            self.usr_cfg = os.environ['ALIGNAKAPP_USR_DIR']

        if 'ALIGNAKAPP_LOG_DIR' in os.environ:
            self.log_dir = os.environ['ALIGNAKAPP_LOG_DIR']

    def check_environment(self, mode='start'):
        """
        Assign fields to environment variables if they don't exist

        """

        if 'ALIGNAKAPP_APP_DIR' not in os.environ:
            os.environ['ALIGNAKAPP_APP_DIR'] = self.app_dir

        if 'ALIGNAKAPP_USR_DIR' not in os.environ:
            os.environ['ALIGNAKAPP_USR_DIR'] = self.usr_cfg

        if 'ALIGNAKAPP_LOG_DIR' not in os.environ:
            os.environ['ALIGNAKAPP_LOG_DIR'] = self.log_dir

        for env_var in ['ALIGNAKAPP_APP_DIR', 'ALIGNAKAPP_USR_DIR', 'ALIGNAKAPP_LOG_DIR']:
            try:
                os.environ[env_var]
            except KeyError as e:
                print('Environment variable missing: %s' % e)
                sys.exit(1)

            if 'ALIGNAKAPP_APP_DIR' not in env_var:
                try:
                    assert os.access(os.environ[env_var], os.W_OK)
                except AssertionError:
                    print('[!] User don\'t have permission on %s !' % os.environ[env_var])
                    sys.exit(1)

        if 'install' in mode:
            print('- Default %s Environment:' % __application__)
            print('\t[ALIGNAKAPP_APP_DIR] = %s' % os.environ['ALIGNAKAPP_APP_DIR'])
            print('\t[ALIGNAKAPP_USR_DIR] = %s' % os.environ['ALIGNAKAPP_USR_DIR'])
            print('\t[ALIGNAKAPP_LOG_DIR] = %s' % os.environ['ALIGNAKAPP_LOG_DIR'])

    def check_user_installation(self):
        """
        Check user installation files

        """

        usr_cfg_file = os.path.join(os.environ['ALIGNAKAPP_USR_DIR'], 'settings.cfg')
        try:
            assert os.path.isfile(usr_cfg_file)
        except AssertionError as e:
            print(e)
            print('- [!] There is no [settings.cfg] file in [ALIGNAKAPP_USR_DIR] folder !')
            print('\tPlease launch "%s.py --install before start."' % self.daemon_name)
            sys.exit(1)

    def install(self):
        """
        Install Alignak-app user files on system

        """

        install_file(
            os.environ['ALIGNAKAPP_APP_DIR'],
            os.environ['ALIGNAKAPP_USR_DIR'],
            'settings.cfg'
        )

        if 'win32' not in sys.platform:
            bin_folder = '%s/bin' % os.environ['HOME']
            bin_file = '%s/bin/%s' % (os.environ['ALIGNAKAPP_APP_DIR'], self.daemon_name + '.py')
            if not os.path.exists(bin_folder):
                mkdir(bin_folder)

            write_file(
                os.path.join(os.environ['ALIGNAKAPP_APP_DIR'], 'bin-samples'),
                bin_folder,
                '%s.sample.sh' % self.daemon_name,
                (
                    self.daemon_name, os.path.join(os.environ['ALIGNAKAPP_APP_DIR'], bin_file),
                    os.environ['ALIGNAKAPP_APP_DIR'], os.environ['ALIGNAKAPP_USR_DIR'],
                    os.environ['ALIGNAKAPP_LOG_DIR'], __version__, __releasenotes__,
                    __project_url__, __doc_url__,
                )
            )
            file_executable(
                os.path.join(bin_folder, self.daemon_name)
            )
            write_file(
                os.path.join(os.environ['ALIGNAKAPP_APP_DIR'], 'bin-samples'),
                bin_folder,
                '%s-auto.sample.sh' % self.daemon_name,
                (
                    os.path.join(bin_folder, self.daemon_name),
                    self.daemon_name
                )
            )
            write_rc_file(os.path.join(bin_folder, '%s-auto' % self.daemon_name))

        return True
