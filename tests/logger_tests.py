#
# Copyright (c) 2016, Michael Conroy
#


import os


from nose.tools import assert_raises
from six import StringIO, BytesIO, string_types
from csv.toolkit.logger import (
    SimpleLogger,
    logger_context,
    logger_main,
)


DUMMY_TEXT_FILE = os.path.join(
    os.path.dirname(__file__), 'examples/dummy.txt'
)
DUMMY_PDF_FILE = os.path.join(
    os.path.dirname(__file__), 'examples/dummy.pdf'
)
LOGGER_SUCCESSES = [
    "Log this text!",
    open(DUMMY_TEXT_FILE, 'r').read(),
    StringIO(DUMMY_TEXT_FILE).read(),
]
LOGGER_FAILURES = [
    {'log': "can't process dict type"},
    set(["can't", "process", "set", "type"]),
    ["can't", "process", "list", "type"],
    1,
    1.0,
    True,
    False,
    open(DUMMY_TEXT_FILE, 'r'),
    open(DUMMY_PDF_FILE, 'r').read(),
    StringIO(DUMMY_TEXT_FILE),
    BytesIO(DUMMY_TEXT_FILE)
]


def success_logger_cleared(logger):
    logger.clear()
    
    check1 = logger.check()
    assert check1 == False

    output = logger.logs
    assert isinstance(output, string_types), type(output)
    assert len(output) == 0


def success_logger(inlog, logger):
    check1 = logger.check()
    assert check1 == False

    logger.log(inlog)

    check2 = logger.check()
    assert check2 == True

    output = logger.logs
    assert isinstance(output, string_types), type(output)
    assert len(output) > 0

    success_logger_cleared(logger)


def failure_logger(inlog, logger):
    assert_raises(
        ValueError,
        logger.log(inlog),
        'Loggable objects must be of type string'
    )


def logger_successes(logger):
    for log in LOGGER_SUCCESSES:
        yield success_logger, logger

def logger_failures(logger):
    for log in LOGGER_FAILURES:
        yield failure_logger, logger

def test_logger():
    logger1 = SimpleLogger()
    logger_successes(logger1)

    logger_successes(logger_main)

    with logger_context() as logger2:
        logger_successes(logger2)
        success_logger_cleared(logger2)

    logger3 = SimpleLogger()
    logger_failures(logger3)

    logger_failures(logger_main)

    with logger_context() as logger4:
        logger_failures(logger2)
