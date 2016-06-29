.. _install:

Installation
============

Requirements
------------

Alignak Suite
~~~~~~~~~~~~~

You must have Alignak Suite installed before using this app :

* `alignak`_
* `alignak-backend`_
* `alignak-webui`_ 

System Compatibility
~~~~~~~~~~~~~~~~~~~~

Actually, you must have a system compatible with **GTK** to run it !

Python and Libraries
~~~~~~~~~~~~~~~~~~~~

You should have ``python`` and ``pip`` installed::

   sudo apt-get install python python-pip

Then simply install Python modules that are listed in ``requirements.txt`` with pip:

   .. literalinclude:: ../requirements.txt

**Tips:** if you encounter problems with `alignak_backend_client`_, download it, install requirements as above and run ``sudo setup.py install``.

Installation
------------

Actually there is no specific step (and no need) to install this app. So there is no ``setup.py`` file.

.. _alignak: http://alignak-monitoring.github.io/
.. _alignak-backend: http://alignak-backend.readthedocs.io/en/latest/
.. _alignak-webui: http://alignak-web-ui.readthedocs.io/en/latest/
.. _alignak_backend_client: https://github.com/Alignak-monitoring-contrib/alignak-backend-client
