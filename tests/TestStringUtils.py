import unittest
from localutils import stringutils


class Test(unittest.TestCase):

	def testIsNoneOrEmpty(self):
		self.assertTrue(stringutils.isNoneOrEmpty(None))
		self.assertTrue(stringutils.isNoneOrEmpty(''))
		self.assertTrue(stringutils.isNoneOrEmpty(' '))
		self.assertFalse(stringutils.isNoneOrEmpty('a'))
		self.assertFalse(stringutils.isNoneOrEmpty(1))
		self.assertFalse(stringutils.isNoneOrEmpty(True))

		return

	def testPadLeft(self):
		self.assertEqual(stringutils.padleft('asdf', 8), '    asdf')
		self.assertEqual(stringutils.padleft('asdf', 8, padchar='*'), '****asdf')
		self.assertEqual(stringutils.padleft('asdf', 8, padchar=''), 'asdf')
		return

	def testPadRight(self):
		self.assertEqual(stringutils.padright('asdf', 8), 'asdf    ')
		self.assertEqual(stringutils.padright('asdf', 8, padchar='*'), 'asdf****')
		self.assertEqual(stringutils.padright('asdf', 8, padchar=''), 'asdf')
		return