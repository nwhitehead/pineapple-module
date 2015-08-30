from unittest import TestCase

import pineapple

class TestHello(TestCase):
  def test_is_string(self):
    s = pineapple.hello()
    self.assertTrue(isinstance(s, basestring))
