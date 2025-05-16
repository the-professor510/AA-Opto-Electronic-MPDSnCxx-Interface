Installation
============

To install MPDSnCxx_Interface using pip run:

.. code-block:: console

   (.env) $ pip install MPDSnCxx_Interface


Or the source code can be found at `<https://github.com/the-professor510/AA-Opto-Electronic-MPDSnCxx-Interface>`_.


Usage
=====

To import and initialise use the following code:

.. code-block:: python

   import MPDSnCxx_Interface
   
   rf_interface = MPDSnCxx_Interface.MPDSnCxx_Interface(vid, pid, serialNum)
   rf_interface.connect_device(baudrate, bytesize, parity, stopbits, xonxoff)

where vid, pid, and serialNum are the vid, pid, and serial numbers of your MPDSnCxx radio frequency driver. For the AA Opto Electronic MPDSnCxx radio frequency driver the following values must selected:

* baudrate = 57600 bauds
* bytesize = 8 bits
* partiy = None
* stopbits = 1 stop bit
* xonxoff = False

Check out :py:func:`MPDSnCxx_Interface.connect_device()` for full information on the allowed values when initialising

At the end of the program it is good practices to close the connection, to do this use:

.. code-block:: python
   
   rf_interface.disconnect_device()

