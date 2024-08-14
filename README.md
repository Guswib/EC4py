The intenetion
---------------
This is a package to treat electrochemical data in order to extract key values such as ECSA and Tafel slopes. Specifically, its aim is to make the data analysis as quick and easy as possible. 

A simple example
---------------
.. code:: python
    
    from EC4py import EC_Data

    data = EC_Data("FILE PATH")
    data.plot("E","i")

Features
--------

* Read TDMS files.
    ** Plot

* Treats cyclic voltammetry data:
    ** subtraction, addition
    ** back ground subtraction 
    ** Levich analysis
    ** Cout

