import unittest
from localutils.tabulator import *
from typing import List


class Test(unittest.TestCase):

	def testTableOutput(self):
		tabulator: Tabulator = Tabulator()
		tabulator.addColumnDefinition(ColumnDefinition('Symbol'))
		tabulator.addColumnDefinition(ColumnDefinition('Date'))
		tabulator.addColumnDefinition(ColumnDefinition('Volume', FormatSpecifier.CommaSeparated))
		tabulator.addColumnDefinition(ColumnDefinition('Avg Price', FormatSpecifier.Currency))

		records: List[list] = [
			[ 'ASDF', '20200930', 1234567, 1234.1234 ],
			[ 'QWER', '20200930', 987654321, 10.1423 ],
			[ 'ASDF', '20201001', 3142536, 1211.89 ],
			[ 'QWER', '20201001', 786466378, 11 ]
		]

		output: str = tabulator.toTable(records, segmentColumnIndex=1)
		with open('table-results.txt') as t:
			expected: str = t.read()

		self.assertEqual(output, expected)

		return
