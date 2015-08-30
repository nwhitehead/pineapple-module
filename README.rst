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
magic functions ``%pip`` and ``%require``.

::

    import pineapple
    
    %pip install numpy
    
    %pip list
    
    %require numpy==1.9.2
    
    %require numpy==1.9.2 ipython==4.0.0
    
    %require
