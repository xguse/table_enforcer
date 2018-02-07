*******
History
*******

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
