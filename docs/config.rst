.. _config:

Before starting
===============

During installation, Alignak-app create the following things:

1. ``/home/$USER/.local/alignak_app``: contains all data files for the application. Like images, logs and configuration file.
2. ``/home/$USER/.local/bin/alignakapp``: this is the script who start Alignak-app.

Configuration Parameters
========================

Before running application, you must configure it. You can configure application in file ``settings.cfg`` located in ``/home/$USER/.local/alignak_app/`` folder.

The two most significant Sections are **[Backend]** and your **[Webui]**.

**Note:** The default configuration file contains some default url for a Alignak server test. 

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

