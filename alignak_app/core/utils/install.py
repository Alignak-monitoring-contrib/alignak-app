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

# Variables
END='\\x1b[0m'
RED='\\x1b[31m'
GREEN='\\x1b[32m'
CYAN='\\x1b[36m'

DAEMON=%s
BIN_FILE=%s
PYBIN=python3

export ALIGNAKAPP_APP_CFG=%s
export ALIGNAKAPP_USER_CFG=%s
export ALIGNAKAPP_LOG_DIR=%s

APP_VERSION="%s"
APP_RELEASE_NOTES="%s"
APP_PROJECT_URL="%s"
APP_DOC_URL="%s"

# Functions for alignak-app
usage() {
    echo "------------------------------------------"
    echo -e "$CYAN Alignak-app, Version $APP_VERSION $END \\n"
    echo "  $APP_RELEASE_NOTES"
    echo "  For more help, visit $APP_DOC_URL."
    echo "  Please open any issue on $APP_PROJECT_URL."
    echo "------------------------------------------"
    echo -e "$CYAN Alignak-app will use following variables: $END \\n"
    echo "ALIGNAKAPP_APP_CFG = $ALIGNAKAPP_APP_CFG"
    echo "ALIGNAKAPP_USER_CFG = $ALIGNAKAPP_USER_CFG"
    echo "ALIGNAKAPP_LOG_DIR = $ALIGNAKAPP_LOG_DIR"
    echo -e "\\n Usage: $GREEN $DAEMON {start|stop|status|restart} $END \\n"
}


do_start() {
    PID=`ps aux |grep "alignak-app.py"|grep -v "grep"|awk '{print $2}'`
    if [ ! -z "$PID" ]; then
        echo "--------------------------------------------------"
        echo -e "$CYAN $DAEMON is already running ;) $END"
        echo "--------------------------------------------------"
    else
        echo "--------------------------------------------------"
        echo -e "$GREEN $DAEMON v$APP_VERSION start... $END"
        echo "--------------------------------------------------"
        "$PYBIN" "$BIN_FILE" --start &
    fi
}

do_stop() {
    PID=`ps aux |grep "alignak-app.py"|grep -v "grep"|awk '{print $2}'`
    if [ ! -z "$PID" ]; then
        echo "--------------------------------------------------"
        echo -e "$RED $DAEMON is stopping... (Kill pid $PID) $END"
        kill "$PID"
        echo -e "...$DAEMON stop !"
        echo "--------------------------------------------------"
    else
        echo "--------------------------------------------------"
        echo -e "$CYAN $DAEMON is not running ;) $END"
        echo "--------------------------------------------------"
    fi
}

do_status() {
    PID=`ps fu |grep "alignak-app.py"|grep -v "grep"|awk '{print $2}'`
    if [ ! -z "$PID" ]; then
        echo "--------------------------------------------------"
        echo -e "$GREEN $DAEMON is running...$END (pid $PID)"
        echo "--------------------------------------------------"
    else
        echo "--------------------------------------------------"
        echo -e "$CYAN $DAEMON is not running ! $END"
        echo -e "Run $GREEN '$DAEMON start' $END to launch Alignak-app"
        echo "--------------------------------------------------"
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
    shortlist)
      echo "start stop restart status"
    ;;
    *)
        usage
        exit 1
esac
exit 0
"""

bash_autocomplete = """_script()
{
  _script_commands=$(%s shortlist)

  local cur
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  COMPREPLY=( $(compgen -W "${_script_commands}" -- ${cur}) )

  return 0
}
complete -o bashdefault -o nospace -F _script %s
"""


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
            # Make file executable
            try:
                st = os.stat(file_to_write)
                os.chmod(file_to_write, st.st_mode | stat.S_IEXEC)
                returncode = 0
            except Exception as e:
                returncode = '%s can\'t set permissions on daemon file: %s\n%s' % (
                    __application__, file_to_write, str(e))

        if 'autocomplete' in args:
            # Source file
            autocompletion_text = '\n# Alignak-app completion:\n. %s' % file_to_write
            user_rc = '%s/.bashrc' % os.environ['HOME']

            try:
                bashrc = open(user_rc, 'r')
                if 'Alignak-app completion' not in bashrc.read():
                    bashrc.close()
                    with open(user_rc, 'a') as cur_file:
                        cur_file.write(autocompletion_text)
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
        '%s/bin' % os.environ['HOME'], '/usr/local/bin', 'usr/sbin'
    ]

    install_path = ''
    for path in possible_paths:
        if path in os.environ['PATH'] and os.access(path, os.W_OK):
            install_path = path

    if install_path:
        # Start installation
        print('----------- Install -----------\nInstallation start...\n')

        # Create daemon bash file
        daemon_name = 'alignak-app'
        bash_format = bash_file % (
            daemon_name, bin_file, os.environ['ALIGNAKAPP_APP_CFG'],
            os.environ['ALIGNAKAPP_USER_CFG'], os.environ['ALIGNAKAPP_LOG_DIR'], __version__,
            __releasenotes__, __alignak_url__, __doc_url__,
        )
        status = check_return_code(
            write_file(install_path, daemon_name, bash_format, 'exec')
        )
        print('Create daemon file...%s\n' % status)

        # Create autocomplete file
        autocomplete_name = '%s-autocomplete.sh' % daemon_name
        autocomplete_format = bash_autocomplete % (
            os.path.join(install_path, daemon_name), daemon_name
        )
        status = check_return_code(
            write_file(install_path, autocomplete_name, autocomplete_format, 'autocomplete')
        )
        print('Add auto completion...%s\n' % status)

        # Installation is done !
        print('Installation is done ! You can run "%s" command !' % daemon_name)
    else:
        print('Please restart this script with a "root" user.')
