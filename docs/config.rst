.. _config:

Configuration
#############

Environment Variables
*********************

During installation, Alignak-app creates some folders that contains all the files application need to run.
Then she will keep them in **environment variables**.

The application will normally automatically detect the folders used by the application and use environment variables for this purpose.

  * ``ALIGNAKAPP_USR_DIR``: this folder is used by application for read the ``settings.cfg`` file . By default, Alignak-app will log also in this directory.
  * ``ALIGNAKAPP_APP_DIR``: this folder is used by application for read ``images.ini`` file, ``style.css`` and get images. This variable is normally equal to the ROOT folder described above. **Be careful if you define this variable yourself!**
  * ``ALIGNAKAPP_LOG_DIR``: this folder is used to create the log file of Alignak-app.

During Windows installation, if you used **Installer**, these variables are automatically filled.

On Linux
========

Alignak-app will try to create ``ALIGNAKAPP_USR_DIR`` for later configurations. By default this folder should be::

    /$HOME/.local/alignak_app/

The ``ALIGNAKAPP_APP_DIR`` should be under one of the following folders and is create by pip during installation::

    /$HOME/.local/alignak_app/
    /usr/local/alignak_app/

On Windows
==========

On Windows, use **Installer** is recommended (see :ref:`installer`) to respect Windows conventions.
``ALIGNAKAPP_USR_DIR`` and ``ALIGNAKAPP_APP_DIR`` variables are by default set to::

    C:\Program Files\Alignak-app\

If you install by ``pip`` under Windows, you may need to **define these variables yourself** !
And ``ALIGNAKAPP_USR_DIR`` and ``ALIGNAKAPP_APP_DIR`` variables should be by default set to::

    C:\Users\user\AppData\Roaming\Python\alignak_app\

Settings File
*************

Before running application, **you must configure it**.

You will find a ``settings.cfg`` file located in the ``ALIGNAKAPP_USR_DIR`` folder cited above.

This file contains Sections who are introduced by a ``[section_name]`` header. Then, it contains ``name = value`` entries.
All parameters are also explained in file. For the boolean parameters, you can use the following values: on/off, true/false or 1/0.

The most significant Section is **[Alignak]**. You'll need set your backend url and ports. Otherwise, Alignak-app proposes to define your server Alignak and its port via the window login.

**To Know:** Without connection on Backend of Alignak, App won't start !

Proxy Settings
**************

If you have a proxy on your network, you can set it in ``settings.cfg`` file, as well as the name and password of the proxy.

In case you use the login window, you will have a button dedicated to the proxy settings.

You can also set proxy in environment variables.
`Alignak backend client <http://alignak-backend-client.readthedocs.io/en/develop>`_ will manage these variables alone when connecting to the backend.

* For HTTP proxies, set ``HTTP_PROXY`` variable.
* For HTTPS proxies, set ``HTTPS_PROXY`` variable.

For more informations, please read `Requests documentation <http://docs.python-requests.org/en/latest/user/advanced/#proxies>`_.

Connection to Backend
*********************

Alignak-app have a login form by default, who let you to connect with the username and password define in backend.

You can also set connection information in the ``settings.cfg`` file:

  * **Recommended:** leave empty "username" and "password". Alignak-app will display a login Window.
  * **Recommended:** set your token in "username" field and leave "password" empty (See below).
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

You can also visit: `Alignak-backend : Get Token <http://docs.alignak.net/projects/alignak-backend/en/latest/api.html#get-the-authentication-token>`_

File Example
============

Here is the full ``settings.cfg`` file. This file contains comments for each setting.

    .. literalinclude:: ../etc/settings.cfg