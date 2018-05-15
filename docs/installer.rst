.. _installer:

Alignak-app Installers
**********************

Requirements
============

Alignak Suite
-------------

You must have Alignak Suite installed before using this app :

* `alignak <http://alignak-monitoring.github.io/>`_
* `alignak-backend <http://alignak-backend.readthedocs.io/en/latest/>`_

Alignak-app need at least a functionnal and available **alignak-backend** to connect with it !

Python 3
--------

You must have **Python 3** installed on your system. Only the Windows installer does not need to install Python 3.

Installation (Windows)
======================

An installer is available in repository of Alignak-app on `releases page <https://github.com/Alignak-monitoring-contrib/alignak-app/releases>`_.
It is **recommended** that you use this installer to run Alignak-app on Windows.

    **You have nothing else to install if you are using the installer !**

**IMPORTANT**: To keep it free, installer is not signed, so **Windows Defender SmartScreen** will warn you about that. Just click on "More Informations" and on "Execute anyway" to run installer.

**IMPORTANT:** This installer is currently only compatible with **x64** architecture !

You can also buid your own Windows installer (on **develop** branch for example), see :ref:`installer` for more information.

However, you can install the application in the same way as under Linux, but this will require you to keep a window open for Python.

Installation (Linux)
====================

You can install Alignak-app like other python libraries, with ``pip3``::

    pip3 install alignak_app

The required Python modules are automatically installed, if not present on your system.

Installation (From Sources)
===========================

Clone and install
-----------------

To install from source, clone repos and install with pip ::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    # If you're under Windows, use "pip" instead "pip3"
    pip3 install .

External Libraries
------------------

You need to install Python modules that are listed in ``requirements.txt`` file with pip:

    .. literalinclude:: ../requirements.txt

Under Windows
-------------

If you've installed Alignak-app with ``pip`` under Windows, you must link install directory with your ``Program Files`` folder. Otherwise, App won't start.

Open a command Windows console as admin and type the following line::

    mklink /J "%ProgramFiles%\Alignak-app" c:\Users\<USERNAME>\AppData\Roaming\Python\alignak_app

Replace ``<USERNAME>`` by your username.

Be sure also that you've install Python3 on your device.

Windows Setup
=============

For releases, a setup is generated for Windows and is available for `download <https://github.com/Alignak-monitoring-contrib/alignak-app/releases>`_.
For the version under development, you have to do it yourself.

Requirements
------------

Obviously, you must clone the Alignak-app repository, on the develop branch before.
Like that you'll have the last fixes. Normally, we try to have a branch ``develop`` as stable as possible.

Python and requirements
^^^^^^^^^^^^^^^^^^^^^^^

You have to install `Python 3.5 <https://www.python.org/downloads/release>`_ in any case.

Then the requirements of Alignak-app . Otherwize, *pyinstaller* will not have the required *.dll* for compilation.
All is available on **Pypi**::

    # In repository folder
    pip install -r requirements.txt --user

Once done, you'll normally have your python modules installed in::

    "%APPDATA%\Python\Python35\"

Then install *pyinstaller*.

Pyinstaller
^^^^^^^^^^^

The module ``pyinstaller`` is also available on **Pypi**. So just run the following command::

    pip install pyinstaller --user

Normally, *pyinstaller.exe* command will be available under::

    "%APPDATA%\Python\Python35\Scripts\"

And will be added to your *PATH* variable.
If it is not the case, you can add this folder to your *PATH* without problem, you will definitely need it for other python libraries.

Inno Setup
^^^^^^^^^^

`Inno Setup <http://www.jrsoftware.org/isinfo.php>`_ is a free installer for Windows.
It is very powerful and allows to create and customize installers quite easily.

To install Inno Setup, just download the last **unicode** version on `Official download <http://www.jrsoftware.org/isdl.php>`_ page.

**Be sure to choose unicode version !**

And simply run it with values as default.

Create Setup
------------

To create your own setup, you'll find scripts in ``bin\win`` folder of repository.
There is also images, a redistribuable for Windows (needed for old versions of Windows) and 2 script files.

The first one is ``pyinstaller_app.bat``.

**Before running it**, check the ``--paths`` arguments.
Normally, you'll have just to change the repository folder (line 13).

**Be sure to put absolute paths !**

The others are normally the sames on your device. If pyinstaller does not find the PyQt dll, check these paths.

Then run the *.bat*. This script will generate an ``alignak-app.exe`` in **dist** folder. Don't move it !

After, simply open the Inno Setup file ``alignak-app-win-setup.iss``. You can change *ShortVersion* if you want, but normally these digits are same as current develop.
And then, compile the file with ``CTRL+F9`` or from menu ``Build->Compile``.

This will generate an installer inside the ``dist\setup`` folder.

Your installer is ready !

You can then uninstall the python libraries if necessary, your Setup will no longer use them. All the libraries you need are compressed into the executable.