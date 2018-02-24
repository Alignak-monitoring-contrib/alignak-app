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
    Install
    +++++++
    Install manage installation folders and the daemon file creation
"""

import os
import sys
import stat
import subprocess

from alignak_app import __alignak_url__, __doc_url__, __version__, __releasenotes__, __application__


def create_user_app_dir(cfg_file):
    """
    Create a user folder for App configuration file and log

    :param cfg_file: file to copy if user has no rights
    :type cfg_file: str
    :return: return original file if user ha right, else the new file created
    :rtype: str
    """

    # If the file exists, App add a sample file
    if not os.path.isfile(cfg_file + '.sample'):
        creation = subprocess.run(
            ['cp', cfg_file, cfg_file + '.sample'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        try:
            assert creation.returncode == 0
        except AssertionError:
            print("User folder creation: ", creation.stdout.decode('UTF-8'))

    if not os.access(cfg_file, os.W_OK):
        # Create Folder for user if does not exist
        user_app_dir = '%s/.local/alignak_app' % os.environ['HOME']
        if not os.path.exists(user_app_dir):
            try:
                os.makedirs(user_app_dir)
            except (PermissionError, FileExistsError) as e:
                print(e)
                sys.exit('Can\'t create App directory for user in [%s] !' % user_app_dir)

        # If file does not exist, App create it
        dest_file = os.path.join(user_app_dir, os.path.split(cfg_file)[1])
        if not os.path.isfile(dest_file):
            creation = subprocess.run(
                ['cp', cfg_file, dest_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            try:
                assert creation.returncode == 0
            except AssertionError:
                print("Copy of user configuration file: ", creation.stdout.decode('UTF-8'))

        return dest_file
    else:
        return cfg_file


def write_file(install_path, filename, text, *args):
    """
    Write file in system, make it executbale or add autocompletion to "rc" user file

    :param install_path: path where to write
    :type install_path: str
    :param filename: name of file to write
    :type filename: str
    :param text: text to write inside filename
    :type text: str
    :param args: argument who define if executable or autocomplete
    :type args: tuple
    :return: 0 if success, else return error string
    :rtype: int | str
    """

    file_to_write = os.path.join(install_path, filename)
    returncode = '%s can\'t create following file: %s' % (__application__, file_to_write)

    try:
        with open(file_to_write, 'w') as cur_file:
            cur_file.write(text)

        if 'exec' in args:
            print('Create/Update [%s]' % file_to_write)
            # Make file executable
            try:
                st = os.stat(file_to_write)
                os.chmod(file_to_write, st.st_mode | stat.S_IEXEC)
                returncode = 0
            except Exception as e:
                returncode = '%s can\'t set permissions on daemon file: %s\n%s' % (
                    __application__, file_to_write, str(e))

        if 'autocomplete' in args:
            # Add auto completion
            user_rc = ''
            for autocomplete_file in ['.bashrc', '.zshrc']:
                if os.path.isfile('%s/%s' % (os.environ['HOME'], autocomplete_file)):
                    user_rc = '%s/%s' % (os.environ['HOME'], autocomplete_file)
                    print('Add autocompletion inside [%s]' % user_rc)
                    break
            autocompletion_text = '\n# Alignak-app completion:\n. %s' % file_to_write

            try:
                bashrc = open(user_rc, 'r')
                if 'Alignak-app completion' not in bashrc.read():
                    bashrc.close()
                    with open(user_rc, 'a') as cur_rc_file:
                        cur_rc_file.write(autocompletion_text)
                else:
                    bashrc.close()
                returncode = 0
            except Exception as w:
                returncode = '%s can\'t add completion to your: %s\n%s' % (
                    __application__, user_rc, str(w))
    except Exception as w:
        returncode = '%s can\'t create following file: %s\n%s' % (
            __application__, file_to_write, str(w))

    return returncode


def check_return_code(returncode):
    """
    Check if returncode is equal to 0, else exit with error

    :param returncode: returncode to check
    :type returncode: int | str
    :return: OK if code is equal to 0, else exit()
    :rtype: str | None
    """

    if returncode == 0:
        return 'OK'

    return sys.exit('ERROR: %s' % returncode)


def display_app_env():
    """
    Display current environment variables used by App

    """

    app_env_var = ['ALIGNAKAPP_APP_CFG', 'ALIGNAKAPP_USER_CFG', 'ALIGNAKAPP_LOG_DIR']

    print('Use following variables:')
    for env_var in app_env_var:
        try:
            print('- [%s] = %s' % (env_var, os.environ[env_var]))
        except KeyError:
            print('- [%s] = None' % env_var)
    print('')


def install_alignak_app(bin_file):
    """
    Install an "alignak-app" daemon for user

    :param bin_file: python file "alignak-app.py" who have been launched
    :type bin_file: str
    """

    if not os.path.isdir('%s/bin' % os.environ['HOME']):
        try:
            os.mkdir('%s/bin' % os.environ['HOME'])
        except IOError as e:
            print('%s fail to create bin directory!' % __application__)
            sys.exit(e)

    possible_paths = [
        '%s/bin' % os.environ['HOME'], '/usr/local/bin', '/usr/sbin'
    ]

    install_path = ''
    for path in possible_paths:
        if path in os.environ['PATH'] and os.access(path, os.W_OK):
            install_path = path

    if install_path:
        # Start installation
        print('----------- Install -----------\nInstallation start...\n')
        display_app_env()
        daemon_name = 'alignak-app'
        auto_name = 'alignak-app-auto'

        # Create daemon bash file
        bash_sample = '%s/bin-samples/%s.sample.sh' % (
            os.environ['ALIGNAKAPP_APP_CFG'], daemon_name)
        bash_file = open(bash_sample)
        bash_format = bash_file.read() % (
            daemon_name, bin_file, os.environ['ALIGNAKAPP_APP_CFG'],
            os.environ['ALIGNAKAPP_USER_CFG'], os.environ['ALIGNAKAPP_LOG_DIR'], __version__,
            __releasenotes__, __alignak_url__, __doc_url__,
        )
        bash_file.close()
        status = check_return_code(
            write_file(install_path, daemon_name, bash_format, 'exec')
        )
        print('Daemon file...%s' % status)

        # Create autocomplete file
        bash_auto_sample = \
            '%s/bin-samples/%s.sample.sh' % (os.environ['ALIGNAKAPP_APP_CFG'], auto_name)
        bash_auto_file = open(bash_auto_sample)
        autocomplete_format = bash_auto_file.read() % (
            os.path.join(install_path, daemon_name), daemon_name
        )
        bash_auto_file.close()
        status = check_return_code(
            write_file(install_path, auto_name, autocomplete_format, 'autocomplete')
        )
        print('Auto completion...%s\n' % status)

        # Installation is done !
        print('Installation is done ! You can run "%s" command !' % daemon_name)
    else:
        print('Please restart this script with a "root" user.')
