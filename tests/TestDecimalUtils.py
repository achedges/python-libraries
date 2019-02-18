import unittest
from localutils import decimalutils


class Test(unittest.TestCase):

	def testParse(self):
		self.assertEqual(decimalutils.parse(None), None)
		self.assertEqual(decimalutils.parse(1), 1.0)
		self.assertEqual(decimalutils.parse(1.0), 1.0)
		self.assertEqual(decimalutils.parse(1.12345678), 1.1234)
		return