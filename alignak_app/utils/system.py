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
    System
    ++++++
    System manage interactions with folders and files for Alignak-app
"""

import os
import sys
import stat

import configparser
from configparser import DuplicateOptionError, DuplicateSectionError

from shutil import copyfile


def mkdir(folder):
    """
    Make wanted folder

    :param folder: folder to create
    :type folder: str
    :return: if creation is success or not
    :rtype: bool
    """

    try:
        os.makedirs(folder)
        return True
    except PermissionError as e:
        print('Can\'t create App directory for user in [%s] !\n%s' % (folder, e))
        return False
    except FileExistsError as e:
        print('App directory for user [%s] already exists.\n%s' % (folder, e))
        return True


def install_file(origin_dir, dest_dir, filename):
    """
    Install (copy) filename from an origin folder to a destination folder

    :param origin_dir: origin folder where file to copy is located
    :type origin_dir: str
    :param dest_dir: destination folder where file will be copied
    :type dest_dir: str
    :param filename: name of file to copy
    :type filename: str
    """

    origin_file = os.path.join(origin_dir, filename)

    dest_file = os.path.join(dest_dir, filename)
    output_msg = ''

    if not os.path.isfile(dest_file):
        output_msg += '\t[%s] has been added.' % filename
        try:
            copyfile(origin_file, dest_file)
        except IOError as e:
            sys.exit(e)
    else:
        output_msg += '\t[%s] already exist.' % filename

    output_msg += '\n\t  - Example file added in "%s"' % dest_dir
    dest_file = dest_file + '.sample'
    try:
        copyfile(origin_file, dest_file)
    except IOError as e:
        sys.exit(e)

    print(output_msg)


def write_file(origin_dir, dest_dir, filename, formatted_var=None):  # pragma: no cover
    """
    Write a file from an origiin to a destination, with formatted variables if needed

    :param origin_dir: origin folder where file is located
    :type origin_dir: str
    :param dest_dir: destination folder where file will be located
    :type dest_dir: str
    :param filename: name of file to write
    :type filename: str
    :param formatted_var: tuple of variable to format origin file
    :type formatted_var: tuple
    """

    origin_file = os.path.join(origin_dir, filename)
    dest_file = os.path.join(dest_dir, filename.replace('.sample.sh', ''))

    if os.path.isfile(dest_file):
        print('\t[%s] file has been updated.' % os.path.split(dest_file)[1])
    else:
        print('\t[%s] file has been created.' % os.path.split(dest_file)[1])

    orig_read_file = open(origin_file)
    if formatted_var:
        orig_format_file = orig_read_file.read() % formatted_var
    else:
        orig_format_file = orig_read_file.read()

    with open(dest_file, 'w') as bin_file:
        for line in orig_format_file:
            bin_file.write(line)


autocompletion_text = """
# Alignak-app completion:
if [ -f %s ]; then
    . %s
fi\n
"""


def write_rc_file(filename):  # pragma: no cover
    """
    Write RC file to add autocompletion for Alignak-app

    :param filename: name of file for autocompletion
    :type filename: str
    """

    # Add auto completion
    user_rc = ''
    for autocomplete_file in ['.bashrc', '.zshrc']:
        if os.path.isfile('%s/%s' % (os.environ['HOME'], autocomplete_file)):
            user_rc = '%s/%s' % (os.environ['HOME'], autocomplete_file)

            break

    full_autocompletion_text = autocompletion_text % (filename, filename)

    try:
        bashrc = open(user_rc, 'r')
        if full_autocompletion_text not in bashrc.read():
            print('- Add autocompletion inside [%s]' % user_rc)
            bashrc.close()
            with open(user_rc, 'a') as cur_rc_file:
                cur_rc_file.write(full_autocompletion_text)
        else:
            print('- Autocompletion already available.')
            bashrc.close()
    except IOError as e:
        sys.exit(e)


def read_config_file(cfg_parser, filename):
    """
    Read configuration file and assign it to configParser object

    :param cfg_parser: configparser object
    :type cfg_parser: configparser.ConfigParser
    :param filename: name of file to read
    :type filename: str
    :return: corresponding filename if read is success
    :rtype: str
    """

    try:
        cfg_file = cfg_parser.read(filename)
        if cfg_file:
            return cfg_file[0]
    except (DuplicateOptionError, DuplicateSectionError) as d:  # pragma: no cover
        print('Duplicate Option/Section in file [%s] !' % filename)
        sys.exit(d)
    except Exception as ex:  # pragma: no cover - not testable
        print('Configuration file [%s] is missing !' % filename)
        sys.exit(ex)

    return None


def file_executable(filename):
    """
    Make filename executable

    :param filename: file to make executable
    :type filename: str
    """

    try:
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)
    except PermissionError as e:
        print(e)
        print('Can\'t make file executable: %s' % filename)
        sys.exit(1)
