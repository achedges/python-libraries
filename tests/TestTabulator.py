import unittest
from localutils.tabulator import *
from typing import List


class Test(unittest.TestCase):

	def testTableOutput(self):
		tabulator: Tabulator = Tabulator()
		tabulator.addColumn(ColumnDefinition('Symbol')) # test with ColumnDefinition
		tabulator.addColumn(columnName='Date') # test with name only
		tabulator.addColumn(ColumnDefinition('Volume', FormatSpecifier.CommaSeparated))
		tabulator.addColumn(ColumnDefinition('Avg Price', FormatSpecifier.Currency))
		tabulator.addColumn(ColumnDefinition('Rate', FormatSpecifier.Percentage))

		records: List[list] = [
			[ 'ASDF', '20200930', 1234567, 1234.1234, .3319 ],
			[ 'QWER', '20200930', 987654321, 10.1423, .7834562 ],
			[ 'ASDF', '20201001', 3142536, 1211.89, 1 ],
			[ 'QWER', '20201001', 786466378, 11, 0 ]
		]

		output: str = tabulator.toTable(records, segmentColumnIndex=1)
		with open('table-results.txt') as t:
			expected: str = t.read()

		self.assertEqual(output, expected)

		return
	
	def testVariableColumnInit(self):
		tabulator: Tabulator = Tabulator("One", "Two", "Three")
		output: str = tabulator.toTable([])
		expected: str = '\nOne    Two    Three    \n-----------------------\nNo records found\n'
		self.assertEqual(output, expected)
		return
