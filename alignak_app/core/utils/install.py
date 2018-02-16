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
    Settings manage configurations of Alignak-app
"""

import os
import sys
import stat
import subprocess

from logging import getLogger

from alignak_app import __alignak_url__, __doc_url__, __version__, __releasenotes__
from alignak_app import __libname__, __application__

logger = getLogger(__name__)


def create_user_app_dir(cfg_file):
    """
    Create a user folder for App configuration file and log

    :param cfg_file: file to copy if user has no rights
    :type cfg_file: str
    :return: return original file if user ha right, else the new file created
    :rtype: str
    """

    if not os.access(cfg_file, os.W_OK):
        # Create Folder for user if does not exist
        user_app_dir = '%s/.local/alignak_app' % os.environ['HOME']
        if not os.path.exists(user_app_dir):
            try:
                os.makedirs(user_app_dir)
            except (PermissionError, FileExistsError) as e:
                print(e)
                sys.exit('Can\'t create App directory for user in [%s] !' % user_app_dir)

        dest_file = os.path.join(user_app_dir, os.path.split(cfg_file)[1])
        # If file does not exist, App create it
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

        return cfg_file


def install_alignak_app(bin_file):
    """
    Install an "alignak-app" daemon for user

    :param bin_file: python file "alignak-app.py" who have been launched
    :type bin_file: str
    """

    print('----------- Install -----------')
    print('Installation...')

    if not os.path.isdir('%s/bin' % os.environ['HOME']):
        try:
            os.mkdir('%s/bin' % os.environ['HOME'])
        except IOError as e:
            print('%s fail to create bin directory!' % __application__)
            sys.exit(e)

    possible_paths = [
        '%s/bin' % os.environ['HOME'], '/usr/local/bin', 'usr/sbin'
    ]

    install_path = ''
    for path in possible_paths:
        if path in os.environ['PATH'] and os.access(path, os.W_OK):
            install_path = path

    if install_path:
        # Create daemon bash file
        daemon_name = 'alignak-app'
        bash_file = """#!/usr/bin/env bash
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

### BEGIN INIT INFO
# Provides:          alignak-app
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: alignak application notifier
# Description:       alignak-app is a notifier for Alignak suite.
### END INIT INFO

END='\\x1b[0m'
RED='\\x1b[31m'
GREEN='\\x1b[32m'
CYAN='\\x1b[36m'

LIB_NAME=%s
DAEMON=%s

BIN_FILE=%s
PYBIN=python3
export ALIGNAKAPP_APP_CFG=%s
export ALIGNAKAPP_USER_CFG=%s
export ALIGNAKAPP_LOG_DIR=%s

# Get version and doc_url of alignak-app
version="%s"
release_notes="%s"
project_url="%s"
doc_url="%s"

# Functions for alignak-app
usage() {
    echo "------------------------------------------"
    echo -e "$CYAN Alignak-app, Version $version $END \\n"
    echo "  $release_notes"
    echo "  For more help, visit $doc_url."
    echo "  Please open any issue on $project_url."
    echo "------------------------------------------"
    echo -e "$CYAN Alignak-app will use following variables: $END \\n"
    echo "ALIGNAKAPP_APP_CFG = $ALIGNAKAPP_APP_CFG"
    echo "ALIGNAKAPP_USER_CFG = $ALIGNAKAPP_USER_CFG"
    echo "ALIGNAKAPP_LOG_DIR = $ALIGNAKAPP_LOG_DIR"
    echo -e "\\n Usage: $GREEN $DAEMON {start|stop|status|restart} $END \\n"
}


do_start() {
    echo "------------------------------------------"
    echo -e "$GREEN Starting $DAEMON daemon $END..."
    echo "------------------------------------------"

    "$PYBIN" "$BIN_FILE" --start &
}

do_stop() {
    pid=`ps aux |grep "alignak-app.py"|grep -v "grep"|awk '{print $2}'`
    if [ ! -z "$pid" ]; then
        echo -e "$RED  Stop $DAEMON daemon... $END"
        echo "Kill pid: $pid"
        kill "$pid"
        echo "...$DAEMON stop !"
    else
        echo -e "$RED $DAEMON is not running ! $END"
    fi
}

do_status() {
    pid=`ps fu |grep "alignak-app.py"|grep -v "grep"|awk '{print $2}'`
    if [ ! -z "$pid" ]; then
        echo -e "$DAEMON is $GREEN running $END... (pid $pid)"
    else
        echo -e "$RED $DAEMON is not running ! $END"
        echo "Run $DAEMON start"
    fi

}

# Arguments
CMD=$1

case "$CMD" in
    start)
        do_start
    ;;
    stop)
        do_stop
    ;;
    restart)
        do_stop
        do_start
    ;;
    status)
        do_status
    ;;
    *)
        usage
        exit 1
esac
exit 0
        """ % (
            __libname__, daemon_name, bin_file, os.environ['ALIGNAKAPP_APP_CFG'],
            os.environ['ALIGNAKAPP_USER_CFG'], os.environ['ALIGNAKAPP_LOG_DIR'], __version__,
            __releasenotes__, __alignak_url__, __doc_url__,
        )

        print('Create daemon file...')
        filename = os.path.join(install_path, daemon_name)
        try:
            with open(filename, 'w') as daemon_file:
                daemon_file.write(bash_file)
        except Exception as e:
            print('%s can\'t create daemon file: %s' % (__application__, filename))
            sys.exit(e)

        try:
            st = os.stat(filename)
            os.chmod(filename, st.st_mode | stat.S_IEXEC)
        except Exception as e:
            print('%s can\'t set permissions on daemon file: %s' % (__application__, daemon_name))
            sys.exit(e)
        print('Installation is done ! You can run "%s" command !' % daemon_name)
    else:
        print('Please restart this script with a "root" user.')
