#!/usr/bin/env python
# encoding: utf-8
# Copyright 2018, The RouterSploit Framework (RSF) by Threat9 All rights reserved.
import re
import os.path
from core.Exceptions import OptionValidationError
from core.Utils import is_ipv4, is_ipv6


class Option(object):
    """ Exploit attribute that is set by the end user """
    def __init__(self, default, description=""):
        self.label = None
        self.description = description
        if default:
            self.__set__("", default)
        else:
            self.display_value = ""
            self.value = ""

    def __get__(self, instance, owner):
        return self.value


class IPOption(Option):
    """ Option ip attribute """
    def __set__(self, instance, value):
        if not value or is_ipv4(value) or is_ipv6(value):
            self.value = self.display_value = value
        else:
            raise OptionValidationError("Invalid address, Provide access is not valid IPv4 or IPv6 address.")


class PortOption(Option):
    """ Option port attribute """
    def __set__(self, instance, value):
        try:
            value = int(value)
            if 0 < value <= 65535:
                self.display_value = str(value)
                self.value = value
            else:
                raise OptionValidationError("Invalid option, port value should be between 0 and 65536.")
        except ValueError:
            raise OptionValidationError("Invalid option, Cannot cast '{}' to integer.".format(value))


class BoolOption(Option):
    """ Option bool attribute """
    def __init__(self, default, description=""):
        super(BoolOption, self).__init__(default=default, description=description)
        if default:
            self.display_value = "true"
        else:
            self.display_value = "false"
        self.value = default

    def __set__(self, instance, value):
        if value == "true":
            self.value = True
            self.display_value = value
        elif value == "false":
            self.value = False
            self.display_value = value
        else:
            raise OptionValidationError("Invalid value, it should be true or false")


class IntegerOption(Option):
    """ Option int attribute """
    def __set__(self, instance, value):
        try:
            self.display_value = str(value)
            self.value = int(value)
        except ValueError:
            raise OptionValidationError("Invalid value, Cannot cast '{}' to integer".format(value))


class FloatOption(Option):
    """ Option float attribute """
    def __set__(self, instance, value):
        try:
            self.display_value = str(value)
            self.value = float(value)
        except ValueError:
            raise OptionValidationError("Invalid value, Cannot cast '{}' to integer".format(value))


class StringOption(Option):
    """ Option string attribute """
    def __set__(self, instance, value):
        try:
            self.display_value = self.value = str(value)
        except ValueError:
            raise OptionValidationError("Invalid value, Cannot cast '{}' to integer".format(value))


class MACOption(Option):
    """ Option MAC attribute """
    def __set__(self, instance, value):
        regexp = r"^[a-f\d]{1,2}:[a-f\d]{1,2}:[a-f\d]{1,2}:[a-f\d]{1,2}:[a-f\d]{1,2}:[a-f\d]{1,2}$"
        if re.match(regexp, value.lower()):
            self.value = self.display_value = value
        else:
            raise OptionValidationError("Invalid option. '{}' is not a valid MAC address".format(value))


class WordDictionaryOption(Option):
    """ Option dictionary attribute """
    def __get__(self, instance, owner):
        if self.display_value.startswith("file://"):
            path = self.display_value.replace("file://", "")
            with open(path, "r") as f:
                lines = [line.strip() for line in f.readlines()]
                return lines
        return self.display_value.split(",")

    def __set__(self, instance, value):
        if value.startswith("file://"):
            path = value.replace("file://", "")
            if not os.path.exists(path):
                raise OptionValidationError("File '{}' does not exist.".format(path))
        self.value = self.display_value = value


class EncoderOption(Option):
    """ Option encoder attribute """
    def __init__(self, default, description):
        super(EncoderOption, self).__init__(default=default, description=description)
        if default:
            self.display_value = default
            self.value = default
        else:
            self.display_value = ""
            self.value = None

    def __set__(self, instance, value):
        encoder = instance.get_encoder(value)
        if encoder:
            self.display_value = encoder
            self.value = value
        else:
            raise OptionValidationError("Encoder not available, Check available encoder with `show encoders`.")
