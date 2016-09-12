#
# Copyright (c) 2016, Michael Conroy
#


import os
import re


from csv.toolkit.validation import (
    SimpleCSVFileValidator,
    IntVal,
    FloatVal,
    BoolVal,
    EnumVal,
    UniqueVal,
    RegexVal,
    EmptyVal,
    AnyVal,
)
from csv.toolkit.loaders import (
    LocalFileLoader,
)


SIMPLE_CSV_FILE = os.path.join(
    os.path.dirname(__file__),
    'examples/simple.csv'
)
SIMPLE_EMPTY_FIELDS_CSV_FILE = os.path.join(
    os.path.dirname(__file__),
    'examples/simple.empty.fields.csv'
)
BAD_VALIDATION_CSV_FILE = os.path.join(
    os.path.dirname(__file__),
    'examples/simple.bad.validation.csv'
)
EMPTY_OK = {'empty_ok': True}


def clean_string(string):
    return re.sub(r'\n|\n\r', '', re.sub(r'\s', '', string))


def run_assertions(instance, ev, el):
    actual_validation, actual_log = instance()
    assert actual_validation == ev, actual_validation
    assert (clean_string(actual_log) == clean_string(el)), actual_log


def run_header_validation(args, expected_validation, expected_log):
    infile = args[0]
    headers = args[1]
    instance = SimpleCSVFileValidator(LocalFileLoader(infile))
    instance.set_validators(headers)
    run_assertions(instance, expected_validation, expected_log)


def run_validator_validation(args, expected_validation, expected_log):
    infile = args[0]
    validators = args[1]
    instance = SimpleCSVFileValidator(LocalFileLoader(infile))
    instance.validators = validators
    run_assertions(instance, expected_validation, expected_log)


def test_successful_header():
    expected_validation = True
    expected_log = (
        "Validating SimpleCSVFileValidator("
        "source=LocalFileLoader('" + SIMPLE_CSV_FILE + "'))\n"
        "Successful validation"
    )
    headers = [
        'unique',
        'enum',
        'int', 
        'bool', 
        'float', 
        'empty', 
        'any',
        'regex',
    ]
    run_header_validation(
        [SIMPLE_CSV_FILE, headers],
        expected_validation,
        expected_log
    )


def test_missing_header():
    expected_validation = False
    expected_log = (
        "Validating SimpleCSVFileValidator("
        "source=LocalFileLoader('" + SIMPLE_CSV_FILE + "'))"
        "Missing validators for:"
        "  'any': [],"
        "  'bool': [],"
        "  'empty': [],"
        "  'enum': [],"
        "  'float': [],"
        "  'int': [],"
        "  'regex': [],"
        "  'unique': [],"
    )
    run_header_validation(
        [SIMPLE_CSV_FILE, []],
        expected_validation,
        expected_log
    )


def test_extra_header():
    expected_validation = False
    expected_log = (
        "Validating SimpleCSVFileValidator("
        "source=LocalFileLoader('" + SIMPLE_CSV_FILE + "'))\n"
        "Missing expected fields:\n"
        "  'extraheader1': [],\n"
        "  'extraheader2': [],\n"
    )
    headers = [
        'unique',
        'enum',
        'int', 
        'bool', 
        'extraheader1',
        'float', 
        'empty', 
        'any',
        'regex',
        'extraheader2',
    ]
    run_header_validation(
        [SIMPLE_CSV_FILE, headers],
        expected_validation,
        expected_log
    )


def test_successful_validators():
    expected_validation = True
    expected_log = (
        "Validating SimpleCSVFileValidator("
        "source=LocalFileLoader('" + SIMPLE_CSV_FILE + "'))\n"
        "Successful validation"
    )
    validators = {
        'unique': [UniqueVal()],
        'enum': [EnumVal(['WORLD', 'world'])],
        'int': [IntVal()], 
        'bool': [BoolVal()], 
        'float': [FloatVal()], 
        'empty': [EmptyVal()], 
        'any': [AnyVal()],
        'regex': [RegexVal(r'^foobar$')],
    }
    run_validator_validation(
        [SIMPLE_CSV_FILE, validators],
        expected_validation,
        expected_log
    )


def test_failing_validators():
    expected_validation = False
    expected_log = (
        "Validating SimpleCSVFileValidator("
        "source=LocalFileLoader('" + BAD_VALIDATION_CSV_FILE + "'))"
        "Failed validation"
        "Failure on field: \"int\":"
        "  LocalFileLoader('" + BAD_VALIDATION_CSV_FILE + "'):3"
        "    invalid literal for int() with base 10: '3.0'"
        "Failure on field: \"regex\":"
        "  LocalFileLoader('" + BAD_VALIDATION_CSV_FILE + "'):7"
        "    'notfoobar' does not match pattern /^foobar$/"
        "Failure on field: \"unique\":"
        "  LocalFileLoader('" + BAD_VALIDATION_CSV_FILE + "'):1"
        "    'hello0' is already in the column"
        "Failure on field: \"empty\":"
        "  LocalFileLoader('" + BAD_VALIDATION_CSV_FILE + "'):5"
        "    'I'M NOT EMPTY!' is not an empty string"
        "Failure on field: \"enum\":"
        "  LocalFileLoader('" + BAD_VALIDATION_CSV_FILE + "'):2"
        "    'waffles' is not in set(['WORLD', 'world'])"
        "  RegexVal failed 1 time(s) on field: 'regex'"
        "    Invalid fields: ['notfoobar']"
        "  EnumVal failed 1 time(s) on field: 'enum'"
        "    Invalid fields: ['waffles']"
        "  IntVal failed 1 time(s) on field: 'int'"
        "    Invalid fields: ['3.0']"
        "  UniqueVal failed 1 time(s) on field: 'unique'"
        "    Invalid fields: ['('hello0',)']"
        "  EmptyVal failed 1 time(s) on field: 'empty'"
        "    Invalid fields: ['I'M NOT EMPTY!']"
    )
    validators = {
        'unique': [UniqueVal()],
        'enum': [EnumVal(['WORLD', 'world'])],
        'int': [IntVal()], 
        'bool': [BoolVal()], 
        'float': [FloatVal()], 
        'empty': [EmptyVal()], 
        'any': [AnyVal()],
        'regex': [RegexVal(r'^foobar$')],
    }
    run_validator_validation(
        [BAD_VALIDATION_CSV_FILE, validators],
        expected_validation,
        expected_log
    )


def test_failing_non_empty_validators_on_empty_fields():
    expected_validation = False
    expected_log = (
        "Validating SimpleCSVFileValidator("
        "source=LocalFileLoader('" + SIMPLE_EMPTY_FIELDS_CSV_FILE + "'))"
        "Failed validation"
        "Failure on field: \"int\":"
        "  LocalFileLoader('" + SIMPLE_EMPTY_FIELDS_CSV_FILE + "'):1"
        "    invalid literal for int() with base 10: ''"
        "Failure on field: \"regex\":"
        "  LocalFileLoader('" + SIMPLE_EMPTY_FIELDS_CSV_FILE + "'):6"
        "    '' does not match pattern /^foobar$/"
        "Failure on field: \"float\":"
        "  LocalFileLoader('" + SIMPLE_EMPTY_FIELDS_CSV_FILE + "'):3"
        "    could not convert string to float:"
        "Failure on field: \"enum\":"
        "  LocalFileLoader('" + SIMPLE_EMPTY_FIELDS_CSV_FILE + "'):0"
        "    '' is not in set(['WORLD', 'world'])"
        "  RegexVal failed 1 time(s) on field: 'regex'"
        "    Invalid fields: ['']"
        "  FloatVal failed 1 time(s) on field: 'float'"
        "    Invalid fields: ['']"
        "  EnumVal failed 1 time(s) on field: 'enum'"
        "    Invalid fields: ['']"
        "  IntVal failed 1 time(s) on field: 'int'"
        "    Invalid fields: ['']"
    )
    validators = {
        'unique': [UniqueVal()],
        'enum': [EnumVal(['WORLD', 'world'])],
        'int': [IntVal()], 
        'bool': [BoolVal()], 
        'float': [FloatVal()], 
        'empty': [EmptyVal()], 
        'any': [AnyVal()],
        'regex': [RegexVal(r'^foobar$')],
    }
    run_validator_validation(
        [SIMPLE_EMPTY_FIELDS_CSV_FILE, validators],
        expected_validation,
        expected_log
    )


def test_success_empty_fields_validation():
    expected_validation = True
    expected_log = (
        "Validating SimpleCSVFileValidator("
        "source=LocalFileLoader('" + SIMPLE_EMPTY_FIELDS_CSV_FILE + "'))\n"
        "Successful validation"
    )
    validators = {
        'unique': [UniqueVal()],
        'enum': [EnumVal(['WORLD', 'world'], **EMPTY_OK)],
        'int': [IntVal(**EMPTY_OK)], 
        'bool': [BoolVal(**EMPTY_OK)], 
        'float': [FloatVal(**EMPTY_OK)], 
        'empty': [EmptyVal()], 
        'any': [AnyVal()],
        'regex': [RegexVal(r'^foobar$', **EMPTY_OK)],
    }
    run_validator_validation(
        [SIMPLE_EMPTY_FIELDS_CSV_FILE, validators],
        expected_validation,
        expected_log
    )


def test_failing_empty_fields_validation():
    expected_validation = True
    expected_log = (
        "Validating SimpleCSVFileValidator("
        "source=LocalFileLoader('" + SIMPLE_EMPTY_FIELDS_CSV_FILE + "'))\n"
        "Successful validation"
    )
    validators = {
        'unique': [UniqueVal()],
        'enum': [EnumVal(['WORLD', 'world'], **EMPTY_OK)],
        'int': [IntVal(**EMPTY_OK)], 
        'bool': [BoolVal(**EMPTY_OK)], 
        'float': [FloatVal(**EMPTY_OK)], 
        'empty': [EmptyVal()], 
        'any': [AnyVal()],
        'regex': [RegexVal(r'^foobar$', **EMPTY_OK)],
    }
    run_validator_validation(
        [SIMPLE_EMPTY_FIELDS_CSV_FILE, validators],
        expected_validation,
        expected_log
    )
