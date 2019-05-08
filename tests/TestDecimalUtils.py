import unittest
from localutils import decimalutils


class Test(unittest.TestCase):

	def testParse(self):
		self.assertEqual(decimalutils.parse(None), None)
		self.assertEqual(decimalutils.parse(1), 1.0)
		self.assertEqual(decimalutils.parse(1.0), 1.0)
		self.assertEqual(decimalutils.parse(1.12345678), 1.1234)
		return

	def testTruncate(self):
		self.assertEqual(decimalutils.truncate(123.456, precision=2), 123.45)
		self.assertEqual(decimalutils.truncate(123, precision=2), 123.0)
		self.assertEqual(decimalutils.truncate(123.4, precision=3), 123.4)
		self.assertEqual(decimalutils.truncate(123.456789, precision=5), 123.45678)
		return