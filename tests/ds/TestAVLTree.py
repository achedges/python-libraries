import unittest
from localutils.ds.tree import TreeMap, TreeSet, TreeBase


class AVLTestBase(unittest.TestCase):

	listSize: int = 10
	keys: list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

	def listSizeTestHelper(self, tree: TreeBase):
		self.assertEqual(tree.size, self.listSize, msg='Incorrect tree size')

	def minMaxTestHelper(self, tree: TreeBase, expectedMin: int, expectedMax: int):
		self.assertEqual(tree.minimum().getValue(), expectedMin, msg='Incorrect tree minimum')
		self.assertEqual(tree.maximum().getValue(), expectedMax, msg='Incorrect tree maximum')

	def nodeBoundariesTestHelper(self, tree: TreeBase):
		self.assertIsNone(tree.root.parent, msg='Invalid parent node on tree root')
		self.assertIsNone(tree.previous(tree.minimum()), msg='Invalid previous node on tree minimum')
		self.assertIsNone(tree.next(tree.maximum()), msg='Invalid next node on tree maximum')

	def nextNodesTestHelper(self, tree: TreeBase):
		cur = tree.minimum()
		nex = tree.next(cur)
		while nex is not None:
			exp = int(str(cur.key)) + 1
			self.assertEqual(nex.key, exp, msg='Incorrect next key')
			cur = nex
			nex = tree.next(nex)

	def previousNodesTestHelper(self, tree: TreeBase):
		cur = tree.maximum()
		pre = tree.previous(cur)
		while pre is not None:
			exp = int(str(cur.key)) - 1
			self.assertEqual(pre.key, exp, msg='Incorrect previous key')
			cur = pre
			pre = tree.previous(pre)

	def traversalTestHelper(self, tree: TreeBase, preOrderKeys: list, postOrderKeys: list):
		self.assertEqual(tree.getKeys(traversal='inorder'), self.keys, msg='Incorrect in-order traversal')
		self.assertEqual(tree.getKeys(traversal='preorder'), preOrderKeys, msg='Incorrect pre-order traversal')
		self.assertEqual(tree.getKeys(traversal='postorder'), postOrderKeys, msg='Incorrect post-order traversal')

	def findTestHelper(self, tree: TreeBase):
		for i in self.keys:
			val = tree.find(i).getValue()
			self.assertEqual(val, i, msg=f'Incorrect value found: {val}')


### TreeMap tests, node insertion in-order ###

class TestTreeMapInOrder(AVLTestBase):

	@classmethod
	def setUpClass(cls) -> None:
		AVLTestBase.setUpClass()
		cls.preOrderKeys: list = [ 3, 1, 0, 2, 7, 5, 4, 6, 8, 9 ]
		cls.postOrderKeys: list = [ 0, 2, 1, 4, 6, 5, 9, 8, 7, 3 ]
		cls.tree: TreeMap = TreeMap()

		for i in cls.keys:
			cls.tree.add(i, i)

	def testListSize(self):
		self.listSizeTestHelper(self.tree)

	def testMinMax(self):
		self.minMaxTestHelper(self.tree, 0, self.listSize - 1)

	def testNodeBoundaries(self):
		self.nodeBoundariesTestHelper(self.tree)

	def testNextNodes(self):
		self.nextNodesTestHelper(self.tree)

	def testPreviousNodes(self):
		self.previousNodesTestHelper(self.tree)

	def testTraversal(self):
		self.traversalTestHelper(self.tree, self.preOrderKeys, self.postOrderKeys)

	def testFind(self):
		self.findTestHelper(self.tree)


### TreeMap tests, node insertion reversed ###

class TestTreeMapReversed(AVLTestBase):

	@classmethod
	def setUpClass(cls) -> None:
		AVLTestBase.setUpClass()
		cls.preOrderKeys: list = [ 6, 2, 1, 0, 4, 3, 5, 8, 7, 9 ]
		cls.postOrderKeys: list = [ 0, 1, 3, 5, 4, 2, 7, 9, 8, 6 ]
		cls.tree: TreeMap = TreeMap()

		for i in cls.keys[::-1]:
			cls.tree.add(i, i)

	def testListSize(self):
		self.listSizeTestHelper(self.tree)

	def testMinMax(self):
		self.minMaxTestHelper(self.tree, 0, self.listSize - 1)

	def testNodeBoundaries(self):
		self.nodeBoundariesTestHelper(self.tree)

	def testNextNodes(self):
		self.nextNodesTestHelper(self.tree)

	def testPreviousNodes(self):
		self.previousNodesTestHelper(self.tree)

	def testTraversal(self):
		self.traversalTestHelper(self.tree, self.preOrderKeys, self.postOrderKeys)

	def testFind(self):
		self.findTestHelper(self.tree)


### TreeSet tests, node insertion in-order ###

class TestTreeSetInOrder(AVLTestBase):

	@classmethod
	def setUpClass(cls) -> None:
		AVLTestBase.setUpClass()
		cls.preOrderKeys: list = [ 3, 1, 0, 2, 7, 5, 4, 6, 8, 9 ]
		cls.postOrderKeys: list = [ 0, 2, 1, 4, 6, 5, 9, 8, 7, 3 ]
		cls.tree: TreeSet = TreeSet()

		for i in cls.keys:
			cls.tree.add(i)

	def testListSize(self):
		self.listSizeTestHelper(self.tree)

	def testMinMax(self):
		self.minMaxTestHelper(self.tree, 0, self.listSize - 1)

	def testNodeBoundaries(self):
		self.nodeBoundariesTestHelper(self.tree)

	def testNextNodes(self):
		self.nextNodesTestHelper(self.tree)

	def testPreviousNodes(self):
		self.previousNodesTestHelper(self.tree)

	def testTraversal(self):
		self.traversalTestHelper(self.tree, self.preOrderKeys, self.postOrderKeys)

	def testFind(self):
		self.findTestHelper(self.tree)


### TreeSet tests, node insertion reversed ###

class TestTreeSetReversed(AVLTestBase):

	@classmethod
	def setUpClass(cls) -> None:
		AVLTestBase.setUpClass()
		cls.preOrderKeys: list = [ 6, 2, 1, 0, 4, 3, 5, 8, 7, 9 ]
		cls.postOrderKeys: list = [ 0, 1, 3, 5, 4, 2, 7, 9, 8, 6 ]
		cls.tree: TreeSet = TreeSet()

		for i in cls.keys[::-1]:
			cls.tree.add(i)

	def testListSize(self):
		self.listSizeTestHelper(self.tree)

	def testMinMax(self):
		self.minMaxTestHelper(self.tree, 0, self.listSize - 1)

	def testNodeBoundaries(self):
		self.nodeBoundariesTestHelper(self.tree)

	def testNextNodes(self):
		self.nextNodesTestHelper(self.tree)

	def testPreviousNodes(self):
		self.previousNodesTestHelper(self.tree)

	def testTraversal(self):
		self.traversalTestHelper(self.tree, self.preOrderKeys, self.postOrderKeys)

	def testFind(self):
		self.findTestHelper(self.tree)
