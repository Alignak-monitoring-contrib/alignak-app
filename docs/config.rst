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

Then only put/copy the ``settings.cfg`` in the folder you have defined.

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

Settings file
-------------

Here is the full ``settings.cfg`` file. This file contains comments for each setting.

    .. literalinclude:: ../etc/settings.cfg

Connection to Backend
---------------------

Alignak-app have a login form by default, who let you to connect with the username and password define in backend.

You can also set connection information in settings file:

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

