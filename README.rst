===========
Alignak App
===========

*Alignak desktop application*

.. image:: https://travis-ci.org/Alignak-monitoring-contrib/alignak-app.svg?branch=develop
    :target: https://travis-ci.org/Alignak-monitoring-contrib/alignak-app
    :alt: Develop branch build status

.. image:: https://landscape.io/github/Alignak-monitoring-contrib/alignak-app/develop/landscape.svg?style=flat
   :target: https://landscape.io/github/Alignak-monitoring-contrib/alignak-app/develop
   :alt: Development code static analysis

.. image:: https://coveralls.io/repos/github/Alignak-monitoring-contrib/alignak-app/badge.svg?branch=develop&service=github
    :target: https://coveralls.io/github/Alignak-monitoring-contrib/alignak-app?branch=develop
    :alt: Development code coverage

.. image:: http://readthedocs.org/projects/alignak-app/badge/?version=latest
    :target: http://alignak-app.readthedocs.io/en/latest/?badge=latest
    :alt: Latest documentation Status

.. image:: http://readthedocs.org/projects/alignak-app/badge/?version=develop
    :target: http://alignak-app.readthedocs.io/en/develop/?badge=develop
    :alt: Development documentation Status

.. image:: https://badge.fury.io/py/alignak_app.svg
    :target: https://badge.fury.io/py/alignak_app
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3

Short description
-----------------

Alignak-App is a desktop application, residing in the system tray, for the Alignak framework. It can be installed on any Linux or Windows Dekstop / Server with a graphical interface which can run Python.

This application is useful for people with an Alignak installation in their business and who want to keep an eye on their supervision constantly.

It is used to :

* Get Alignak daemons status, number of hosts and services per state
* Be notified when problems are raised by Alignak
* View, in real time, an host synthesis (host and its services state)
* Acknowledge problems or schedule downtimes on your Hosts / Services

App use `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/intro>`_, bindings of Qt application framework.

Installation
------------

To install Alignak-app::

    ##### WINDOWS USERS #####
    # An installer for Windows is available on this repository.
    # To keep it free, installer is not signed, so Windows Defender SmartScreen will warn you about that.
    # Just click on "More Informations" and on "Execute anyway" to run installer.

    ##### LINUX USERS #####
    # Alignak App
    pip3 install alignak_app --user -v

    # First run
    ~/.local/alignak_app/bin/alignak-app

    # If you've already run App, just do
    alignak-app start

    ##### Development #####
    # If you want development version, run:
    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    pip3 install -r requirements.txt
    pip3 install . --user -v

You can find more help in the documentation below.

Documentation
-------------

Documentation for Alignak-app is available on `Read The Docs <http://alignak-app.readthedocs.io/en/develop/index.html>`_.
You will find everything you need to install and configure the application.
To learn more about Alignak, visit `http://www.alignak.net/ <http://www.alignak.net/>`_ website.

Bugs / Enhancements
-------------------

Please open any issue or idea on this `repository <https://github.com/Alignak-monitoring-contrib/alignak-app/issues>`_.

Preview
-------

.. image:: https://raw.githubusercontent.com/Alignak-monitoring-contrib/alignak-app/develop/docs/image/preview.png
