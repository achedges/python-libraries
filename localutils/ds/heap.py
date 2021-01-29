from abc import ABC, abstractmethod
from typing import List, Optional


class Heap(ABC):
	
	def __init__(self):
		self.values: List[int] = []
		self.numvalues: int = 0
		
	@staticmethod
	def getParentIndex(index: int) -> Optional[int]:
		if index == 0:
			return None
		
		_offset:int = 2 if index % 2 == 0 else 1
		return int((index - _offset) / 2)
	
	def getLeftIndex(self, index: int) -> Optional[int]:
		_left: int = (index * 2) + 1
		return _left if _left < self.numvalues else None
	
	def getRightIndex(self, index: int) -> Optional[int]:
		_right: int = (index * 2) + 2
		return _right if _right < self.numvalues else None
	
	def getSmallerChildIndex(self, index: int) -> Optional[int]:
		_left: int = self.getLeftIndex(index)
		if _left is None:
			return None
		
		_right: int = self.getRightIndex(index)
		if _right is None:
			return _left
		
		return _left if self.values[_left] < self.values[_right] else _right
	
	def getLargerChildIndex(self, index: int) -> Optional[int]:
		_left: int = self.getLeftIndex(index)
		if _left is None:
			return None
		
		_right: int = self.getRightIndex(index)
		if _right is None:
			return _left
		
		return _left if self.values[_left] > self.values[_right] else _right
	
	def swapValues(self, indexA: int, indexB: int) -> None:
		_tmp: int = self.values[indexA]
		self.values[indexA] = self.values[indexB]
		self.values[indexB] = _tmp
		return
	
	def peek(self) -> Optional[int]:
		return self.values[0] if self.numvalues > 0 else None
	
	def pop(self) -> Optional[int]:
		if self.numvalues == 0:
			return None
		
		_last: int = self.numvalues - 1
		_value: int = self.values[0]
		self.swapValues(0, _last)
		self.numvalues -= 1
		self.heapifyDown()
		return _value
	
	def push(self, value: int) -> None:
		if self.numvalues == len(self.values):
			self.values.append(value)
		else:		
			self.values[self.numvalues] = value
			
		self.numvalues += 1
		self.heapifyUp()
		return
	
	@abstractmethod
	def heapifyUp(self) -> None:
		raise Exception('Calling abstract heapifyUp() method')
	
	@abstractmethod
	def heapifyDown(self) -> None:
		raise Exception('Calling abstract heapifyDown() method')


class MinHeap(Heap):
	
	def __init__(self):
		Heap.__init__(self)
	
	def heapifyUp(self) -> None:
		_index: int = self.numvalues - 1
		_parent: int = Heap.getParentIndex(_index)
		while _parent is not None and self.values[_parent] > self.values[_index]:
			self.swapValues(_index, _parent)
			_index = _parent
			_parent = Heap.getParentIndex(_parent)
			
		return
	
	def heapifyDown(self) -> None:
		_index: int = 0
		_child: Optional[int] = self.getSmallerChildIndex(_index)
		while _child is not None and self.values[_child] < self.values[_index]:
			self.swapValues(_child, _index)
			_index = _child
			_child = self.getSmallerChildIndex(_index)
		return
	
	
class MaxHeap(Heap):
	
	def __init__(self):
		Heap.__init__(self)
	
	def heapifyUp(self) -> None:
		_index: int = self.numvalues - 1
		_parent: int = Heap.getParentIndex(_index)
		while _parent is not None and self.values[_parent] < self.values[_index]:
			self.swapValues(_index, _parent)
			_index = _parent
			_parent = Heap.getParentIndex(_parent)
			
		return
	
	def heapifyDown(self) -> None:
		_index: int = 0
		_child: Optional[int] = self.getLargerChildIndex(_index)
		while _child is not None and self.values[_child] > self.values[_index]:
			self.swapValues(_child, _index)
			_index = _child
			_child = self.getLargerChildIndex(_index)
		
		return
