.. _installer:

Alignak-app Installers
======================

Requirements
------------

Alignak Suite
~~~~~~~~~~~~~

You must have Alignak Suite installed before using this app :

* `alignak`_
* `alignak-backend`_

Alignak-app need at least a functionnal and available **alignak-backend** to connect with it !

Python 3
~~~~~~~~

You must have **Python 3** installed on your system. Only the Windows installer does not need to install Python 3.

Installation (Windows)
----------------------

An installer is available in repository of Alignak-app on `releases page <https://github.com/Alignak-monitoring-contrib/alignak-app/releases>`_.
It is **recommended** that you use this installer to run Alignak-app on Windows.

    **You have nothing else to install if you are using the installer !**

**IMPORTANT**: To keep it free, installer is not signed, so **Windows Defender SmartScreen** will warn you about that. Just click on "More Informations" and on "Execute anyway" to run installer.

**IMPORTANT:** This installer is currently only compatible with **x64** architecture !

You can also buid your own Windows installer (on **develop** branch for example), see :ref:`setup` for more information.

However, you can install the application in the same way as under Linux, but this will require you to keep a window open for Python.

Installation (Linux)
--------------------

You can install Alignak-app like other python libraries, with ``pip3``::

    pip3 install alignak_app

The required Python modules are automatically installed, if not present on your system.

If you install App as a root user (with ``sudo``), you have to run ``--install`` command before launch Alignak-App ! (see :ref:`launch`)

Installation (From Sources)
---------------------------

Clone and install
~~~~~~~~~~~~~~~~~

To install from source, clone repos and install with pip ::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    # If you're under Windows, use "pip" instead "pip3"
    pip3 install .

External Libraries
~~~~~~~~~~~~~~~~~~

You need to install Python modules that are listed in ``requirements.txt`` file with pip:

    .. literalinclude:: ../requirements.txt

Under Windows
~~~~~~~~~~~~~

If you've installed Alignak-app with ``pip`` under Windows, you must link install directory with your ``Program Files`` folder. Otherwise, App won't start.

Open a command Windows console as admin and type the following line::

    mklink /J "%ProgramFiles%\Alignak-app" c:\Users\<USERNAME>\AppData\Roaming\Python\alignak_app

Replace ``<USERNAME>`` by your username.

Be sure also that you've install Python3 on your device.

.. _alignak: http://alignak-monitoring.github.io/
.. _alignak-backend: http://alignak-backend.readthedocs.io/en/latest/
