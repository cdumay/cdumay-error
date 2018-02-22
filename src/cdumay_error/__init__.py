#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import traceback
from marshmallow import Schema, fields


class Error(Exception):
    def __init__(self, message, code=1, msgid=None, extra=None):
        Exception.__init__(self, code, message)
        self.message = message
        self.code = code
        self.msgid = msgid
        self.stack = traceback.format_exc()
        self.extra = extra or dict()

    def __str__(self):
        return "Error {}: {}".format(self.code, self.message)


class ErrorValidator(Schema):
    code = fields.Integer(required=True)
    message = fields.String(required=True)
    msgid = fields.String()
    extra = fields.Dict()
    stack = fields.String()
