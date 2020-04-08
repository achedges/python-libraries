from typing import Optional


class Node:
	def __init__(self, key: object, value: object):
		self.height: int = 1
		self.key: object = key
		self.value: object = value
		self.left: Optional[Node] = None
		self.right: Optional[Node] = None
		self.parent: Optional[Node] = None

	def __str__(self):
		return f'{self.key}: {self.value}'

class Tree:

	def __init__(self):
		self.size: int = 0
		self.root: Optional[Node] = None

	@classmethod
	def __getSubtreeHeight(cls, node: Node) -> int:
		return node.height if node is not None else 0

	@classmethod
	def __getMaxSubtreeHeight(cls, node: Node) -> int:
		l = node.left.height if node.left is not None else 0
		r = node.right.height if node.right is not None else 0
		return max(l, r)

	@classmethod
	def __getSubtreeBalance(cls, node: Node) -> int:
		return cls.__getSubtreeHeight(node.left) - cls.__getSubtreeHeight(node.right) if node is not None else 0

	@classmethod
	def __getMin(cls, node: Node) -> Node:
		while node.left is not None:
			node = node.left
		return node

	@classmethod
	def __getMax(cls, node: Node) -> Node:
		while node.right is not None:
			node = node.right
		return node

	@classmethod
	def __rotate(cls, oldroot: Node, direction: str) -> Node:

		# the assignments to oldroot.left/right/height seem to be confusing PyCharm into thinking that the Tree itself has left/right/height

		if direction not in ['left', 'right']:
			raise Exception(f'Unknown tree rotation direction: {direction}')

		newroot: Node
		tmp: Node

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

		oldroot.height = cls.__getMaxSubtreeHeight(oldroot) + 1
		newroot.height = cls.__getMaxSubtreeHeight(newroot) + 1

		cls.__setParentNodes(newroot.parent)

		return newroot

	@classmethod
	def __setParentNodes(cls, node: Node):
		if node is None: return
		if node.left is not None: node.left.parent = node
		if node.right is not None: node.right.parent = node
		return

	@classmethod
	def __walkKeys(cls, node: Node, elements: list, order: str='inorder') -> None:
		if order == 'inorder':
			if node.left is not None:
				cls.__walkKeys(node.left, elements, order)
			elements.append(node.key)
			if node.right is not None:
				cls.__walkKeys(node.right, elements, order)

		elif order == 'preorder':
			elements.append(node.key)
			if node.left is not None:
				cls.__walkKeys(node.left, elements, order)
			if node.right is not None:
				cls.__walkKeys(node.right, elements, order)

		elif order == 'postorder':
			if node.left is not None:
				cls.__walkKeys(node.left, elements, order)
			if node.right is not None:
				cls.__walkKeys(node.right, elements, order)
			elements.append(node.key)

		else:
			raise Exception(f'Unknown tree walk order: {order}')

		return

	@classmethod
	def next(cls, node: Node) -> Optional[Node]:
		if node.right is not None:
			return cls.__getMin(node.right)

		parent = node.parent
		while parent is not None and parent.right is not None and node.key == parent.right.key:
			node = parent
			parent = parent.parent

		return parent

	@classmethod
	def previous(cls, node: Node) -> Optional[Node]:
		if node.left is not None:
			return cls.__getMax(node.left)

		parent = node.parent
		while parent is not None and parent.left is not None and node.key == parent.left.key:
			node = parent
			parent = parent.parent

		return parent

	def minimum(self) -> Optional[Node]:
		if self.root is None:
			return None

		return self.__getMin(self.root)

	def maximum(self) -> Optional[Node]:
		if self.root is None:
			return None

		return self.__getMax(self.root)

	def insert(self, root: Node, key: object, value: object) -> Node:
		if root is None:
			root = Node(key, value)
			self.size += 1
			return root

		if key < root.key:
			root.left = self.insert(root.left, key, value)
		elif key > root.key:
			root.right = self.insert(root.right, key, value)
		else:
			return root

		root.height = self.__getMaxSubtreeHeight(root) + 1
		balance = self.__getSubtreeBalance(root)

		if balance > 1 and key < root.left.key:
			root = self.__rotate(root, 'right')

		elif balance < -1 and key > root.right.key:
			root = self.__rotate(root, 'left')

		elif balance > 1 and key > root.left.key:
			root.left = self.__rotate(root.left, 'left')
			root = self.__rotate(root, 'right')

		elif balance < -1 and key < root.right.key:
			root.right = self.__rotate(root.right, 'right')
			root = self.__rotate(root, 'left')
		root.parent = None

		return root

	def delete(self, root: Node, key: object) -> Optional[Node]:
		if root is None:
			return root

		if key < root.key:
			root.left = self.delete(root.left, key)
		elif key > root.key:
			root.right = self.delete(root.right, key)
		else:
			if root.left is None or root.right is None:
				tmp = root.left if root.right is None else root.right
				if tmp is not None:	root = tmp
				del tmp

			else:
				tmp = self.__getMax(root.left)
				root.key = tmp.key
				root.value = tmp.value
				root.left = self.delete(root.left, tmp.key)

		if root is None:
			return root

		root.height = self.__getMaxSubtreeHeight(root) + 1
		balance = self.__getSubtreeBalance(root)

		if balance > 1 and self.__getSubtreeBalance(root.left) >= 0:
			return self.__rotate(root, 'right')

		elif balance > 1 and self.__getSubtreeBalance(root.left) < 0:
			root.left = self.__rotate(root.left, 'left')
			return self.__rotate(root, 'right')

		elif balance < -1 and self.__getSubtreeBalance(root.right) <= 0:
			return self.__rotate(root, 'left')

		elif balance < -1 and self.__getSubtreeBalance(root.right) > 0:
			root.right = self.__rotate(root.right, 'right')
			return self.__rotate(root, 'left')

		root.parent = None

		return root

	def find(self, key: object) -> Optional[Node]:
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
			self.__walkKeys(self.root, keys, traversal)

		return keys