import unittest
from localutils.ds.heap import MaxHeap, MinHeap
from typing import List, Optional


class TestHeap(unittest.TestCase):
	
	testValues: List[int] = [ 4, 1, 6, 7, 2, 3, 9, 8, 5, 0 ]
	minHeap: MinHeap = None
	maxHeap: MaxHeap = None
	
	def setUp(self) -> None:
		self.minHeap = MinHeap()
		self.maxHeap = MaxHeap()
		for i in self.testValues:
			self.minHeap.push(i)
			self.maxHeap.push(i)
			
	def testHeapSize(self):
		self.assertEqual(self.minHeap.numvalues, len(self.testValues), msg='Incorrect min-heap size')
		self.assertEqual(self.maxHeap.numvalues, len(self.testValues), msg='Incorrect max-heap size')
			
	def testRootValue(self):
		self.assertEqual(self.minHeap.peek(), min(self.testValues), msg='Incorrect min-heap root value')
		self.assertEqual(self.maxHeap.peek(), max(self.testValues), msg='Incorrect max-heap root value')
		
	def testPop(self):
		minvalues: List[int] = []
		maxvalues: List[int] = []
		minv: Optional[int] = self.minHeap.pop()
		maxv: Optional[int] = self.maxHeap.pop()
		
		while minv is not None and maxv is not None:
			minvalues.append(minv)
			minv = self.minHeap.pop()
			maxvalues.append(maxv)
			maxv = self.maxHeap.pop()
			
		self.assertEqual(minvalues, sorted(self.testValues, reverse=False), msg='Incorrect min-heap sort result')
		self.assertEqual(maxvalues, sorted(self.testValues, reverse=True), msg='Incorrect max-heap sort result')
