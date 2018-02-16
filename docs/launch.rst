.. _launch:

Launch Alignak-App
==================

On Linux
~~~~~~~~

First launch
************

Once you have install Alignak-app, just run `alignak-app.py` file. This file should be located in::

    # If install by pip as user
    $HOME/.local/alignak_app/bin/alignak-app.py
    # If install by pip as root
    /usr/local/alignak_app/bin/alignak-app.py

To launch application use ``--start``::

    /usr/local/alignak_app/bin/alignak-app.py --start

To generate an Alignak-app daemon file, use ``--install``::

    /usr/local/alignak_app/bin/alignak-app.py --install

If you have set environment variables for application, they will be added to the generated script (see :ref:`config`).

Launch daemon
*************

Once installed, just run::

    alignak-app start

Here is the available commands::

    alignak-app {start|stop|status|restart}

With no parameters, this will display help and your environment variables configuration.

**Note:** To generate a new daemon file with other environment variable, just run ``alignak-app.py --install`` again.

On Windows
~~~~~~~~~~

With Installer
**************

Just launch ``Alignak-app vX.x`` shorcut on your desktop or run the ``alignak-app.exe`` located in ``C:\Program Files\Alignak-app\``.

From command line
*****************

If you install from sources or with pip, you just have to launch the ``alignak-app.py`` in ``bin`` folder::

    python c:\Users\user\AppData\Roaming\Python\alignak_app\bin\alignak-app.py --start

Obviously, it requires to keep an open command prompt on Windows.

**Note:** There is no daemon available on Windows, please use provided setup.

Solve Problems
==============

If you're having trouble getting started and running the app, here are some things to check:

1. Be sure you have correctly set your configuration file (see above) and that you can join your backend.
2. The application generates a log file in its root folder (see :ref:`config`). Search for ``ERROR`` messages.
3. If you have installed Alignak-app with pip, be sure to add the flag *--user* (see :ref:`install`).


