from enum import Enum
from typing import Callable, List, Optional


class HeapType(Enum):
	MinHeap = 'MinHeap',
	MaxHeap = 'MaxHeap'
	

class Heap:
	
	def __init__(self, heaptype: HeapType=HeapType.MinHeap):
		self.values: List[int] = []
		self.numvalues: int = 0
		
		if heaptype == HeapType.MinHeap:
			self.comparator: Callable[[int, int], bool] = lambda x,y: x < y
		else:
			self.comparator: Callable[[int, int], bool] = lambda x,y: x > y
		
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
	
	def getChildIndex(self, index: int) -> Optional[int]:
		_left: int = self.getLeftIndex(index)
		if _left is None:
			return None
		
		_right: int = self.getRightIndex(index)
		if _right is None:
			return _left
		
		return _left if self.comparator(self.values[_left], self.values[_right]) else _right
	
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
	
	def heapifyUp(self) -> None:
		_index: int = self.numvalues - 1
		_parent: Optional[int] = Heap.getParentIndex(_index)
		while _parent is not None and self.comparator(self.values[_index], self.values[_parent]):
			self.swapValues(_index, _parent)
			_index = _parent
			_parent = Heap.getParentIndex(_parent)
			
		return
	
	def heapifyDown(self) -> None:
		_index: int = 0
		_child: Optional[int] = self.getChildIndex(_index)
		while _child is not None and self.comparator(self.values[_child], self.values[_index]):
			self.swapValues(_child, _index)
			_index = _child
			_child = self.getChildIndex(_index)
			
		return
