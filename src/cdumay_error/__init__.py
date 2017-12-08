#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import traceback


class Error(Exception):
    def __init__(self, message, code=1, extra=None):
        self.message = message
        self.code = code
        self.stack = traceback.format_exc()
        self.extra = extra or dict()

    def __str__(self):
        return "Error {}: {}".format(self.code, self.message)
