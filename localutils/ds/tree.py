from abc import ABC, abstractmethod
from typing import Optional


### Node classes ###

class TreeNode(ABC):
	def __init__(self, key: object):
		self.height: int = 1
		self.key: object = key
		self.left: Optional[TreeNode] = None
		self.right: Optional[TreeNode] = None
		self.parent: Optional[TreeNode] = None

	@abstractmethod
	def getValue(self): pass

	@abstractmethod
	def copyTo(self, target): pass


class KeyNode(TreeNode):
	def __init__(self, key: object):
		TreeNode.__init__(self, key)

	def __str__(self):
		return f'{self.key}'

	def getValue(self):
		return self.key

	def copyTo(self, target):
		target.key = self.key


class KeyValueNode(TreeNode):
	def __init__(self, key: object, value: object):
		TreeNode.__init__(self, key)
		self.value: object = value

	def __str__(self):
		return f'{self.key}: {self.value}'

	def getValue(self):
		return self.value

	def copyTo(self, target):
		target.key = self.key
		target.value = self.value


### AVL-Tree implementations ###

class TreeBase(object):

	def __new__(cls, *args, **kwargs):
		if cls is TreeBase:
			raise TypeError('TreeBase can not be instantiated directly.')
		return object.__new__(cls)

	def __init__(self):
		self.size: int = 0
		self.root: Optional[TreeNode] = None

	@classmethod
	def _getSubtreeHeight(cls, node: TreeNode) -> int:
		return node.height if node is not None else 0

	@classmethod
	def _getMaxSubtreeHeight(cls, node: TreeNode) -> int:
		l = node.left.height if node.left is not None else 0
		r = node.right.height if node.right is not None else 0
		return max(l, r)

	@classmethod
	def _getSubtreeBalance(cls, node: TreeNode) -> int:
		return cls._getSubtreeHeight(node.left) - cls._getSubtreeHeight(node.right) if node is not None else 0

	@classmethod
	def _getMin(cls, node: TreeNode) -> TreeNode:
		while node.left is not None:
			node = node.left
		return node

	@classmethod
	def _getMax(cls, node: TreeNode) -> TreeNode:
		while node.right is not None:
			node = node.right
		return node

	@classmethod
	def _rotate(cls, oldroot: TreeNode, direction: str) -> TreeNode:

		if direction not in ['left', 'right']:
			raise Exception(f'Unknown tree rotation direction: {direction}')

		newroot: TreeNode
		tmp: TreeNode

		if direction == 'right':
			newroot = oldroot.left
			tmp = newroot.right
			newroot.right = oldroot
			oldroot.left = tmp

		else:
			newroot = oldroot.right
			tmp = newroot.left
			newroot.left = oldroot
			oldroot.right = tmp

		oldroot.height = cls._getMaxSubtreeHeight(oldroot) + 1
		newroot.height = cls._getMaxSubtreeHeight(newroot) + 1

		cls._setParentNodes(newroot.parent)

		return newroot

	@classmethod
	def _setParentNodes(cls, node: TreeNode):
		if node is None: return
		if node.left is not None: node.left.parent = node
		if node.right is not None: node.right.parent = node
		return

	@classmethod
	def _walkKeys(cls, node: TreeNode, elements: list, order: str= 'inorder') -> None:
		if order == 'inorder':
			if node.left is not None:
				cls._walkKeys(node.left, elements, order)
			elements.append(node.key)
			if node.right is not None:
				cls._walkKeys(node.right, elements, order)

		elif order == 'preorder':
			elements.append(node.key)
			if node.left is not None:
				cls._walkKeys(node.left, elements, order)
			if node.right is not None:
				cls._walkKeys(node.right, elements, order)

		elif order == 'postorder':
			if node.left is not None:
				cls._walkKeys(node.left, elements, order)
			if node.right is not None:
				cls._walkKeys(node.right, elements, order)
			elements.append(node.key)

		else:
			raise Exception(f'Unknown tree walk order: {order}')

		return

	@classmethod
	def next(cls, node: TreeNode) -> Optional[TreeNode]:
		if node.right is not None:
			return cls._getMin(node.right)

		parent = node.parent
		while parent is not None and parent.right is not None and node.key == parent.right.key:
			node = parent
			parent = parent.parent

		return parent

	@classmethod
	def previous(cls, node: TreeNode) -> Optional[TreeNode]:
		if node.left is not None:
			return cls._getMax(node.left)

		parent = node.parent
		while parent is not None and parent.left is not None and node.key == parent.left.key:
			node = parent
			parent = parent.parent

		return parent

	def minimum(self) -> Optional[TreeNode]:
		if self.root is None:
			return None

		return self._getMin(self.root)

	def maximum(self) -> Optional[TreeNode]:
		if self.root is None:
			return None

		return self._getMax(self.root)

	def _balanceSubtree(self, root: TreeNode, key: object) -> TreeNode:
		root.height = self._getMaxSubtreeHeight(root) + 1
		balance = self._getSubtreeBalance(root)

		if balance > 1 and key < root.left.key:
			root = self._rotate(root, 'right')

		elif balance < -1 and key > root.right.key:
			root = self._rotate(root, 'left')

		elif balance > 1 and key > root.left.key:
			root.left = self._rotate(root.left, 'left')
			root = self._rotate(root, 'right')

		elif balance < -1 and key < root.right.key:
			root.right = self._rotate(root.right, 'right')
			root = self._rotate(root, 'left')

		root.parent = None

		return root

	def _insertNode(self, root: TreeNode, node: TreeNode) -> TreeNode:
		if root is None:
			root = node
			self.size += 1
			return root

		if node.key < root.key:
			root.left = self._insertNode(root.left, node)
		elif node.key > root.key:
			root.right = self._insertNode(root.right, node)
		else:
			return root

		return self._balanceSubtree(root, node.key)

	def _deleteNode(self, root: TreeNode, key: object) -> Optional[TreeNode]:
		if root is None:
			return root

		if key < root.key:
			root.left = self._deleteNode(root.left, key)
		elif key > root.key:
			root.right = self._deleteNode(root.right, key)
		else:
			if root.left is None or root.right is None:
				tmp = root.left if root.right is None else root.right
				if tmp is not None:	root = tmp
				del tmp

			else:
				self._getMax(root.left).copyTo(root)
				root.left = self._deleteNode(root.left, root.key)

		if root is None:
			return root

		root.height = self._getMaxSubtreeHeight(root) + 1
		balance = self._getSubtreeBalance(root)

		if balance > 1 and self._getSubtreeBalance(root.left) >= 0:
			return self._rotate(root, 'right')

		elif balance > 1 and self._getSubtreeBalance(root.left) < 0:
			root.left = self._rotate(root.left, 'left')
			return self._rotate(root, 'right')

		elif balance < -1 and self._getSubtreeBalance(root.right) <= 0:
			return self._rotate(root, 'left')

		elif balance < -1 and self._getSubtreeBalance(root.right) > 0:
			root.right = self._rotate(root.right, 'right')
			return self._rotate(root, 'left')

		root.parent = None

		return root

	def find(self, key: object) -> Optional[TreeNode]:
		if self.root is None or self.root.key == key:
			return self.root

		node = self.root
		while node is not None:
			if node.key == key:
				return node
			else:
				node = node.left if key < node.key else node.right

		return None

	def contains(self, key: object) -> bool:
		return self.find(key) is not None

	def getKeys(self, traversal: str='inorder') -> list:
		if traversal not in ['inorder','preorder','postorder']:
			raise Exception(f'Invalid tree traversal order: {traversal}')

		keys = []
		if self.root is not None:
			self._walkKeys(self.root, keys, traversal)

		return keys


class TreeMap(TreeBase):

	def __init__(self):
		TreeBase.__init__(self)

	def add(self, key: object, value: object):
		self.root = self._insertNode(self.root, KeyValueNode(key, value))


class TreeSet(TreeBase):

	def __init__(self):
		TreeBase.__init__(self)

	def add(self, key: object):
		self.root = self._insertNode(self.root, KeyNode(key))