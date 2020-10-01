import unittest
from localutils.tabulator import *
from typing import List


class Test(unittest.TestCase):

	def testTableOutput(self):
		tabulator: Tabulator = Tabulator()
		tabulator.addColumnDefinition(ColumnDefinition('Col1'))
		tabulator.addColumnDefinition(ColumnDefinition('Col2', FormatSpecifier.CommaSeparated))
		tabulator.addColumnDefinition(ColumnDefinition('Col3', FormatSpecifier.Currency))

		records: List[list] = [
			[ 'Record 1', 1234567, 1234.1234 ],
			[ 'Record 2', 987654321, 10.1423 ]
		]

		output: str = tabulator.toTable(records)
		expected: str = 'Col1        Col2           Col3         \n----------------------------------------\nRecord 1    1,234,567      $1,234.12    \nRecord 2    987,654,321    $10.14       \n'

		self.assertEqual(output, expected)

		return
