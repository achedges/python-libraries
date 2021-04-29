import unittest
from localutils import crypto


class Test(unittest.TestCase):
	
	def testGCD(self):
		
		self.assertEqual(crypto.gcd(12, 64), 4)
		self.assertEqual(crypto.gcd(270, 192), 6)
		self.assertEqual(crypto.gcd(3, 3), 3)
		self.assertEqual(crypto.gcd(1, 17), 1)
		self.assertEqual(crypto.gcd(10, 100), 10)
		
		return
