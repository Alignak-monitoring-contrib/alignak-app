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

Alignak-app need at least the backend to connect with it.

System Compatibility
~~~~~~~~~~~~~~~~~~~~

You must have a system compatible with **GTK** to run it !

Python and Libraries
~~~~~~~~~~~~~~~~~~~~

You should have ``python``, ``python-gi`` and ``pip`` installed::

    sudo apt-get update
    sudo apt-get install python python-pip python-gi
    pip install --upgrade pip

Then, simply install Python modules that are listed in ``requirements.txt`` file with pip:

    .. literalinclude:: ../requirements.txt

**Note**: if you proceed to an end-user installation with pip, the required modules are automatically installed.
 
Installation
------------

End user installation
~~~~~~~~~~~~~~~~~~~~~

You can install with pip::

    pip install alignak_app

The required Python modules are automatically installed if not present on your system.

From Sources
~~~~~~~~~~~~

Now you have all requires, clone repos and let's install::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    pip install .


.. _alignak: http://alignak-monitoring.github.io/
.. _alignak-backend: http://alignak-backend.readthedocs.io/en/latest/
.. _alignak-webui: http://alignak-web-ui.readthedocs.io/en/latest/
.. _alignak_backend_client: https://github.com/Alignak-monitoring-contrib/alignak-backend-client
