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


Running the tests
-----------------

    See `Contributing <https://github.com/strets123/grapper/blob/master/CONTRIBUTING.rst>`_


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

Given that the only explicitely permitted assumption was that genome fragments do not overlap, I have assumed that chromosomes can be split into multiple fragments and tested for this case.


Discussion
-----------

A further improvement can be envisioned whereby the reading of the file is done in multiple processes too. This could be done by splitting up the chromosomes between different procesesses

Furthermore, we currently work with the whole of the required data from the alignment file in memory. Memory consumption has been reduced slightly by using a list of tuples rather than dictionaries. Clearly if the alignment file is truly as big as the coordinates file a different approach may be needed.

Currently we use a bisect_left function to find the nearest start point in the alignment file to the positions in the coordinate file. It might be possible instead to use a mergesort where both datasets are held in memory and are read side by side.

Errors
------

There is currently an error if running tox locally if the coveralls repo key environment variable is not set but this does not affect running the tests.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


* Free software: ISC license
