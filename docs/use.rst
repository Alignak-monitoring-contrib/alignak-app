.. _use:

Alignak-app Interface
=====================

System Tray
-----------

Once Alignak-app is started, you'll have an icon in your task bar (in bottow right under Windows, top right under Ubuntu for example).
When you click on this icon, you'll have access to multiple menu like "dock", "about" or configurations.

App Dock
--------

When App is launched, a "dock" will also appear right of your screen.
This "dock" will contains different buttons and some container who will receive different notifications.

Alignak part
~~~~~~~~~~~~

This part of dock contains informations about your connection to backend and the states of Alignak daemons.
If you've some connection problems or if backend is restart, you'll see icons change.

Livestate part
~~~~~~~~~~~~~~

In the livestate part, you'll have many buttons whi let you see: hosts, your user configuration, problems view (available soon) and a button to reach your WebUI if available.

You'll also see a resume of number of problems for hosts and services monitored in your backend.

Events part
~~~~~~~~~~~

This is one of the most interesting features of the application. You'll receive many informations in this part like alignak notifications, actions informations (like acknowledge or modifications you do in App).
You will also be able to drag and drop a notification from a host in the container below (Spy Hosts). Then App will send you regular notifications about that host.

Some notifications will be temporary but some others not. If you want to remove an event, simply double click on it.

Spy part
~~~~~~~~

This is where you can find the list of hosts that you spy on. You can spy on as many hosts as you want.
To stop spying on a host, just double click on it.

App Panel
---------

When you click on **host** button in dock, a new window will appear, called **Hosts Synthesis View**. This where you can see your monitored hosts and services.

At the top of this window, you will find a summary of the number of items for each state (OK, CRITICAL, DOWN...).

Start typing the name of a host in the search bar and App will propose to you different corresponding names.
When you select a host, its information and the list of its services will be displayed.

You will then be able to perform various actions such as seeing the details of each of its services, acknowledging a problem or planning a downtime for an item (service or host).

You will also have access to the host's history. It may take a while to be available. It depends on the number of hosts monitored in backend.