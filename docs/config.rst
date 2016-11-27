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

The root folder of the application should be under::

    C:\Users\user\AppData\Roaming\Python\alignak_app\

**Note:** Currently application runs on windows only recently, so launching is not friendly. More pretty version will come soon.

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
  * **notifications:** choose if you want to be notify by popup or not. (boolean)
  * **position:** chosse where the notifications will be displayed.

[Backend] section
-----------------

This section contains parameters to connect to *backend*.

1. **Recommended:** set your token in "username" filed and leave "password" empty. To obtain a token, open a python terminal and type the following commands::

    import requests
    r = requests.post(
        "http://94.76.229.155:6000/login",
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
  * **about:** this image is for about menu.
  * **checked:** this image is for validate button.
  * **exit:** this image is for quit menu.

  * **host_up:** = image for host UP.
  * **host_down:** = image for host DOWN.
  * **host_unreach:** = image for host UNREACHABLE.

  * **service_ok:** = image for service OK.
  * **service_critical:** = image for service CRITICAL.
  * **service_unknown:** = image for service UNKNOWN.
  * **service_warning:** = image for service WARNING.
