.. _run:

Run
***

Alignak-App Launcher
====================

.. automodule:: alignak_app.app

Linux Daemon
============

If you have set environment variables for application, they will be added to the generated daemon script (see :ref:`config`).

Here is the available commands for daemon::

    Usage:
        # Without parameters
        alignak-app             Displays the help message and configured environment variables.

        # With parameters
        alignak-app start       Start Alignak-app daemon.
        alignak-app stop        Stop Alignak-app daemon.
        alignak-app status      Show status of daemon running.
        alignak-app restart     Stop and restart application.

**Note:** To generate a new daemon file with other environment, just run ``alignak-app-launcher --install`` again with your new environment variables.

Windows Installer
=================

If you used the installer provided in the repository or did you generate your own, just launch **Alignak-app vX.x** shorcut on your desktop.

All files have been installed in ``C:\Program Files\Alignak-app\``.
