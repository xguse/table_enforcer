*******
History
*******

v0.4.3 / 2018-02-15
==================

  * Fixed import errors
  * ignore test_chamber

v0.4.2 / 2018-02-15
===================

  * Address import errors when not installed editable
  * update README link to Usage_Demo
  * ship docs/_static/Usage_Demo.html
  * Updated Usage_Demo
  * added to doctrings in main_classes

v0.4.1 / 2018-02-14
===================

  * added readthedocs.yml
  * Updated Usage_Demo and README

v0.4.0 / 2018-02-13
===================

  * Updated tests for CompoundColumn
  * CompoundColumn absorbs MTO/OTM-subclasses
  * updated tests/files/demo_table*.csv
  * updated docs/demo_notebook
  * OTMColumn.input_columns must be len == 1
  * amended tests for new OTMColumn
  * main_classes: rewrite OTMColumn and general reorg
  * BaseColumn method defs now sets api for subclasses
  * Enforcer.columns is now simple list
  * setup.cfg: whitelist varname df
  * main_classes: restruct base classes + ComplexColumn
  * main_classes: col takes table
  * test_column: col takes table
  * add testing files for MTOColumn
  * ignore LibreOffice lock files
  * OTMColumn: improved __doc__
  * update_dataframe: call sig now has `validate`

v0.3.0 / 2018-02-07
===================

  * main_classes: OTMColumn is functional
  * updated testing for OTMColumn
  * main_classes: replace Munch w/ Box (probationary)
  * add python-box to reqs (probationary)
  * conftest: modularize paths
  * add testing for OTMColumn
  * test_column: fix typos and style
  * import all from main_classes
  * Bump version: 0.1.5 → 0.2.0
  * changelog(v0.2.0)
  * Updated Docs version Usage_Demo.ipynb

v0.2.0 / 2018-02-02
===================

  * Enforcer.recode lets Column.recode do the validation now
  * Enforcer.validate no longer recodes
  * Enforcer: make_validations now private
  * Column: added find_failed_rows()
  * columns now take series not dataframe
  * added system-lvl tests based on Usage_Demo.ipynb
  * Enforcer.recode create new df rather than copy
  * added RecoderError and focused ValidationError
  * remove testing for 3.5
  * dont lint tests
  * ignore flake8:W292
  * formatting

v0.1.5 / 2018-02-01
===================

  * Added tests for imports and more Class behavior
  * main_classes: calling recode with validate is now prefered

v0.1.4 / 2018-01-26
===================

  * main_classes.py: removed faulty imports

v0.1.3 / 2018-01-26
===================

  * corrected Usage_Demo.ipynb
  * formatting and typing
  * table_enforcer.py -> main_classes.py

v0.1.2 / 2017-11-17
===================

  * flake8
  * set up basic testing
  * changed travis build settings
  * updated usage demo and readme

v0.1.1 / 2017-11-16
===================

  * Added usage notebook link to docs.
  * reorganized import strategy of Enforcer/Column objs
  * added more builtin validators/recoders/decorators
  * updated reqs
  * initialized travis integration
  * updated docs
  * Added usage demo notebook for docs
  * updated ignore patterns
  * validators.py: renamed

v0.1.0 / 2017-11-15
===================

  * first minimally functional package
  * Enforcer and Column classes defined and operational
  * small cadre of built-in validator functions and decorators
  * ignore jupyter stuff
  * linter setups

v0.0.1 / 2017-11-14
===================

* First commit
