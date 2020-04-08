import unittest
from localutils.datastructures.avltree import Tree


class Test(unittest.TestCase):

	@classmethod
	def setUpClass(cls) -> None:
		cls.listSize: int = 10
		cls.keysInOrder: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
		cls.forwardKeysPreOrder: list = [3, 1, 0, 2, 7, 5, 4, 6, 8, 9]
		cls.reverseKeysPreOrder: list = [6, 2, 1, 0, 4, 3, 5, 8, 7, 9]
		cls.forwardKeysPostOrder: list = [0, 2, 1, 4, 6, 5, 9, 8, 7, 3]
		cls.reverseKeysPostOrder: list = [0, 1, 3, 5, 4, 2, 7, 9, 8, 6]

		cls.forwardInsertTree: Tree = Tree()
		for i in range(cls.listSize):
			cls.forwardInsertTree.root = cls.forwardInsertTree.insert(cls.forwardInsertTree.root, i, i)

		cls.reverseInsertTree: Tree = Tree()
		for i in range(cls.listSize - 1, -1, -1):
			cls.reverseInsertTree.root = cls.reverseInsertTree.insert(cls.reverseInsertTree.root, i, i)


	def testListSize(self):
		self.assertEqual(self.forwardInsertTree.size, self.listSize, msg='Incorrect tree size (forward)')
		self.assertEqual(self.reverseInsertTree.size, self.listSize, msg='Incorrect tree size (reverse)')


	def testMinMax(self):
		self.assertEqual(self.forwardInsertTree.minimum().value, 0, msg='Incorrect tree minimum (forward)')
		self.assertEqual(self.forwardInsertTree.maximum().value, 9, msg='Incorrect tree maximum (forward)')

		self.assertEqual(self.reverseInsertTree.minimum().value, 0, msg='Incorrect tree minimum (reverse)')
		self.assertEqual(self.reverseInsertTree.maximum().value, 9, msg='Incorrect tree maximum (reverse)')


	def testNodeBoundaries(self):
		ftree = self.forwardInsertTree
		rtree = self.reverseInsertTree

		self.assertIsNone(ftree.root.parent, msg='Invalid parent node on tree root (forward)')
		self.assertIsNone(rtree.root.parent, msg='Invalid parent node on tree root (reverse)')

		self.assertIsNone(ftree.previous(ftree.minimum()), msg='Invalid previous node found on tree minimum (forward)')
		self.assertIsNone(ftree.next(ftree.maximum()), msg='Invalid next node found on tree maximum (forward)')

		self.assertIsNone(rtree.previous(rtree.minimum()), msg='Invalid previous node found on tree minimum (reverse)')
		self.assertIsNone(rtree.next(rtree.maximum()), msg='Invalid next node found on tree maximum (reverse)')


	def testNextNodes(self):
		cur = self.forwardInsertTree.minimum()
		nex = self.forwardInsertTree.next(cur)
		while nex is not None:
			exp = int(str(cur.key)) + 1
			self.assertEqual(nex.key, exp, msg='Incorrect next key (forward)')
			cur = nex
			nex = self.forwardInsertTree.next(nex)

		cur = self.reverseInsertTree.minimum()
		nex = self.reverseInsertTree.next(cur)
		while nex is not None:
			exp = int(str(cur.key)) + 1
			self.assertEqual(nex.key, exp, msg='Incorrect next key (reverse)')
			cur = nex
			nex = self.reverseInsertTree.next(nex)


	def testPreviousNodes(self):
		cur = self.forwardInsertTree.maximum()
		pre = self.forwardInsertTree.previous(cur)
		while pre is not None:
			exp = int(str(cur.key)) - 1
			self.assertEqual(pre.key, exp, msg='Incorrect previous key (forward)')
			cur = pre
			pre = self.forwardInsertTree.previous(pre)

		cur = self.reverseInsertTree.maximum()
		pre = self.reverseInsertTree.previous(cur)
		while pre is not None:
			exp = int(str(cur.key)) - 1
			self.assertEqual(pre.key, exp, msg='Incorrect previous key (reverse)')
			cur = pre
			pre = self.reverseInsertTree.previous(pre)


	def testTraversal(self):
		ftree = self.forwardInsertTree
		rtree = self.reverseInsertTree

		self.assertEqual(ftree.getKeys(traversal='inorder'), self.keysInOrder, msg='Incorrect in-order traversal (forward)')
		self.assertEqual(rtree.getKeys(traversal='inorder'), self.keysInOrder, msg='Incorrect in-order traversal (reverse)')

		self.assertEqual(ftree.getKeys(traversal='preorder'), self.forwardKeysPreOrder, msg='Incorrect pre-order traversal (forward)')
		self.assertEqual(rtree.getKeys(traversal='preorder'), self.reverseKeysPreOrder, msg='Incorrect pre-order traversal (reverse)')

		self.assertEqual(ftree.getKeys(traversal='postorder'), self.forwardKeysPostOrder, msg='Incorrect post-order traversal (forward)')
		self.assertEqual(rtree.getKeys(traversal='postorder'), self.reverseKeysPostOrder, msg='Incorrect post-order traversal (reverse)')


	def testFind(self):
		for i in range(self.listSize):
			fv = self.forwardInsertTree.find(i).value
			rv = self.reverseInsertTree.find(i).value
			self.assertEqual(fv, i, msg=f'Incorrect value found: {fv} (forward)')
			self.assertEqual(rv, i, msg=f'Incorrect value found: {rv} (reverse)')
