import unittest2

from nose import with_setup
from nose.tools import *
from alignak_app.application import AlignakApp

class TestAlignakData(unittest2.TestCase):

    def test_initialization(self):
        under_test = AlignakApp()

        self.assertIsNone(under_test.Config)
        self.assertIsNone(under_test.backend)
        self.assertIsNotNone(under_test.up_item)
        self.assertIsNotNone(under_test.down_item)
        self.assertIsNotNone(under_test.quit_item)
