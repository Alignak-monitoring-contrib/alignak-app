import unittest

from alignak_app import application as app

class TestAlignakData(unittest.TestCase):

    def test_initialization(self):
        under_test = app.AlignakApp()

        self.assertIsNone(under_test.Config)
        self.assertIsNone(under_test.backend)
        self.assertIsNotNone(under_test.up_item)
        self.assertIsNotNone(under_test.down_item)
        self.assertIsNotNone(under_test.quit_item)
