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

The most significant Section is **[Backend]**. You need to fill in your different url and credentials.

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

This section contains parameters to connect to *backend*.

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

Then fill your "alignak_url":

  * **alignak_url:** url of your Backend, without port. (IP or FQDN if you have it)

You can call this option after with ``%(alignak_url)s`` syntax, but **only in this section !**

Your "alignak_backend" url:

  * **alignak_backend:** your backend url. Default is: ``%(alignak_url)s:5000`` but you can also put the IP or FQDN.

And the "alignak_webui" url.

  * **alignak_webui:** url of your WebUI. Default is: ``%(alignak_url)s`` but you can also put the IP or else.

If you have a port other than port 80 for your WebUI, do not forget to add it (e.g.: ``%(alignak_url)s:5001``).

If you have installed `Web Service <https://github.com/Alignak-monitoring-contrib/alignak-module-ws>`_ module,
Alignak-app can display daemons status of Alignak.

  * **web_service:** active or not the web-service in Alignak-app. Set to `yes` or `no` to display it.

Application then need url of your alignak Web Service. If "web_service_status" is set to "no", this settings has no effect.

  * **alignak_ws:** = url of your web service. Default is: ``%(alignak_url)s:8888`` but you can also put the IP or FQDN.

[Config] section
----------------

This section contains application paths. Be **careful** if you modify something in this section.

  * **path:** this is the main path of application.
  * **img:** this the images path. This path is relative of the [path] value.
  * **tpl:** this the templates path. This path is relative of the [path] value.

[Images] section
----------------

This section contains images names. You can add your own images if you want, but they had to be in [path] + [img] folder.
They are also all in ``.svg`` format and can therefore be easily modified.
