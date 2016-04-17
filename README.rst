===============================
Grapper
===============================


.. image:: https://img.shields.io/travis/strets123/grapper.svg
        :target: https://travis-ci.org/strets123/grapper

.. image:: https://coveralls.io/repos/github/strets123/grapper/badge.svg?branch=master 
        :target: https://coveralls.io/github/strets123/grapper?branch=master

A reference genome re-mapper performing a simplified version of what tools such as `LiftOver <http://genome.ucsc.edu/cgi-bin/hgLiftOver>`_ do.


Features
--------

* Given a file with a JSON list of chomosome alignments and a second file with coordinates for remapping, convert the format of the input coordinates so they map to the target genome.


How to install in a virtualenv
------------------------------

    git clone https://github.com/strets123/grapper

    cd grapper

    python setup.py install

    OR

    pip install git+https://github.com/strets123/grapper#egg=master

Usage
------
 
    grapper.py [-h] alignfile coordsfile output

    
Argument definitions
--------------------

    alignfile   Path to the alignment JSON file

    coordsfile  Path to the coordinates JSON file

    output      Path to the desired output file




Expected file formats are as follows
------------------------------------

alignfile:

    [{ "length": 100, "source": { "chromosome": "1", "start": 100 }, "target": { "chromosome": "2", "start": 

    300 } },{ "length": 200, "source": { "chromosome": "2", "start": 300 }, "target": { "chromosome": "7", "start": 

    20 } }

    ]

coordsfile:


    [{ "chromosome": "1", "position": 150, "reference": "A" },

     { "chromosome": "2", "position": 300, "reference": "C" }

    ]

Design Considerations
---------------------

Requirement was to create an application that would run the required genome remapping and be scalable up to very large file sizes.

In order to do this the ijson library was used for reading the content from the input file. This provides a generator allowing each JSON object to be loaded lazily as required without having to evaluate the whole JSON list into memory.

JSON content is written line by line using a separate process, with communication happening via a multiprocessing queue.

Tests have been added to demonstrate the functionality and specifically to show that chomosomes which have no mapping are ignored, as are chomosomes where the coordinate given is invalid for the length of the chomosome.


Future Work
-----------

A further improvement can be envisioned whereby the reading of the file is done in multiple processes too. This could be done by reading alternate JSON objects in different subprocesses.

It may also be faster


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


* Free software: ISC license
