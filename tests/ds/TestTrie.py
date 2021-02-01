import unittest
from localutils.ds.trie import Trie
from typing import List


class TestTrie(unittest.TestCase):
	
	words: List[str] = [ 'add', 'adder', 'address', 'administrator', 'buffer', 'bug' ]
	trie: Trie = Trie()
	
	def setUp(self) -> None:
		for word in self.words:
			self.trie.addWord(word)
		return
	
	def testValidWords(self):
		for word in self.words:
			self.assertTrue(self.trie.isValidWord(word))
		return
	
	def testInvalidWords(self):
		self.assertFalse(self.trie.isValidWord('ad'))
		self.assertFalse(self.trie.isValidWord('adds'))
		self.assertFalse(self.trie.isValidWord('bogus'))
		self.assertFalse(self.trie.isValidWord('dog'))
		return
