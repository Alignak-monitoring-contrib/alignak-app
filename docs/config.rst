.. _config:

Before starting
===============

During installation, Alignak-app create a folder who contains all data files for the application (Like images, logs and configuration file).

On Linux
--------

The root folder of the application should be under::

``/home/$USER/.local/alignak_app``:

On Windows
----------

The root folder of the application should be under::

    C:\Users\user\AppData\Roaming\Python\alignak_app\

**Note:** Currently application runs on windows only recently, so launching is not easy. More pretty version will come soon.

Configuration Parameters
========================

Before running application, you must configure it. You can do it in file ``settings.cfg`` located in the folder cited above.

The two most significant Sections are **[Backend]** and your **[Webui]**.

All parameters are explained in file, you only have to read each section.

[Alignak-App] section
---------------------

This section contains main configuration for *alignak-app*. 

[Backend] section
-----------------

This section contains parameters to connect to *backend*.

[Webui] section
---------------

This section contains parameters to reach *webui*.

[Config] section
----------------

This section contains path to application and images. Be **careful** if you change something in it.

