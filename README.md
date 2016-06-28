# AppAlignak

# Introduction

Alignak-App is an appindicator for [Alignak](https://alignak-monitoring.github.io). It will display number of Hosts (and in future version number of Services) who are DOWN or UP.

If some of them change to DOWN, you'll have a notification on your desktop.

# Requirements

1. You must have [alignak-backend](http://alignak-backend.readthedocs.io/en/latest/) and [alignak-webui](http://alignak-web-ui.readthedocs.io/) installed before running.

2. **You must have a system compatible with GTK to run it !**

3. Install `python` and `pip`:

`sudo apt-get install python python-pip`

4. You have to install requirements with pip. Just run:

`pip install -r requirements.txt`

> **WARNING:** currently you have to install `alignak_backend_client` by running `setup.py` of [Github Project](https://github.com/Alignak-monitoring-contrib/alignak-backend-client).

# Launch App

Just run :

`python appalignak.py &`

You should normally have an icon of Alignak in your notification bar.

You can open and see how many of Hosts (or Services) are DOWN or UP. If you click a menu, it will open a web page to your Webui.

You can exit app just by clicking on `Quit`.

# Bugs / Enhancements

Please open any issue or idea in this repository.
