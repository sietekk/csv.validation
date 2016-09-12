#
# Copyright (c) 2016, Michael Conroy
#


from nose.tools import raises
from csv.toolkit.validation import (
    BaseValidator,
    BaseTypeValidator,
    IntVal,
    FloatVal,
    BoolVal,
    EnumVal,
    UniqueVal,
    RegexVal,
    EmptyVal,
    AnyVal,
    ValidationConfigurationException,
)


@raises(NotImplementedError)
def test_base_validator_validate_notimplemented():
    instance = BaseValidator()
    instance.validate('dummyarg1', 'dummyarg2'),


@raises(NotImplementedError)
def test_base_validator_fails_notimplemented():
    instance = BaseValidator()
    instance.fails()

@raises(ValidationConfigurationException)
def test_unique_val_validation_configuration_exception():
    instance = UniqueVal(['value1', 'value2',])
    validation_args = {'field': 'value1', 'row': {'value1': "",}}
    instance.validate(**validation_args)
