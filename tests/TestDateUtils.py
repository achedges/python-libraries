import datetime
import unittest
from localutils import dateutils


class Test(unittest.TestCase):

	def testParse(self):
		self.assertEqual(dateutils.parse(''), None)
		self.assertEqual(dateutils.parse(' '), None)
		self.assertEqual(dateutils.parse(None), None)
		self.assertEqual(dateutils.parse('2019-01-01'), datetime.date(2019, 1, 1))
		self.assertEqual(dateutils.parse('01-Jan-19'), datetime.date(2019, 1, 1))
		self.assertEqual(dateutils.parse('testinput'), None)
		return