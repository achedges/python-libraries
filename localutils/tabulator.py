from enum import Enum
from typing import List, Union


class FormatSpecifier(Enum):
	CommaSeparated = 'CommaSeparated',
	Currency = 'Currency'

class ColumnDefinition:
	def __init__(self, name: str, columnFormat: Union[FormatSpecifier, str]='', padsize: int=4):
		self.name: str = name
		self.length: int = len(self.name)
		self.columnFormat: Union[FormatSpecifier, str] = columnFormat
		self.padsize = padsize

	def __str__(self):
		return f'{self.name.ljust(self.length + self.padsize)}'

	def getField(self, value):
		if self.columnFormat == FormatSpecifier.CommaSeparated:
			return f'{value:,}'
		elif self.columnFormat == FormatSpecifier.Currency:
			return f'${value:,.2f}'
		elif self.columnFormat != '':
			return f'{value:{self.columnFormat}}'

		return f'{value}'

class Tabulator:
	def __init__(self):
		self.columnDefinitions: List[ColumnDefinition] = []

	def addColumnDefinition(self, definition: ColumnDefinition):
		self.columnDefinitions.append(definition)

	def toTable(self, records: List[list]) -> str:
		_records: List[list] = []
		for record in records:
			fields: List[str] = [ self.columnDefinitions[i].getField(record[i]) for i in range(len(record)) ]
			for i in range(len(self.columnDefinitions)):
				if len(fields[i]) > self.columnDefinitions[i].length:
					self.columnDefinitions[i].length = len(fields[i])

			_records.append(fields)

		output: str = ''
		output += ''.join([ c.name.ljust(c.length + c.padsize) for c in self.columnDefinitions ]) + '\n'
		output += ''.join([ '-'.ljust(c.length + c.padsize, '-') for c in self.columnDefinitions ]) + '\n'

		if len(_records) == 0:
			output += 'No records found\n'

		for record in _records:
			output += ''.join([ record[i].ljust(self.columnDefinitions[i].length + self.columnDefinitions[i].padsize) for i in range(len(self.columnDefinitions)) ]) + '\n'

		return output