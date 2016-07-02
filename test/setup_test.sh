#!/usr/bin/env bash
#

set -e

THIS_PATH=$(dirname "$0")
BASE_PATH=$(dirname "$THIS_PATH")

cd $BASE_PATH

sudo apt-get update
sudo apt-get install -qq python-gi gir1.2-gtk-3.0 ibus gir1.2-appindicator3-0.1 gir1.2-notify-0.7 gir1.2-glib-2.0

echo 'Upgrade pip ...'
pip install --upgrade pip

# install prog AND tests requirements :
echo 'Installing application requirements ...'
pip install -r requirements.txt
echo 'Installing application in development mode ...'
pip install -e .
echo 'Installing tests requirements ...'
pip install --upgrade -r test/requirements.txt
