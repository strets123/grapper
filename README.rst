===============================
Grapper
===============================


.. image:: https://img.shields.io/travis/strets123/grapper.svg
        :target: https://travis-ci.org/strets123/grapper

.. image:: https://readthedocs.org/projects/grapper/badge/?version=latest
        :target: https://readthedocs.org/projects/grapper/?badge=latest
        :alt: Documentation Status


A simple reference genome re-mapper

* Free software: ISC license
* Documentation: https://grapper.readthedocs.org.

Features
--------

* Given a file with a JSON list of chomosome alignments and a second file with coordinates for remapping, write an output file



* Usage:

.. code-block:: bash
   grapper.py [-h] alignfile coordsfile output

.. code-block:: none
    positional arguments:
        
    alignfile   Path to the alignment JSON file
    coordsfile  Path to the coordinates JSON file
    output      Path to the desired output file

* How to install and run with test data:

    


* Expected file formats are as follows:

alignfile:

    [{ "length": 100, "source": { "chromosome": "1", "start": 100 }, "target": { "chromosome": "2", "start": 

    300 } },{ "length": 200, "source": { "chromosome": "2", "start": 300 }, "target": { "chromosome": "7", "start": 

    20 } }

    ]

coordsfile:


    [{ "chromosome": "1", "position": 150, "reference": "A" },

     { "chromosome": "2", "position": 300, "reference": "C" }

    ]

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
