
from madn.game import *

import unittest


class TestClass01(unittest.TestCase):
    def test_case01(self):
        self.assertLess(rollDie(), 7)
