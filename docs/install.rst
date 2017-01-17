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
* `alignak-webui`_ 

Alignak-app need at least a functionnal **alignak-backend** to connect with it.

Before install
~~~~~~~~~~~~~~

Please **READ** the following lines before to begin:

**Note for Windows users:** An installer is available in repository of Alignak-app, under `win folder <https://github.com/Alignak-monitoring-contrib/alignak-app/tree/develop/bin/win>`_.
PyQt5 and Python3 are more easy to install if you want to install from sources or with pip.

**Note for Linux users:** PyQt5 and Python 3 are recommended, but not required.
A ``.desktop``, named **alignak-app.desktop**, is available in repository of Alignak-app under `unix folder <https://github.com/Alignak-monitoring-contrib/alignak-app/tree/develop/bin/unix>`_
to create a shorcut with "Stop" and "Restart" actions.

PyQT
~~~~

You must install a version of **PyQt**, compatible with your python version.

"App" support PyQt4 and PyQt5, there is many tutorial on web who explains how to install it.
But below, you'll find "quick install" for Linux and Windows:

Linux
*****

For PyQt4, it's often available with your distribution packages::

    sudo apt-get install python-qt4

Pyqt5 is directly available via pip but only for Python 3.5::

    pip3 install PyQt5 --user

Windows
*******

**Note:** If you install "App" with the installer, you do not need to do this step.

For PyQt4:

* Download the correct executable on `PyQt4 Official Website`_.
* Be sure to have **the same architecture** as your **Python version** (`x86` or `x64`).
* Then simply run installer.

Pyqt5 installs in the same way as Linux and is only available for Python 3.5::

    pip3 install PyQt5 --user


External Libraries
~~~~~~~~~~~~~~~~~~

Then, simply install Python modules that are listed in ``requirements.txt`` file with pip:

    .. literalinclude:: ../requirements.txt

**Note**: if you proceed to an end-user installation with pip, the required modules are automatically installed.

Installation
------------

**Note:** Be sure to install this application with ``--user`` flags. Otherwise you may not be able to launch it !
**Note:** If you install "App" with the installer, you do not need to install Python or other libraries.

End user installation
~~~~~~~~~~~~~~~~~~~~~

You can install with pip::

    pip install alignak_app --user

The required Python modules are automatically installed if not present on your system.
Obviously, you should use ``pip3`` to install for Python 3.

From Sources
~~~~~~~~~~~~

To install from source, clone repos and install with pip ::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    pip install . --user

Installer (Windows only)
~~~~~~~~~~~~~~~~~~~~~~~~

An installer is available on `Alignak-app repository <https://github.com/Alignak-monitoring-contrib/alignak-app/tree/develop/bin/win>`_ for Windows.
It already contains the application and required libraries. Installing Python and PyQt is not necessary !

**IMPORTANT:** This installer is only compatible with **x64** architecture !

.. _alignak: http://alignak-monitoring.github.io/
.. _alignak-backend: http://alignak-backend.readthedocs.io/en/latest/
.. _alignak-webui: http://alignak-web-ui.readthedocs.io/en/latest/
.. _alignak_backend_client: https://github.com/Alignak-monitoring-contrib/alignak-backend-client
.. _PyQt4 Official Website: https://www.riverbankcomputing.com/software/pyqt/download
.. _PyQt4 Official Tutorial: http://pyqt.sourceforge.net/Docs/PyQt4/installation.html
