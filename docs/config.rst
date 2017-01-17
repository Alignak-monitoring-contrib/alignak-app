.. _config:

Before starting
===============

During installation, Alignak-app creates a root folder that contains all the files you need: images, logs, and configuration files.

On Linux
--------

The root folder of the application should be under::

    /home/$USER/.local/alignak_app/

On Windows
----------

From Pip or Sources
~~~~~~~~~~~~~~~~~~~

The root folder of the application should be under::

    C:\Users\user\AppData\Roaming\Python\alignak_app\


With installer
~~~~~~~~~~~~~~

If you install app with installer (see :ref:`install`), the configuration file will be located under::

    C:\Program Files\Alignak-app\

The rest of the files is in::

    C:\Users\user\AppData\Roaming\Python\alignak_app\

Configuration Parameters
========================

Before running application, you must configure it. You can do it in file ``settings.cfg`` located in the folder cited above.
This file contains Sections who are introduced by a ``[section_name]`` header. Then, it contains ``name = value`` entries.

The two most significant Sections are **[Backend]** and **[Webui]**. You need to fill in your different url and credentials.

All parameters are also explained in file. For the boolean parameters, you can use the following values: on/off, true/false or 1/0.

[Alignak-App] section
---------------------

This section contains main configuration for *alignak-app*.

  * **check_interval:** defines (in seconds) the frequency of checks to the backend API.
  * **duration:** defines (in seconds) the duration of the notification popup.
  * **position:** choose where the notifications will be displayed.
  * **debug:** set application to debug or not.

[Backend] section
-----------------

This section contains parameters to connect to *backend*. Choose from the following 3 ways to connect:

1. **Recommended:** leave empty "username" and "password". Alignak-app will display a login Window.
2. **Recommended:** set your token in "username" field and leave "password" empty. To obtain a token, open a python terminal and type the following commands::

    import requests
    r = requests.post(
        "http://127.0.0.1:5000/login",
         data={
            'username': 'admin',
            'password': 'admin'
         }
    )
    print(r.text)

2. **Not recommended:** set your "username" and your "password". This method is less secure.

  * **username:** username define in your backend.
  * **password:** password of your backend user.

Then fill your "backend_url":

  * **backend_url:** url of your Backend (IP + port or FQDN if you have it)

If you have installed `Web Service <https://github.com/Alignak-monitoring-contrib/alignak-module-ws>`_ module,
Alignak-app can display daemons status of Alignak.

  * **web_service_status:** = set to yes or no to display it.

Application then need url of your alignak Web Service. If "web_service_status" is set to "no", this settings has no effect.

  * **web_service_url:** = url of your web service.

[Webui] section
---------------

This section contains parameters to reach *webui*.

  * **webui_url:** url of your WebUI (IP + port or FQDN if you have it).

[Config] section
----------------

This section contains application paths. Be **careful** if you change something in this section.

  * **path:** this is the main path of application.
  * **img:** this the images path. This path is relative of the [path] value.
  * **tpl:** this the templates path. This path is relative of the [path] value.

[Images] section
----------------

This section contains images names. You can add your images if you want, but they had to be in [path] + [img] folder.
They are also all in ``.svg`` format and can therefore be easily modified.

  * **icon:** this is the main icon of Alignak-App. It will be displayed in your taskbar.

  * **host_up:** = image for host UP.
  * **host_down:** = image for host DOWN.
  * **host_unreach:** = image for host UNREACHABLE.

  * **service_ok:** = image for service OK.
  * **service_critical:** = image for service CRITICAL.
  * **service_unknown:** = image for service UNKNOWN.
  * **service_warning:** = image for service WARNING.

The other images are used for different application interfaces.