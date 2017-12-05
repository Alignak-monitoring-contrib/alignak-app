.. _install:

Install Alignak-app
===================

Requirements
------------

Alignak Suite
~~~~~~~~~~~~~

You must have Alignak Suite installed before using this app :

* `alignak`_
* `alignak-backend`_

Alignak-app need at least a functionnal and available **alignak-backend** to connect with it !

Windows Users
-------------

An installer is available in repository of Alignak-app on `releases page <https://github.com/Alignak-monitoring-contrib/alignak-app/releases>`_.
It is **recommended** that you use this installer to run Alignak-app on Windows.

    **You have nothing else to install if you are using the installer !**

**IMPORTANT**: To keep it free, installer is not signed, so **Windows Defender SmartScreen** will warn you about that. Just click on "More Informations" and on "Execute anyway" to run installer.

**IMPORTANT:** This installer is currently only compatible with **x64** architecture !

Linux Users
-----------

**IMPORTANT** Be sure to install this application with ``--user`` flags. Otherwise you may not be able to launch it !

You can install with pip::

    pip3 install alignak_app --user

The required Python modules are automatically installed if not present on your system.

An installation for root will be available as soon as possible.

From Sources
------------

External Libraries
~~~~~~~~~~~~~~~~~~

You need to install Python modules that are listed in ``requirements.txt`` file with pip:

    .. literalinclude:: ../requirements.txt

**Note**: if you proceed to an end-user installation with pip, the required modules are automatically installed.

Installation
~~~~~~~~~~~~

To install from source, clone repos and install with pip ::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    # If you're under Windows, use "pip" instead "pip3"
    pip3 install . --user

Under Windows
~~~~~~~~~~~~~

If you've installed Alignak-app with ``pip`` under Windows, you must link install directory with your ``Program Files`` folder. Otherwise, App won't start.

Open a command Windows console as admin and type the following line::

    mklink /J "%ProgramFiles%\Alignak-app" c:\Users\<USERNAME>\AppData\Roaming\Python\alignak_app

Replace ``<USERNAME>`` by your username.

Be sure also that you've install Python3 on your device.


.. _alignak: http://alignak-monitoring.github.io/
.. _alignak-backend: http://alignak-backend.readthedocs.io/en/latest/
.. _alignak-webui: http://alignak-web-ui.readthedocs.io/en/latest/
.. _alignak_backend_client: https://github.com/Alignak-monitoring-contrib/alignak-backend-client
.. _PyQt4 Official Website: https://www.riverbankcomputing.com/software/pyqt/download
.. _PyQt4 Official Tutorial: http://pyqt.sourceforge.net/Docs/PyQt4/installation.html
