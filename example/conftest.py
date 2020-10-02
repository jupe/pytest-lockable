""" example conftest """
import sys
import os
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(TEST_DIR, '../')
sys.path.insert(0, PLUGIN_DIR)

pytest_plugins = ("pytest_lockable.plugin", "metadata")  # pylint: disable=invalid-name
