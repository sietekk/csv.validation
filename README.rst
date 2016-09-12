.. image:: https://travis-ci.org/sietekk/csv.validation.svg?branch=master
    :target: https://travis-ci.org/sietekk/csv.validation
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/sietekk/csv.validation/badge.svg?branch=master
    :target: https://coveralls.io/github/sietekk/csv.validation?branch=master
    :alt: Coverage

.. image:: https://img.shields.io/pypi/v/csv.validation.svg
   :target: https://pypi.python.org/pypi/csv.validation

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/sietekk/csv.validation/master/LICENSE.rst

***********************
CSV Validation Overview
***********************


CSV Validation is a `Python`_ package that provides validation tooling
and processing of CSV files. The initial validation tooling is based on the
fantastic package `Vladiate`_.

.. _`Python`: https://www.python.org
.. _`Vladiate`: https://github.com/di/vladiate

.. contents:: Table of Contents


Example Usage
=============

This packace comes equipped with validation tooling, a logging mechanism, and
loader mechanisms. The validation mechanism is extensible allowing for the
use of custom validation schemas for your implementation. This package
comes with a basic implementation built in as well.


Validation Tooling
******************

This package allows for defining a validation schema to run against a CSV file.
This was implemented due to the severe lack of strict validation mechanisms in
the Python standard library's ``csv`` module. While it does implement the ``csv``
module to some extent, it allows for stricter validation with an extensible
validation mechanism.


Built-In Simple CSV Validator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Included with this package is a simple CSV file validation mechanism to use to
validate simple CSV structures where fields may contain any values or may be
empty. This is also a good example of how to implement a CSV validation schema
in your project.

New Implementations
^^^^^^^^^^^^^^^^^^^

Subclass the ``BaseFileValidator`` class to create a new CSV validation tool. The
required fields ``validators``, ``delimeter``, ``default_validator``,
``check_duplicate_headers``, and ``logger`` attributes must be defined. Creating
a new logger for each CSV validation tool is recommended, but not necessary.

An example bare-bones implementation would be::

    >>> class YourFirstValidatorLogger(Logger):
    >>>     pass
    >>>
    >>> class YourFirstValidator(BaseFileValidator):
    >>>     validators = {
    >>>         "Field1": [],
    >>>         "Field2": [],
    >>>         "Field3": [],
    >>>     }
    >>>     delimiter = ","
    >>>     default_validator = AnyVal
    >>>     check_duplicate_headers = True
    >>>     logger = YourFirstValidatorLogger
    >>>
    >>>     def validate(self):
    >>>         ... validation mechanism here...
    >>>
    >>> validator = YourFirstValidator(LocalFileLoader('/path/to/example.csv'))
    >>> print validator.validate()
    True
    >>> result = validator()
    >>> print result.validation
    True
    >>> print result.log
    ... validation log text...

Obviously, you may call the ``validate`` property directly without a logger, but
you may also call the validator instance, which returns a named tuple ``Result``
with ``validation`` and ``log`` attributes.

Please note, at this time the ``BaseFileValidator`` only supports loggers of the
built-in type. Pull requests and contributions to change this are more than
welcome.

Validator Attribute Definition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``validators`` attribute must define the validation schema for your type of
CSV. It must be a dictionary with string keys defining the available columns and
list values specifying the validator (with any initialization parameters the
validator requires).

An example validation schema would look like::

    >>> validators = {
    >>>     "Foo": [
    >>>         UniqueVal(),
    >>>     ],
    >>>     "Bar": [
    >>>         RegexVal(r'^baz$'),
    >>>     ],
    >>>     "hello world": [
    >>>         IntVal(empty_ok=True),
    >>>     ],
    >>> }

This schema corresponds to a CSV with headers ``Foo``, ``Bar``, and
``hello world``. The ``Foo`` column must contain unique values, the ``Bar``
column must contain fields matching the regular expression ``^baz$``, and the
``hello world`` column must contain integer values, but allows for empty fields
as well.

Built-In Validators
^^^^^^^^^^^^^^^^^^^

This package comes with built-in validators. For example:

- IntVal: Integer values (allows empty values)
- FloatVal: Float values (allows empty values)
- BoolVal: Boolean values (allows empty values)
- EnumVal: Enumerated values::

    EnumVal(['a', 'list', 'of', 'enumerations',])

- UniqueVal: Unique values only
- RegexVal: Fields must match supplied regex value (or no fields are matched)
- EmptyVal: All fields must be empty
- AnyVal: Any allowed values, but not empty

**NOTE:** Inclusion of a JSON validator has not been made at this time, but
pull requests and contributions of an implementation are welcome.


Logging
*******

The logging mechanism is simple, and records logs to an internal dictionary per
instantiation. This allows for easy storage and retrieval of logs and logging
information pertinent to your CSV tool.

One may use the global logging instance ``logger_main``, the logging context
manager ``logger_context``, or subclass the logging implementation ``Logger``
to create custom logging instances.


Loaders
*******

The loader mechanism provides an easy tool to work with files and string objects.
A simple wrapper around a specified ``loader``, working with file-like objects
becomes much simpler when working with CSV data.

A user may work with the ``StringLoader`` or ``LocalFileLoader`` classes by
instantiating them with a source string or directory. For example::

    >>> mystring = StringLoader(StringIO("A test string."))
    >>> teststring = mystring.open()
    >>> print teststring
    "A test string."

To create new loaders, simply subclass the ``Loader`` class, specify a loader
and any ``args`` or ``kwargs`` that are necessary for that loader to operate.


Contributing
============

Contributions and/or fixes to this package are more than welcome. Please submit
them by forking this repository and creating a Pull Request that includes your
changes. We ask that you please include unit tests and any appropriate
documentation updates along with your code changes. Code must be `PEP 8`_
compliant.

This project will adhere to the `Semantic Versioning`_ methodology as much as
possible, so when building dependent projects, please use appropriate version
restrictions.

.. _`Semantic Versioning`: http://semver.org
.. _`PEP 8`: https://www.python.org/dev/peps/pep-0008/

A development environment can be set up to work on this package by doing the
following::

    $ virtualenv csvtools
    $ cd csvtools
    $ . ./bin/activate
    $ git clone https://github.com/sietekk/csv.validation.git
    $ pip install -e ./csv.validation[dev]


License/Copyright
=================

This project is licensed under The MIT License. See the accompanying
``LICENSE.rst`` file for details.

Copyright (c) 2016, Michael Conroy
