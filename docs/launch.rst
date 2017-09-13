.. _launch:

Launch Alignak-App
==================

On Linux
~~~~~~~~

Once you have configured your application, just type the following in a terminal::

    $HOME/.local/alignak_app/alignak-app start

Alignak-app will start, but will also create a command for later. Thereafter, you will only have to type the following command to launch your application::

    alignak-app start

Here is the available commands::

    alignak-app {start|stop|status|restart}

On Windows
~~~~~~~~~~

With Installer
**************

Just launch ``Alignak-app vX.x`` shorcut on your desktop or run the ``alignak-app.exe`` located in ``C:\Program Files\Alignak-app\``.

From command line
*****************

If you install from sources or with pip, you just have to launch the ``alignak-app.py`` in ``bin`` folder::

    python c:\Users\user\AppData\Roaming\Python\alignak_app\bin\alignak-app.py

Obviously, it requires to keep an open command prompt on Windows.

Solve Problems
==============

If you're having trouble getting started and running the app, here are some things to check:

1. Be sure you have correctly set your configuration file (see above) and that you can join your backend.
2. The application generates a log file in its root folder (see :ref:`config`). Search for ``ERROR`` messages.
3. If you have installed Alignak-app with pip, be sure to add the flag *--user* (see :ref:`install`).


