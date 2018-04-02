.. _interface:

Interface
#########

Login Window
************

If you have not set your configuration file, Alignak-app will display a login window by default.
In this window, you'll be able to:

* Configure your Alignak server (by clicking on **server** icon).
* Type your **username** and **password** to login.

Start
*****

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
*********************

When App is launched, the right part (called "dock") will contains different buttons and some container who will receive different notifications.

Alignak
=======

This part of dock contains informations about your connection to backend and the states of Alignak daemons.
If you've some connection problems or if backend is restart, you'll be notified here.

You can also see each daemon state by clicking on button with Alignak icon, if endpoint is available in backend.

Finally, you can see your profile by clicking on the button.

Livestate part
==============

In the livestate part, you'll see a resume of number of problems and items monitored in your backend.

Events part
===========

This is one of the most interesting features of the application. You'll receive many informations in this part like alignak notifications, acknowledge or modifications you do in App.

**Events:**

  * If you want to remove an event, simply double click on it.
  * Some events are temporary and remove themselves.
  * Some events can be drag and drop (see below)
  * Full events text can be see in tooltip when you keep mouse over.

**Drag & Drop:**

  * Events from an host or a service can be drag and dropped in "Spied Hosts" tab.
  * Events can also be moved to Host Synthesis view (Panel), to display host instantly.

App Panel (Left part)
*********************

The left part of application (called "Panel"), will display a **Hosts Synthesis View**. This is where you can see your monitored hosts and services.

Dashboard
=========

At the top of this window, you will find a dashboard with the number of items, for each state (OK, CRITICAL, DOWN, ACKNOWLEDGED...).

Host Synthesis
==============

Host View
---------

Start typing the name of a host in the search bar and App will propose to you different corresponding names.
When you select a host, its informations and the list of its services will be displayed.

Services
--------

When a host is displayed, you will have the list of services, classified by aggregation. Click on one of them to display them.

If you click on a service, a summary of its status will be displayed on the right.

Actions
-------

You will then be able to perform various actions such as seeing the details of each of its services, acknowledging a problem or planning a downtime for an item (service or host).

You will also have access to the host's history. It may take a while to be available.

Another tab called "Problems" is used to display the problems listed by the backend (like a DOWN host or a CRITICAL service).

Problems
========

Problems tab will display problems found by Alignak-app in backend.
This panel gathers hosts down, critical services or other issues.

  * You'll be able to acknowledge problems or trigger downtimes.
  * You can choose to spy an host from any item.
  * You can display host concerned in Host Synthesis view.

Spied Hosts
===========

This is where you can find the list of hosts that you spy on.

  * You can spy on as many hosts as you want.
  * App will keep you informed about host state.
  * When you select a spy host, App will show you the information it has collected.
  * To stop spying on a host, just double click on it, host will be removed from list.

You can also **drag & drop** spied elements to display host instantly in Host Synthesis.

External Tools
**************

WebUI
=====

App also have lot of buttons which bring you to WebUI. You've to set WebUI url in configuration file to make this buttons available.

App will be aware also on events trigger in WebUI in host history.

GLPI
====

**Not yet implemented.**