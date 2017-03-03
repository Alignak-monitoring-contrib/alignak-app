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
* `alignak-webui`_ (optional)

Alignak-app need at least a functionnal **alignak-backend** to connect with it.

Windows Users
~~~~~~~~~~~~~

An installer is available in repository of Alignak-app on `releases page <https://github.com/Alignak-monitoring-contrib/alignak-app/releases>`_.
It is **recommended** that you use this installer to run Alignak-app on Windows.

    **You have nothing else to install if you are using the installer !**

If you want to install Alignak-app with ``pip3``, you must link install directory with your ``Program Files`` folder.
Open a command Windows console as admin and type the following line::

    mklink /J "%ProgramFiles%\Alignak-app" c:\Users\<USERNAME>\AppData\Roaming\Python\alignak_app

Replace *<USERNAME>* by your username.

External Libraries
~~~~~~~~~~~~~~~~~~

You need to install Python modules that are listed in ``requirements.txt`` file with pip:

    .. literalinclude:: ../requirements.txt

**Note**: if you proceed to an end-user installation with pip, the required modules are automatically installed.

Installation
------------

**Note:** Be sure to install this application with ``--user`` flags. Otherwise you may not be able to launch it !
**Note:** If you install "App" with the installer, you do not need to install Python or other libraries.

End user installation
~~~~~~~~~~~~~~~~~~~~~

You can install with pip::

    pip3 install alignak_app --user

The required Python modules are automatically installed if not present on your system.

From Sources
~~~~~~~~~~~~

To install from source, clone repos and install with pip ::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    pip install . --user

Installer (Windows only)
~~~~~~~~~~~~~~~~~~~~~~~~

An installer is available on `Alignak-app repository <https://github.com/Alignak-monitoring-contrib/alignak-app/tree/develop/bin/win>`_ for Windows.
It already contains the application and required libraries.

**IMPORTANT:** This installer is currently only compatible with **x64** architecture !

.. _alignak: http://alignak-monitoring.github.io/
.. _alignak-backend: http://alignak-backend.readthedocs.io/en/latest/
.. _alignak-webui: http://alignak-web-ui.readthedocs.io/en/latest/
.. _alignak_backend_client: https://github.com/Alignak-monitoring-contrib/alignak-backend-client
.. _PyQt4 Official Website: https://www.riverbankcomputing.com/software/pyqt/download
.. _PyQt4 Official Tutorial: http://pyqt.sourceforge.net/Docs/PyQt4/installation.html
