from abc import ABC, abstractmethod
from typing import Optional


class TreeNode(ABC):
	def __init__(self, key: object):
		self.height: int = 1
		self.key: object = key
		self.left: Optional[TreeNode] = None
		self.right: Optional[TreeNode] = None
		self.parent: Optional[TreeNode] = None

	@abstractmethod
	def getValue(self):
		pass

	@abstractmethod
	def copyTo(self, target):
		pass


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


class KeyNode(TreeNode):
	def __init__(self, key: object):
		TreeNode.__init__(self, key)

	def __str__(self):
		return f'{self.key}'

	def getValue(self):
		return self.key

	def copyTo(self, target):
		target.key = self.key