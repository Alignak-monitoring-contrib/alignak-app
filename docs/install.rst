.. _install:

Install Alignak-app
===================

Requirements
------------

Alignak Suite
~~~~~~~~~~~~~

You must have Alignak Suite installed before using this app :

* `alignak`_
* `alignak-backend`_
* `alignak-webui`_ 

Alignak-app need at least a functionnal **alignak-backend** to connect with it.

Python and PyQT
~~~~~~~~~~~~~~~

You must install a version of **PyQt**, compatible with your python version.

**Note:** For **Windows** users, PyQt5 and Python3 are more easy to install.

Generally, here's how to install PyQt:

Python2
*******

On Linux::

    sudo apt-get install python-qt4

On Windows:

* Download the correct executable on `PyQt4 Official Website`_.
* Be sure to have **the same architecture** as your **Python version** (`x86` or `x64`).
* Then simply run installer.

Python3
*******

On Linux and Windows::

    pip install PyQt5 --user

Python and Libraries
~~~~~~~~~~~~~~~~~~~~

Then, simply install Python modules that are listed in ``requirements.txt`` file with pip:

    .. literalinclude:: ../requirements.txt

**Note**: if you proceed to an end-user installation with pip, the required modules are automatically installed.

Installation
------------

**Note:** Be sure to install this application with ``--user`` flags. Otherwise you may not be able to launch it !

End user installation
~~~~~~~~~~~~~~~~~~~~~

You can install with pip::

    pip install alignak_app --user

The required Python modules are automatically installed if not present on your system.
Obviously, you should use ``pip3`` to install for Python 3.

From Sources
~~~~~~~~~~~~

To install from source, clone repos and install with pip ::

    git clone https://github.com/Alignak-monitoring-contrib/alignak-app
    cd alignak-app
    pip install . --user

.. _alignak: http://alignak-monitoring.github.io/
.. _alignak-backend: http://alignak-backend.readthedocs.io/en/latest/
.. _alignak-webui: http://alignak-web-ui.readthedocs.io/en/latest/
.. _alignak_backend_client: https://github.com/Alignak-monitoring-contrib/alignak-backend-client
.. _PyQt4 Official Website: https://www.riverbankcomputing.com/software/pyqt/download
.. _PyQt4 Official Tutorial: http://pyqt.sourceforge.net/Docs/PyQt4/installation.html
