from abc import ABC, abstractmethod
from typing import Optional, List, Dict


### Node classes ###

class TreeNode(ABC):
	
	__slots__ = [
		'height',
		'key',
		'left',
		'right',
		'parent'
	]
	
	def __init__(self, key: object):
		self.height: int = 1
		self.key: object = key
		self.left: Optional[TreeNode] = None
		self.right: Optional[TreeNode] = None
		self.parent: Optional[TreeNode] = None

	@abstractmethod
	def getValue(self) -> object: pass

	@abstractmethod
	def copyTo(self, target): pass


class KeyNode(TreeNode):
	def __init__(self, key: object):
		TreeNode.__init__(self, key)

	def __str__(self):
		return f'{self.key}'

	def getValue(self) -> object:
		return self.key

	def copyTo(self, target):
		target.key = self.key


class KeyValueNode(TreeNode):
	
	__slots__ = [ 'value' ]
	
	def __init__(self, key: object, value: object):
		TreeNode.__init__(self, key)
		self.value: object = value

	def __str__(self):
		return f'{self.key}: {self.value}'

	def getValue(self) -> object:
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
	def _getMaxSubtreeHeight(cls, node: TreeNode) -> int:
		l = node.left.height if node.left is not None else 0
		r = node.right.height if node.right is not None else 0
		return max(l, r)

	@classmethod
	def _getSubtreeBalance(cls, node: TreeNode) -> int:
		if node is None:
			return 0
		else:
			return (node.left.height if node.left is not None else 0) - (node.right.height if node.right is not None else 0)

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

	@classmethod
	def _rotate(cls, curroot: TreeNode, direction: str) -> TreeNode:

		if direction not in ['left', 'right']:
			raise Exception(f'Unknown tree rotation direction: {direction}')

		newroot: TreeNode
		tmp: TreeNode

		if direction == 'right':
			newroot = curroot.left
			tmp = newroot.right
			newroot.right = curroot
			curroot.left = tmp
			if tmp is not None: tmp.parent = curroot

		else:
			newroot = curroot.right
			tmp = newroot.left
			newroot.left = curroot
			curroot.right = tmp
			if tmp is not None:	tmp.parent = curroot

		curroot.height = cls._getMaxSubtreeHeight(curroot) + 1
		newroot.height = cls._getMaxSubtreeHeight(newroot) + 1

		return newroot

	def _insertNode(self, root: TreeNode, node: TreeNode) -> TreeNode:
		if root is None:
			root = node
			self.size += 1
			return root

		if node.key < root.key:
			root.left = self._insertNode(root.left, node)
			root.left.parent = root
		elif node.key > root.key:
			root.right = self._insertNode(root.right, node)
			root.right.parent = root
		else:
			node.copyTo(root) # replace if key found

		lheight = root.left.height if root.left is not None else 0
		rheight = root.right.height if root.right is not None else 0
		root.height = 1 + (lheight if lheight > rheight else rheight)

		balance = (root.left.height if root.left is not None else 0) - (root.right.height if root.right is not None else 0)

		if balance > 1 and node.key < root.left.key:
			root = self._rotate(root, 'right')

		elif balance < -1 and node.key > root.right.key:
			root = self._rotate(root, 'left')

		elif balance > 1 and node.key > root.left.key:
			root.left = self._rotate(root.left, 'left')
			root = self._rotate(root, 'right')

		elif balance < -1 and node.key < root.right.key:
			root.right = self._rotate(root.right, 'right')
			root = self._rotate(root, 'left')

		if root.left is not None: root.left.parent = root
		if root.right is not None: root.right.parent = root

		return root

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

	@staticmethod
	def _bfs(node: Optional[TreeNode], depthmap: Dict[object, List[object]], depth: int) -> None:
		if node is None:
			return

		if depth not in depthmap:
			depthmap[depth] = []

		depthmap[depth].append(node.key)
		TreeBase._bfs(node.left, depthmap, depth + 1)
		TreeBase._bfs(node.right, depthmap, depth + 1)

		return

	def getKeys(self, traversal: str='inorder') -> List[object]:
		if traversal not in ['inorder','preorder','postorder','breadthfirst']:
			raise Exception(f'Invalid tree traversal order: {traversal}')

		keys: List[object] = []
		if self.root is None:
			return keys

		if traversal == 'breadthfirst':
			_map: Dict[object, List[object]] = {}
			TreeBase._bfs(self.root, _map, 0)
			for k in sorted(_map.keys()):
				keys += _map[k]

		else:
			self._walkKeys(self.root, keys, traversal)

		return keys


class TreeMap(TreeBase):

	def __init__(self):
		TreeBase.__init__(self)

	def add(self, key: object, value: object):
		self.root = self._insertNode(self.root, KeyValueNode(key, value))
		self.root.parent = None


class TreeSet(TreeBase):

	def __init__(self):
		TreeBase.__init__(self)

	def add(self, key: object):
		self.root = self._insertNode(self.root, KeyNode(key))
		self.root.parent = None