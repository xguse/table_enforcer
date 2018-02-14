==============
Table Enforcer
==============


.. image:: https://img.shields.io/pypi/v/table_enforcer.svg
        :target: https://pypi.python.org/pypi/table_enforcer

.. image:: https://img.shields.io/travis/xguse/table_enforcer.svg
        :target: https://travis-ci.org/xguse/table_enforcer

.. image:: https://readthedocs.org/projects/table-enforcer/badge/?version=latest
        :target: https://table-enforcer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

..        .. image:: https://pyup.io/repos/github/xguse/table_enforcer/shield.svg
        :target: https://pyup.io/repos/github/xguse/table_enforcer/
        :alt: Updates

Demo Usage
----------

Have a look at this `Demo Notebook <http://table-enforcer.readthedocs.io/en/latest/_static/Usage_Demo.html>`_

Description
-----------

A python package to facilitate the iterative process of developing and using schema-like representations of table data to recode and validate instances of these data stored in pandas DataFrames.
This is a `fairly young` attempt to solve a recurrent problem many people have.
So far I have looked at multiple solutions, but none really did it for me.

They either deal primarily with JSON encoded data or they only really solve the validation side of the problem and consider recoding to be a separate issue.
They seem to assume that recoding and cleaning has already been done and all we care about is making sure the final product is sane.

To me, this seems backwards.

I need to load, recode, and validate tables all day, everyday.
Sometimes its simple; I can ``pandas.read_table()`` and all is good.
But sometimes I have a 700 column long RedCap data dump that is complicated af, and it `really` helps me to develop my recoding logic through an iterative process.
For me it makes sense to couple the recoding process directly with the validation process:
to write the "tests" for each column first, then add recoding logic in steps until the tests pass.

So `Table Enforcer` is my attempt to apply a sort of "test driven development" workflow to data cleaning and validation.


Basic Workflow
--------------

#. For each column that you care about in your source table:

   #. Define a ``Column`` object that represents the ideal state of your data by passing a list of small, independent, reusable validator functions and some descriptive information.

   #. Use this object to validate the column data from your source table.

      * It will probably fail.

   #. Add small, composable, reusable recoding functions to the column object and iterate until your validations pass.

#. Define an ``Enforcer`` object by passing it a list of your column representation objects.

#. This enforcer can be used to recode or validate recoded tables of the same kind as your source table wherever your applications use that type of data.



Please take a look and offer thoughts/advice.

* Free software: MIT license
* Web site: https://github.com/xguse/table_enforcer
* Documentation: https://table-enforcer.readthedocs.io.


Features
--------

* ``Enforcer`` and ``Column`` classes to define what columns should look like in a table.
* ``CompundColumn`` class that supports complex operations including "one-to-many" and "many-to-one" recoding logic as sometimes a column tries to do too much and should really be multiple columns as well as the reverse.
* Growing cadre of built-in validator functions and decorators.
* Decorators for use in defining parameterized validators like ``between_4_and_60()``.



Credits
---------

This package was created with Cookiecutter_ and the `xguse/cookiecutter-pypackage`_ project template which is based on `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`xguse/cookiecutter-pypackage`: https://github.com/xguse/cookiecutter-pypackage
