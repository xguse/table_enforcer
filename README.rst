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

.. image:: https://pyup.io/repos/github/xguse/table_enforcer/shield.svg
     :target: https://pyup.io/repos/github/xguse/table_enforcer/
     :alt: Updates


Python package for defining, recoding, and validating table schemas in pandas using a SQLAlchemy-like syntax.


* Free software: MIT license
* Documentation: https://table-enforcer.readthedocs.io.


Features
--------

  * ``Enforcer`` and ``Column`` classes to define what columns should look like in a table.
  * Small but growing cadre of built-in validator functions and decorators.
  * Decorators for use in defining parameterized validators like ``between_4_and_60()``.
  * Declaration syntax for ``Enforcer`` is based on SqlAlchemy's `Table <http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table>`_ pattern.

Credits
---------

This package was created with Cookiecutter_ and the `xguse/cookiecutter-pypackage`_ project template which is based on `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`xguse/cookiecutter-pypackage`: https://github.com/xguse/cookiecutter-pypackage
