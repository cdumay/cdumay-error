#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. codeauthor:: Cédric Dumay <cedric.dumay@gmail.com>


"""
import unittest

from cdumay_error import types
from cdumay_error.registry import Registry


class TestRegistry(unittest.TestCase):
    """Tests Registry"""

    def test_status(self):
        """Test by error status"""
        self.assertIn(types.NotFound, Registry.filter_by_status(404))

    def test_serialization(self):
        """Error serialization"""
        self.assertEqual(
            Registry.error_to_dict(types.NotFound),
            {
                'code': 404, 'description': 'Not Found', 'msgid': 'ERR-08414',
                'name': 'NotFound'
            }
        )
        self.assertIn(
            {
                'code': 500, 'description': 'Configuration error',
                'msgid': 'ERR-19036', 'name': 'ConfigurationError'
            },
            Registry.to_list()
        )
        self.assertEqual(len(Registry.to_dict()), 6)

    def test_craft_error(self):
        """craft_error function"""
        my_error = Registry.craft_error(
            'ERR-19036', message="Configuration failed"
        )
        self.assertIs(my_error.name, 'ConfigurationError')
        my_error = Registry.craft_error('ERR-*****', message="Unknown error")
        self.assertIs(my_error.code, 1)
