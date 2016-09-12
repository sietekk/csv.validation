#
# Copyright (c), 2016, Michael Conroy
#


import os
import re


from nose.tools import assert_raises
from csv.toolkit.validation import (
    BaseFileValidator,
    SimpleCSVFileValidator,
)
from csv.toolkit.loaders import LocalFileLoader


DUMMY_SOURCE = "A dummy source."
EMPTY_CSV = os.path.join(
    os.path.dirname(__file__),
    'examples/empty.csv'
)
DUPLICATE_HEADERS_CSV = os.path.join(
    os.path.dirname(__file__),
    'examples/duplicate.headers.csv'
)


def clean_string(string):
    return re.sub(r'\n|\n\r', '', re.sub(r'\s', '', string))


def test_failure_base_file_validate_validate_not_implemented():
    class BaseFileValidatorTest(BaseFileValidator):
        pass
    BaseFileValidatorTest.validators = {}
    instance = BaseFileValidatorTest(DUMMY_SOURCE)
    assert_raises(NotImplementedError, instance.validate)


def test_simple_csv_validator_empty_csv_no_headers():
    class SimpleCSVFileValidatorTest(SimpleCSVFileValidator):
        pass
    SimpleCSVFileValidatorTest.validators = {}
    instance = SimpleCSVFileValidatorTest(LocalFileLoader(EMPTY_CSV))
    assert instance.validate() == False, instance.validate()
    expected_log = (
        "Validating SimpleCSVFileValidatorTest("
        "source=LocalFileLoader('" + EMPTY_CSV + "'))"
        "Source CSV has no field names"
    )
    assert clean_string(instance.log) == clean_string(expected_log), \
        instance.log

def test_simple_csv_validator_duplicate_headers():
    class SimpleCSVFileValidatorTest(SimpleCSVFileValidator):
        pass
    SimpleCSVFileValidatorTest.validators = {}
    instance = SimpleCSVFileValidatorTest(LocalFileLoader(
                                          DUPLICATE_HEADERS_CSV))
    assert instance.validate() == False, instance.validate()
    expected_log = (
        "Validating SimpleCSVFileValidatorTest("
        "source=LocalFileLoader('" + DUPLICATE_HEADERS_CSV + "'))"
        "Found duplicate column headers:"
        "  Header: header1, columns: 0, 1"
        "Missing validators for:"
        "  'header1': [],"
        "  'header2': [],"
    )
    assert clean_string(instance.log) == clean_string(expected_log), \
        instnace.log
