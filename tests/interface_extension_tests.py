#
# Copyright (c) 2016, Michael Conroy
#


import argparse


from nose.tools import assert_raises, raises
from csv.toolkit.interface import (
    Extension,
    Tool,
)
from csv.toolkit.validation import SimpleCSVValidationTool


ARGUMENTS = [
    (
        'filename',
        {'type': argparse.FileType('r')},
        {'help': 'The file containing the structure to validate.'},
    ),
    (
        '--headers',
        {'nargs': '+'},
        {'help': 'A list detailing the expected headers'},
    ),
]
INVALID_ARGUMENT = [([1, 2, 3,], ["invalid", "list", "argument",], )]


def test_extension():
    instance = Extension()
    assert instance.enabled() == False, instance.enabled()
    assert isinstance(instance.all(), list), type(instance.all())
    assert isinstance(instance.all()[0], type(SimpleCSVValidationTool))
    assert_raises(NotImplementedError, instance.signature)
    assert isinstance(instance.mapped(), dict), type(instance.mapped())
    assert isinstance(
        instance.mapped()['simple-validator'], type(SimpleCSVValidationTool)
    ), type(instance.mapped()['simple-validator'])


def test_interface_without_self_arguments():
    instance = Tool(*ARGUMENTS)
    assert instance.name == NotImplemented, instance.name
    assert instance.arguments == None, instance.arguments
    assert instance.description == None, instance.description


def test_interface_with_self_arguments():
    class ToolTest(Tool):
        pass
    ToolTest.arguments = ARGUMENTS
    instance = ToolTest(*ARGUMENTS)


@raises(TypeError)
def test_failure_interface_with_invalid_argument_config():
    class ToolTest2(Tool):
        pass
    ToolTest2.arguments = INVALID_ARGUMENT
    instance = ToolTest2()


def test_failure_interface_call():
    instance = Tool()
    assert_raises(NotImplementedError, instance)
