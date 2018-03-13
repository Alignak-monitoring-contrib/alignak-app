.. _use:

Use Alignak-App
###############

Run "App"
*********

On Linux
========

First launch
------------

Once you have install Alignak-app, just run `alignak-app.py` file. This file should be located in::

    # If install by pip as user
    $HOME/.local/alignak_app/bin/alignak-app.py
    # If install by pip as root
    /usr/local/alignak_app/bin/alignak-app.py

To launch application use ``--start``::

    /usr/local/alignak_app/bin/alignak-app.py --start

If you have set environment variables for application, they will be added to the generated daemon script (see :ref:`config`).

To generate an Alignak-app daemon file, use ``--install``::

    /usr/local/alignak_app/bin/alignak-app.py --install

Launch daemon
-------------

Once installed, just run::

    alignak-app start

Here is the available commands::

    alignak-app {start|stop|status|restart}

With no parameters, this will display help and your environment variables configuration.

**Note:** To generate a new daemon file with other environment, just run ``alignak-app.py --start`` again with your new environment variables.

On Windows
==========

With Installer
--------------

Just launch ``Alignak-app vX.x`` shorcut on your desktop or run the ``alignak-app.exe`` located in ``C:\Program Files\Alignak-app\``.

From command line
-----------------

If you install from sources or with pip, you just have to launch the ``alignak-app.py`` in ``bin`` folder::

    python c:\Users\user\AppData\Roaming\Python\alignak_app\bin\alignak-app.py --start

Obviously, it requires to keep an open command prompt on Windows.

**Note:** There is no daemon available on Windows, please use provided setup.

Interface
*********

Login Window
============

If you have not set your configuration file, Alignak-app will display a login window by default.
In this window, you'll be able to:

* Configure your Alignak server (by clicking on **server** icon).
* Type your **username** and **password** to login.

Start
=====

Once you're connected, Alignak-app will start and show you a progress bar. Time to start will depend on your installation (a backend with a lot of host and services will take more time).

When Alignak-app has started, you'll have:

* The **Main Window** of App, separated into two parts:

  * The "App Dock" (Right part)
  * The "App Panel" (Left part)

* A **Tray Icon** in your task bar. This icon gives you access to a menu with:

  * Alignak-app menu, to view the app if it has been reduced
  * About menu, to show informations of Alignak-app
  * Reload menu, to reload your configuration.

Other menu will come in future versions.

App Dock (Right part)
=====================

When App is launched, the right part (called "dock") will contains different buttons and some container who will receive different notifications.

Alignak part
------------

This part of dock contains informations about your connection to backend and the states of Alignak daemons.
If you've some connection problems or if backend is restart, you'll see icons change.

You can also see each daemon state by clicking on button with Alignak icon.

Livestate part
--------------

In the livestate part, you'll have many buttons who let you see: hosts, user configuration, problems view (available soon) and a button to reach your WebUI if available.

You'll also see a resume of number of problems for hosts and services monitored in your backend.

Events part
-----------

This is one of the most interesting features of the application. You'll receive many informations in this part like alignak notifications, acknowledge or modifications you do in App.

**Events:**

  * If you want to remove an event, simply double click on it.
  * Full events text can be see in tooltip when you keep mouse over.
  * Some events are temporary and remove themselves.
  * Some events can be drag and drop (see below)

**Drag & Drop:**

  * Events from a host or a service can be drag to in "Spy Hosts". Then App will send you regular notifications about that host.
  * Events can also be move to host synthesis view (Panel), to display host instantly.

Spy part
--------

This is where you can find the list of hosts that you spy on.

  * You can spy on as many hosts as you want.
  * To stop spying on a host, just double click on it, host will be removed from list.

App Panel (Left part)
=====================

The left part of application (called "Panel"), will display a **Hosts Synthesis View**. This is where you can see your monitored hosts and services.

Host Synthesis
--------------

**Dashboard:**

At the top of this window, you will find a dashboard with the number of items, for each state (OK, CRITICAL, DOWN...).

**Host View:**

Start typing the name of a host in the search bar and App will propose to you different corresponding names.
When you select a host, its information and the list of its services will be displayed.

*Services:*

When a host is displayed, you will have the list of services, classified by aggregation. Click on one of them to display them.

If you click on a service, a summary of its status will be displayed on the right.

**Actions:**
You will then be able to perform various actions such as seeing the details of each of its services, acknowledging a problem or planning a downtime for an item (service or host).

You will also have access to the host's history. It may take a while to be available.

Another tab called "Problems" is used to display the problems listed by the backend (like a DOWN host or a CRITICAL service).

Problems
--------

Other tab will display problems found by Alignak-app in backend.

This will bring together down hosts, critical services or any other worries, such as an unreachable host.

You'll be able to acknowledge problems or trigger downtimes.

WebUI Integration
=================

App also have lot of buttons which bring you to WebUI. You've to set WebUI url in configuration file to make this buttons available.

App will be aware also on events trigger in WebUI in host history.
