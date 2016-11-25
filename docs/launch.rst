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

You just have to launch the ``alignak-app.py`` in ``bin`` folder::

    python c:\Users\user\AppData\Roaming\Python\alignak_app\bin\alignak-app.py

Obviously, for the time it requires to have an open command prompt on Windows. A more complete installer will arrive soon

Solve Problems
==============

If you're having trouble getting started and running the app, here are some things to check:

1. Be sure you have correctly set your configuration file (see above) and that you can join your backend.
2. Do you use the correct version of Python to run the script ?
3. The application generates a log file in its root folder (see :ref:`config`). Check that there are no error messages.
4. Alignak-App must be installed in your `$HOME` folder, defines by the ``--user`` pip parameter (see :ref:`install`).
