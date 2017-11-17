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

Have a look at this `Demo Notebook <https://nbviewer.jupyter.org/github/xguse/table_enforcer/blob/master/docs/demo_notebook/Usage_Demo.ipynb>`_

Description
-----------

A python package to facilitate the iterative process of developing and using schema-like representations of DataFrames in pandas for recoding and validating instances of these data.

This is a very young attempt at solving a recurrent problem many people have.  So far I have looked at multiple solutions, but none really did it for me.

I need to load, recode, and validate tables all day everyday. Sometimes its simple; you can ``pandas.read_table()`` and all is good. But sometimes you have a 400 column long RedCap data dump that is complicated `af` and you need to develop your recoding logic through an iterative process.

This is an attempt to apply a sort of "test driven development" approach to data cleaning.


Basic Workflow
--------------

#. For each column that you care about in your source table:

        #. Define a ``Column`` object that represents the ideal state of your data by passing a list of small, independent, reusable validator functions and some descriptive information.

        #. Use this object to validate the column data from your source table.

                * It WILL fail.

        #. Add small, composable, reusable recoding functions to the column object and iterate until your validations pass.

#. Define an ``Enforcer`` object by passing it a list of your column representation objects.

#. This enforcer can be used to recode or validate recoded tables of the same kind as your source table wherever your applications use that type of data.


.. note:: Soon, I want to add more kinds of ``Column`` objects that implement one-to-many and many-to-one recoding logic as sometimes a column tries to do too much and should really be multiple columns as well as the reverse.


Please take a look and offer thoughts/advice.

* Free software: MIT license
* Web site: https://github.com/xguse/table_enforcer
* Documentation: https://table-enforcer.readthedocs.io.


Features
--------

  * ``Enforcer`` and ``Column`` classes to define what columns should look like in a table.
  * Small but growing cadre of built-in validator functions and decorators.
  * Decorators for use in defining parameterized validators like ``between_4_and_60()``.
  * Declaration syntax for ``Enforcer`` is loosely based on SqlAlchemy's `Table <http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table>`_ pattern.



Credits
---------

This package was created with Cookiecutter_ and the `xguse/cookiecutter-pypackage`_ project template which is based on `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`xguse/cookiecutter-pypackage`: https://github.com/xguse/cookiecutter-pypackage
