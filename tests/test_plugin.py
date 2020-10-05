# pylint: disable=missing-function-docstring,missing-class-docstring
""" Unit test for lockable pytest plugin """
import unittest
import os
import pytest
from os.path import join


class TestPlugin(unittest.TestCase):

    def test_e2e(self):
        here = os.path.abspath(os.path.dirname(__file__))
        example_root = join(here, "../example")
        exit_code = pytest.main([
            "-x",  # exit instantly on first error or failed test.
            "-vvv", "-s",
            "--rootdir", example_root,
            "--allocation_resource_list_file", join(example_root, "resources.json"),
            "--allocation_lock_folder", example_root,
            "--allocation_hostname", "localhost",
            join(example_root, "test_example.py")])
        self.assertEqual(exit_code, 0)
