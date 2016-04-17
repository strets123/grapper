===============================
Grapper
===============================

.. image:: https://img.shields.io/pypi/v/grapper.svg
        :target: https://pypi.python.org/pypi/grapper

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

   grapper.py [-h] alignfile coordsfile output

    positional arguments:
        alignfile   Path to the alignment JSON file
        coordsfile  Path to the coordinates JSON file
        output      Path to the desired output file



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
