pineapple-module
----------------

This project is a Python module that defines some utility
functions for the Pineapple IPython/Jupyter front-end.

The goal is to standardize notebooks so that notebook authors
can have a consistent and easy way for readers to reproduce their
exact results with the least amount of hassle.

Usage
~~~~~

After importing the module, within IPython notebooks you get
magic functions ``%pip``, ``%require``, and ``%runtest``.

The ``%pip`` command lets you easily use the ``pip`` command
directly to manage installed packages.

The ``%require`` command shows all installed packages with versions
if called with no arguments. If called with arguments, it will attempt
to install the requested packages. Arguments are version specifiers,
separated by spaces.

The ``%runtest`` command takes any number of test case or test suite
classes descended from ``unittest.TestCase`` or ``unittest.TestSuite``
and runs them in the cell. It should also be compatible with ``unittest2``.

::

    import pineapple
    
    %pip install numpy
    
    %pip list
    
    %require numpy==1.9.2
    
    %require numpy==1.9.2 ipython==4.0.0
    
    %require

    %runtest MyTesterClass
