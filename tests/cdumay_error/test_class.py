#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import json
import unittest

import marshmallow

from cdumay_error import Error, ErrorSchema, from_exc, types


class TestError(unittest.TestCase):
    """Tests for class Error"""

    def test_init(self):
        """Test Error init"""
        with self.assertRaises(Error) as context:
            raise Error(message="My error")

        self.assertEqual(context.exception.message, "My error")
        self.assertEqual(context.exception.extra, {})
        self.assertEqual(context.exception.msgid, "Err-00000")
        self.assertIsNone(context.exception.stack)
        self.assertEqual(context.exception.name, 'Error')
        self.assertEqual(context.exception.code, 1)

    def test_serialization(self):
        """Error serialization"""
        my_error = Error(message="My error")
        desired = {
            "msgid": "Err-00000", "code": 1, "extra": {}, "stack": None,
            "name": "Error", "message": "My error"
        }
        self.assertEqual(json.loads(my_error.to_json()), desired)
        self.assertEqual(my_error.to_dict(), desired)

    def test_deserialization(self):
        """Error deserialization"""
        self.assertEqual(
            Error.from_json({"message": "My error"}),
            {"message": "My error"}
        )

    def test_repr(self):
        """String representation"""
        my_error = Error(message="My error")
        self.assertEqual(
            repr(my_error),
            'Error<code=1, msgid=Err-00000, message=My error>'
        )
        self.assertEqual(str(my_error), 'Err-00000: My error')
        self.assertEqual(ErrorSchema.class_name(my_error), 'Error')

    def test_load_error(self):
        """Load Error instance"""
        self.assertEqual(
            str(from_exc(Error(message="My error"))),
            'Err-00000: My error'
        )

    def test_intercept_marshmallow_error(self):
        """Load marshmallow.ValidationError"""

        class MySchema(marshmallow.Schema):
            """Custom schema"""
            my_int = marshmallow.fields.Int()

        with self.assertRaises(marshmallow.ValidationError) as context:
            MySchema().load({"my_int": "string"})

        my_error = from_exc(context.exception)
        self.assertIsInstance(my_error, types.ValidationError)

    def test_load_exception(self):
        """Load Error instance"""

        with self.assertRaises(ZeroDivisionError) as context:
            5 / 0

        my_error = from_exc(context.exception)
        self.assertIsInstance(my_error, types.InternalError)
        self.assertEqual(my_error.message, 'division by zero')
