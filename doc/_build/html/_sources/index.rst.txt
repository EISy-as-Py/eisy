.. eisy documentation master file, created by
   sphinx-quickstart on Thu Mar  5 20:22:20 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


eisy
===================================

:code:`eisy` is a Python module for simulating and classifying impedance data.



Using circuit elements, the simulation module is able to reproduce the impedance response of the selected circuit.
Look into the :code:`circuit.py` page to see which configurations are already supported.
The :code:`data_simulation.py` module allows to simulate the response and saves the result in a :code:`pandas.DataFrame` in the
frequency domain. The impedance response is  presented both in its complex form, as well as separated in its real and imaginary parts.

.. note::
  :code:`eisy` is a new Python model and will be continuously updated as more feature are developed.

For any suggestions or request for specific features, plese visit the `eisy` `issue page <https://github.com/EISy-as-Py/EISy_as_Py/issues.>`_

How to install `eisy`
-----------------------

Add instructions on how to install : conda? or PyPI?

Dependencies
------------

Add list of package dependencies.


Other Section
-------------


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
