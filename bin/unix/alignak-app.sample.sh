#!/usr/bin/env sh
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
# Description:       alignak-app is a desktop application for Alignak solution.
### END INIT INFO

#############################################################################
#                                                                           #
#                           DAEMON ALIGNAK-APP                              #
#                                                                           #
#############################################################################

# Variables
DAEMON=%s
BIN_FILE=%s
PYBIN=python3

export ALIGNAKAPP_APP_DIR=%s
export ALIGNAKAPP_USR_DIR=%s
export ALIGNAKAPP_LOG_DIR=%s

APP_VERSION="%s"
APP_RELEASE_NOTES="%s"
APP_PROJECT_URL="%s"
APP_DOC_URL="%s"

# Functions for alignak-app
usage() {
    echo "------------------------------------------"
    echo "Alignak-app, Version $APP_VERSION \n"
    echo "\t$APP_RELEASE_NOTES"
    echo "\tFor more help, visit $APP_DOC_URL."
    echo "\tPlease open any issue on $APP_PROJECT_URL."
    echo "------------------------------------------"
    echo "Alignak-App Environment: \n"
    echo "\tALIGNAKAPP_APP_DIR = $ALIGNAKAPP_APP_DIR"
    echo "\tALIGNAKAPP_USR_DIR = $ALIGNAKAPP_USR_DIR"
    echo "\tALIGNAKAPP_LOG_DIR = $ALIGNAKAPP_LOG_DIR"
    echo "\n Usage: $DAEMON {start|stop|status|restart} \n"
}


do_start() {
    PID=`ps aux |grep "alignak-app.py"|grep -v "grep"|awk '{print $2}'`
    if [ ! -z "$PID" ]; then
        echo "--------------------------------------------------"
        echo " $DAEMON is already running ;) "
        echo "--------------------------------------------------"
    else
        echo "--------------------------------------------------"
        echo " $DAEMON v$APP_VERSION start... "
        echo "--------------------------------------------------"
        "$PYBIN" "$BIN_FILE" --start &
    fi
}

do_stop() {
    PID=`ps aux |grep "alignak-app.py"|grep -v "grep"|awk '{print $2}'`
    if [ ! -z "$PID" ]; then
        echo "--------------------------------------------------"
        echo " $DAEMON is stopping... (Kill pid $PID) "
        kill "$PID"
        echo "...$DAEMON stop !"
        echo "--------------------------------------------------"
    else
        echo "--------------------------------------------------"
        echo " $DAEMON is not running ;) "
        echo "--------------------------------------------------"
    fi
}

do_status() {
    PID=`ps fu |grep "alignak-app.py"|grep -v "grep"|awk '{print $2}'`
    if [ ! -z "$PID" ]; then
        echo "--------------------------------------------------"
        echo " $DAEMON is running... (pid $PID)"
        echo "--------------------------------------------------"
    else
        echo "--------------------------------------------------"
        echo " $DAEMON is not running ! "
        echo "Run '$DAEMON start' to launch Alignak-app"
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