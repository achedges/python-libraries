from typing import Dict

class Trie:
	
	def __init__(self):
		self.next: Dict[str, Trie] = {}
		self.isCompleteWord: bool = False
		
	def addWord(self, word: str) -> None:
		node: Trie = self
		for char in word:
			if char not in node.next:
				node.next[char] = Trie()
			node = node.next[char]
			
		node.isCompleteWord = True
		return
	
	def isValidWord(self, word: str) -> bool:
		valid: bool = False
		node: Trie = self
		for char in word:
			if char in node.next:
				node = node.next[char]
			else:
				return valid
			
		return node.isCompleteWord
