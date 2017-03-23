.. _config:

Alignak-app Main Folder
=======================

During installation, Alignak-app creates a root folder that contains all the files application need to run.

On Linux
--------

The ROOT folder of the application should be under::

    /home/$USER/.local/alignak_app/

On Windows
----------

1. If you install from **Pip** or with **Sources**:

The ROOT folder of the application should be under::

    C:\Users\user\AppData\Roaming\Python\alignak_app\


2. If you use **Installer** (see :ref:`install`):

The ROOT folder will be located under::

    C:\Program Files\Alignak-app\

This is to facilitate access to the configuration and respect Windows conventions.

Alignak-app Workdir
===================

This folder is defined by the ``app_workdir.ini`` file located in the main application folder cited above.

The goal of this file is to define a directory where Alignak-app can write/read without problems to get settings and create log files.
So make sure that you have the right to write and read.

You must set an **absolute path** for this settings.

Then only put/copy the ``settings.cfg``, located in application main folder, inside the one you have defined.

**Note:** If you have not set this option, application use the same directory than cited above. If you have no rights, application will crash.

Configuration Parameters
========================

Before running application, **you must configure it**.

You will find a file named ``settings.cfg`` located in the "ROOT" folder cited above.
Otherwise, Alignak-app proposes to define your server Alignak and its port via the window login.

This file contains Sections who are introduced by a ``[section_name]`` header. Then, it contains ``name = value`` entries.
All parameters are also explained in file. For the boolean parameters, you can use the following values: on/off, true/false or 1/0.

The most significant Section is **[Backend]**. You need set your backend url, ports and credentials.

.. [ToKnow] " Without connection on Backend of Alignak, App won't start ! "

[Alignak-App] section
---------------------

This section contains main configuration for *alignak-app*.

  * **synthesis_interval:** defines (in seconds) the frequency of checks to the backend API *livesynthesis*.
  * **daemon_interval:** defines (in seconds) the frequency of checks to the backend API *alignakdaemon*.
  * **item_interval:** defines (in seconds) the frequency of checks to the backend API for other checks.

[Dashboard] section
-------------------

This section contains configuration of Dashboard application.

  * **position:** define default position of dashboard.
  * **pop:** define if you want the dashboard "pop" at each backend changes or not.
  * **duration:** define how long the dashboard is displayed if *pop* mode is set to *yes*
  * **sticky:** define if the dashboard can be move or not.

[Banners] section
-----------------

This section contains configuration of banners.

  * **title:** choose to display banner title or not, if the colors are not enough.
  * **changes:** display banners at each backend changes or not.
  * **duration:** set the time (in seconds) before a banner that indicates changes will close.
  * **animation:** define speed of animation. Must be equal or greater than 0 !

[Alignak] section
-----------------

This section contains parameters to interact with Alignak.

For "username" and "password", choose from the following 3 ways to connect:

  * **Recommended:** leave empty "username" and "password". Alignak-app will display a login Window.
  * **Recommended:** set your token in "username" field and leave "password" empty.
  * **Not recommended:** set your "username" and your "password". This method is less secure.

To obtain a token, open a python terminal and type the following commands::

    import requests
    backend_url = 'http://alignak.com:5000'
    r = requests.post(
        backend_url + '/login',
         data={
            'username': 'admin',
            'password': 'admin'
         }
    )
    print(r.text)

Then:

  * **url:** url of Alignak, without port. (IP or FQDN if you have it). You can call this option after with ``%(alignak_url)s`` syntax, but **only in this section !**
  * **backend:** your backend url. Default is: ``%(alignak_url)s:5000`` but you can also put the IP or FQDN.
  * **webui:** url of your WebUI. Default is: ``%(alignak_url)s:80`` but you can also put the IP or FQDN.
  * **processes:** number of processes used for backend connection

[Log] section
-------------

This section contains log system of application.

  * **filename:** define name of file where logs will be stored
  * **location:** set this setting if you want to store your logs somewhere else
  * **debug:** activate the debug mode of application

[Config] section
----------------

This section contains application paths. Be **careful** if you modify something in this section.

  * **path:** this is the main path of application.
  * **img:** this the images path. This path is relative of the [path] value.

[Images] section
----------------

This section contains images names. You can add your own images if you want, but they had to be in *images* application folder.
They are also all in ``.svg`` format (except alignak logo) and can therefore be easily modified.
