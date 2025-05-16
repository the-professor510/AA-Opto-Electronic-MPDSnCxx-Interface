# AA-Opto-Electronic-MPDSnCxx-Interface
Python package for USB interfacing of the AA Opto-Electronic MPDSnCxx Radio Frequency Driver ([Link](https://aaoptoelectronic.com/mpdsnc-multi-purpose-digital-synthesizers/)). 
This code was developed as part of my PhD in optical chemical profiling through scattering media, to allow for control of AA Opto-Electronic MPDSnCxx radio frequency driver. 
We used the driver to control an AA Opto-Electronic Acousto-Optic Tunable Filter (AOTF).

# Documentation

Full documentation can be found at ...

# Installation

To intsall MPDSnCxx_Interface using pip run:
```
pip install MPDSnCxx_Interface
```

# Usage

To import and initialise use the following code:

```python
import MPDSnCxx_Interface
   
rf_interface = MPDSnCxx_Interface.MPDSnCxx_Interface(vid, pid, serialNum)
rf_interface.connect_device(baudrate, bytesize, parity, stopbits, xonxoff)
```

where vid, pid, and serialNum are the vid, pid, and serial numbers of your MPDSnCxx radio frequency driver. For the AA Opto Electronic MPDSnCxx radio frequency driver the following values must selected:

* baudrate = 57600 bauds
* bytesize = 8 bits
* partiy = None
* stopbits = 1 stop bit
* xonxoff = False

At the end of the program it is good practices to close the connection, to do this use:

```python
rf_interface.disconnect_device()
```
