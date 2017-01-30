===========
Alignak App
===========

*Alignak desktop application*

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-app.svg?branch=master
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-app
    :alt: Master branch build status

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-app.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-backend-import
    :alt: Develop branch build status

.. image:: https://landscape.io/github/Alignak-monitoring-contrib/alignak-app/master/landscape.svg?style=flat
   :target: https://landscape.io/github/Alignak-monitoring-contrib/alignak-app/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/github/Alignak-monitoring-contrib/alignak-app/badge.svg?branch=master
    :target: https://coveralls.io/github/Alignak-monitoring-contrib/alignak-app?branch=master
    :alt: Code coverage

.. image:: http://readthedocs.org/projects/alignak-app/badge/?version=latest
    :target: http://alignak-app.readthedocs.io/en/develop/?badge=latest
    :alt: Documentation Status

.. image:: https://badge.fury.io/py/alignak_app.svg
    :target: https://badge.fury.io/py/alignak_app
    :alt: Last PyPi version

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3


Alignak-App is a desktop application, residing in the system tray, for the Alignak framework. It can be installed on any Linux or Windows Dekstop / Server with a graphical interface which can run Python.

This application is useful for people with an Alignak installation in their business and who want to keep an eye on their supervision constantly.

Installation
============

To install Alignak-app::

    # For Linux users with python2
    sudo apt-get install python-qt4
    # For Linux and Windows users with python3
    pip3 install PyQt5 --user

    # For Windows users, we recommend using python3, else install PyQt from the download page

    # Alignak App
    pip install alignak_app --user

    # As of now, the last version is not yet pip installable, so we:
    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    pip install . --user

    # Run the app (1st run will finalize the installation)
    $HOME/.local/alignak_app/alignak-app start

    # Then you will be able for next runs to
    alignak-app start

You can find more help in the documentation below.

Documentation
=============

Documentation for Alignak-app is available on `Read The Docs <http://alignak-app.readthedocs.io/en/develop/index.html>`_.
You will find everything you need to install and configure the application.
To learn more about Alignak, visit `http://alignak-monitoring.github.io <http://alignak-monitoring.github.io/>`_ website.

Bugs / Enhancements
===================

Please open any issue or idea on this `repository <https://github.com/Alignak-monitoring-contrib/alignak-app/issues>`_.

Preview (Debian and Windows)
============================

.. image:: https://raw.githubusercontent.com/Alignak-monitoring-contrib/alignak-app/develop/docs/image/preview_deb.png
.. image:: https://raw.githubusercontent.com/Alignak-monitoring-contrib/alignak-app/develop/docs/image/preview_win.png
