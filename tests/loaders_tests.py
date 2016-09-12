#
# Copyright (c) 2016, Michael Conroy
#


import os


from six import StringIO, BytesIO, string_types, binary_type
from nose.tools import raises
from csv.toolkit.loaders import (
    Loader,
    StringLoader,
    LocalFileLoader,
    LoaderException,
)


DUMMY_BYTES_SOURCE = os.path.join(
    os.path.dirname(__file__),
    'examples/dummy.pdf'
)
DUMMY_STRING_SOURCE = os.path.join(
    os.path.dirname(__file__),
    'examples/dummy.txt'
)
DUMMY_STRING = "An example string."
DUMMY_SOURCE = StringIO(DUMMY_STRING)


@raises(TypeError)
def test_loader_base_class_empty_init():
    instance = Loader()


def test_loader_base_class_source_init():
    instance = Loader(DUMMY_SOURCE)
    assert isinstance(instance.source, StringIO), type(instance.source)


@raises(NotImplementedError)
def test_loader_base_class_not_implemented():
    instance = Loader(DUMMY_SOURCE)
    instance.open()


def test_loader_base_class_repr():
    instance = Loader(DUMMY_SOURCE)
    expected = "Loader('<type 'instance'>')"
    assert repr(instance) == expected, repr(instance)


@raises(LoaderException)
def test_failing_string_loader_open():
    instance = StringLoader(int)
    print instance.open()


def test_success_string_loader_open_with_plain_string():
    instance = StringLoader(DUMMY_STRING)
    assert isinstance(instance.open(), string_types), type(instance.open())


def test_success_string_loader_open_with_stringio():
    instance = StringLoader(DUMMY_SOURCE)
    assert isinstance(instance.open(), StringIO), instance.open()


def test_string_loader_repr_source_with_name():
    instance = StringLoader(file(DUMMY_BYTES_SOURCE))
    expected = "StringLoader('" + DUMMY_BYTES_SOURCE + "')"
    assert repr(instance) == expected, repr(instance)


def test_string_loader_repr_source_without_name():
    instance = StringLoader(DUMMY_STRING_SOURCE)
    expected = "StringLoader('<type 'str'>')"
    assert repr(instance) == expected, repr(instance)


def test_success_local_file_loader_and_repr():
    instance = LocalFileLoader(DUMMY_BYTES_SOURCE)
    assert isinstance(instance.open(), list), type(instance.open())
    expected = "LocalFileLoader('" + DUMMY_BYTES_SOURCE + "')"
    assert repr(instance) == expected, repr(instance)


@raises(LoaderException)
def test_success_local_file_loader():
    instance = LocalFileLoader(DUMMY_STRING)
    assert isinstance(instance.open(), list), type(instance.open())
