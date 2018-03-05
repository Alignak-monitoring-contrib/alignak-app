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

.. image:: https://coveralls.io/repos/github/Alignak-monitoring-contrib/alignak-app/badge.svg?branch=develop
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

Features:
^^^^^^^^^

* *See Alignak daemons status (if activate in backend), number, states, informations of hosts and services*
* *Be notified for: problems, actions, changes*
* *View a synthesis view of a host and its services (states, output, checks)*
* *Acknowledge problems, schedule downtimes on your Hosts / Services*
* *Spy hosts*

And other features to come...

App use `PyQt5 <https://www.riverbankcomputing.com/software/pyqt/intro>`_, bindings of Qt application framework.

Installation
------------

To install Alignak-app:

* **Windows Users:**

.. code-block:: bash

    # An installer for Windows is available on this repository.
    # To keep it free, installer is not signed, so Windows Defender SmartScreen will warn you about that.
    # Just click on "More Informations" and on "Execute anyway" to run installer.

    # You can generate your own setup. Please, follow the documentation link below.

* **Linux Users:**

.. code-block:: bash

    # Alignak App
    pip3 install alignak_app

    # First run
    # Installed as "user"
    ~/.local/alignak_app/bin/alignak-app.py --start   # Run application in current shell
    ~/.local/alignak_app/bin/alignak-app.py --install # Install a daemon file
    # Installed as "root"
    /usr/local/aligna_app/alignak-app.py --start   # Run application in current shell
    /usr/local/aligna_app/alignak-app.py --install # Install a daemon file

    # If you've installed Alignak-app daemon, then run:
    alignak-app start

* **Development (Windows or Linux):**

.. code-block:: bash

    # If you want to test development version or a specific version, tags, commit run:
    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    # If you're under Windows, use "pip" instead of "pip3"
    pip3 install -r requirements.txt
    pip3 install . -v
    # Then run "alignak-app.py" file

You can find more help in the documentation below.

Documentation
-------------

Documentation for Alignak-app is available on `Read The Docs <http://alignak-app.readthedocs.io/en/develop/index.html>`_.
You will find everything you need to install and configure the application.

To learn more about **Alignak** project, please visit `http://www.alignak.net/ <http://www.alignak.net/>`_.

Release strategy
----------------

Alignak-app will *try* to follow the `Alignak-Backend <https://github.com/Alignak-monitoring-contrib/alignak-backend>`_ version.
As of it, take care to install the same minor version on your system to ensure compatibility between all the packages.
If your Backend is **1.1.0**, use Alignak-app **1.1.x**.

Bugs / Enhancements
-------------------

Please open any issue or idea on this `repository <https://github.com/Alignak-monitoring-contrib/alignak-app/issues>`_.

Preview
-------

.. image:: https://raw.githubusercontent.com/Alignak-monitoring-contrib/alignak-app/develop/docs/image/preview.png
