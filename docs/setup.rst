.. _setup:

Windows Setup
=============

Requirements
------------

For releases, a setup is generated for Windows and is available for `download <https://github.com/Alignak-monitoring-contrib/alignak-app/releases>`_.
For the version under development, the Windows setup is not necessarily up to date.

But you can create your own. Obviously, you must clone the Alignak-app repository, on the develop branch before.
Like that you'll have the last fixes. Normally, we try to have a branch develop as stable as possible.

Python 3.5 and PyQt5
~~~~~~~~~~~~~~~~~~~~

You have to install `Python 3.5 <https://www.python.org/downloads/release>`_ in any case.

Then the requirements of Alignak-app and PyQt5 to build setup. Otherwize, *pyinstaller* will not have the required *.dll* for compilation.
All is available on **Pypi**::

    # In repository folder
    pip install -r requirements.txt --user
    # Then PyQt5
    pip install pyqt5 --user

Once done, you'll have your python modules installed in::

    "%APPDATA%\Python\Python35\"

Then install *pyinstaller*.

Pyinstaller
~~~~~~~~~~~

The module ``pyinstaller`` is also available on **Pypi**. So just run the following command::

    pip install pyinstaller --user

Normally, *pyinstaller.exe* command will be available under::

    "%APPDATA%\Python\Python35\Scripts\"

And will be added to your *PATH* variable.

Inno Setup
~~~~~~~~~~

`Inno Setup <http://www.jrsoftware.org/isinfo.php>`_ is a free installer for Windows.
It is very powerful and allows to create and customize installers quite easily.

To install Inno Setup, just download the last **unicode** version on `Official download <http://www.jrsoftware.org/isdl.php>`_ page.

**Be sure to choose unicode version !**

And simply run it with values as default.

Create Setup
------------

To create your own setup, you'll find scripts in ``bin\win`` folder of repository.
Inside, sometimes you'll have a BETA setup. There is also images, a redistribuable for Windows (needed for old versions of Windows) and 2 script files.

The first one is ``pyinstaller_app.bat``.

**Before running it**, check the ``--paths`` arguments.
Normally, you'll have just to change the repository folder (line 13).

**Be sure to put absolute paths !**

The others are normally the sames on your device.

Then run the *.bat*. This script will generate an ``alignak-app.exe`` in **dist** folder. Don't move it !

After, simply open the Inno Setup file ``alignak-app-win-setup.iss``. You can change *ShortVersion* if you want, but normally these digits are rights.
And then, compile the file with ``CTRL+F9`` or from menu ``Build->Compile``.

This will generate an installer inside the ``dist\setup`` folder.

Your installer is ready !