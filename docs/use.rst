.. _use:

Alignak-app Interface
=====================

System Tray
-----------

Once Alignak-app is started, you'll have an icon in your task bar (in bottow right under Windows, top right under Ubuntu for example).
When you click on this icon, you'll have access to multiple menu like "dock", "about" or configurations.

App Dock (Right part)
---------------------

When App is launched, the right part (called "dock") will contains different buttons and some container who will receive different notifications.

Alignak part
~~~~~~~~~~~~

This part of dock contains informations about your connection to backend and the states of Alignak daemons.
If you've some connection problems or if backend is restart, you'll see icons change.

You can also see each daemon state by clicking on button with Alignak icon.

Livestate part
~~~~~~~~~~~~~~

In the livestate part, you'll have many buttons who let you see: hosts, user configuration, problems view (available soon) and a button to reach your WebUI if available.

You'll also see a resume of number of problems for hosts and services monitored in your backend.

Events part
~~~~~~~~~~~

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
~~~~~~~~

This is where you can find the list of hosts that you spy on.

  * You can spy on as many hosts as you want.
  * To stop spying on a host, just double click on it, host will be removed from list.

App Panel (Left part)
---------------------

The left part of application (called "Panel"), will display a **Hosts Synthesis View**. This is where you can see your monitored hosts and services.

At the top of this window, you will find a summary of the number of items for each state (OK, CRITICAL, DOWN...).

Start typing the name of a host in the search bar and App will propose to you different corresponding names.
When you select a host, its information and the list of its services will be displayed.

You will then be able to perform various actions such as seeing the details of each of its services, acknowledging a problem or planning a downtime for an item (service or host).

You will also have access to the host's history. It may take a while to be available. It depends on the number of hosts monitored in backend.

Another tab called "Problems" is used to display the problems listed by the backend (like a DOWN host or a CRITICAL service).

WebUI
-----

App also have lot of buttons which bring you to WebUI. You've to set WebUI url in configuration file to make this buttons available.