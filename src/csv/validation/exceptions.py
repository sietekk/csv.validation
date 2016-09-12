#
# Copyright (c) 2016, Michael Conroy
#


__all__ = (
    'ValidationException',
    'ValidationConfigurationException',
    'LoaderException',
)


class ValidationException(Exception):
    """ Base validation exception """

    pass


class ValidationConfigurationException(ValidationException):
    """ Exception for poorly configured validator configuration """

    pass


class LoaderException(ValidationException):
    """ Thrown when a file loader fails """

    pass
