# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: test_compiler_warning.py
# ----------------------------------------------------------------------------
"""Test for compiler_warnings/compiler_warning.py"""
import unittest

from swq.compiler_warnings.compiler_warning import CompilerWarning


class TestCompilerWarning(unittest.TestCase):
    """ TestCompilerWarnings class """
    def setUp(self):
        self.compiler_warning = CompilerWarning('file_path', 2, 3, 'msg',
                                                'some_type', 'domain')

    def test_eq(self):
        """ Test equality """
        # same class
        compiler_warning = CompilerWarning('file_path', 2, 3, 'msg',
                                           'some_type', 'domain')
        self.assertEqual((self.compiler_warning == compiler_warning), True)
        compiler_warning = CompilerWarning('file_path1', 2, 3, 'msg',
                                           'some_type', 'domain')
        self.assertEqual((self.compiler_warning == compiler_warning), False)

        # other class
        compiler_warning = {"foo": "bar"}
        self.assertEqual((self.compiler_warning == compiler_warning), False)

    def test_contains_component(self):
        """ Test contains_component() method in class """
        component = 'component'
        self.compiler_warning.components = [component, 'component1']
        self.assertEqual(self.compiler_warning.contains_component(component),
                         True)
        self.assertEqual(
            self.compiler_warning.contains_component(component + '_other'),
            False)
