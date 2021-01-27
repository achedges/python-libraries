from enum import Enum
from typing import List, Union


class FormatSpecifier(Enum):
	CommaSeparated = 'CommaSeparated',
	Currency = 'Currency',
	Percentage = 'Percentage'

class ColumnDefinition:
	def __init__(self, name: str, columnFormat: Union[FormatSpecifier, str]='', padlen: int=4, fieldlen: int=None):
		self.name: str = name
		self.columnFormat: Union[FormatSpecifier, str] = columnFormat
		self.fieldlen: int = len(self.name) if fieldlen is None else fieldlen
		self.padlen = padlen

	def __str__(self):
		return f'{self.name.ljust(self.fieldlen + self.padlen)}'

	def getField(self, value):
		if self.columnFormat == FormatSpecifier.CommaSeparated:
			return f'{value:,}'
		elif self.columnFormat == FormatSpecifier.Currency:
			return f'${value:,.2f}'
		elif self.columnFormat == FormatSpecifier.Percentage:
			return f'{value * 100:.2f}%'
		elif self.columnFormat != '':
			return f'{value:{self.columnFormat}}'

		return f'{value}'

class Tabulator:
	def __init__(self):
		self.columnDefinitions: List[ColumnDefinition] = []

	def addColumnDefinition(self, definition: ColumnDefinition):
		self.columnDefinitions.append(definition)
		
	def getTableHeader(self):
		header: str = '\n'
		header += ''.join([c.name.ljust(c.fieldlen + c.padlen) for c in self.columnDefinitions]) + '\n'
		header += ''.join([ '-'.ljust(c.fieldlen + c.padlen, '-') for c in self.columnDefinitions])
		return header

	def toTable(self, records: List[list], segmentColumnIndex: int = None) -> str:
		# validate the segment column index, if provided
		if segmentColumnIndex is not None and (segmentColumnIndex < 0 or segmentColumnIndex > len(self.columnDefinitions)):
			segmentColumnIndex = None			
		
		_records: List[list] = []
		for record in records:
			fields: List[str] = [ self.columnDefinitions[i].getField(record[i]) for i in range(len(record)) ]
			for i in range(len(self.columnDefinitions)):
				if len(fields[i]) > self.columnDefinitions[i].fieldlen:
					self.columnDefinitions[i].fieldlen = len(fields[i])

			_records.append(fields)

		output: str = self.getTableHeader() + '\n' # initialize output with table header

		if len(_records) == 0:
			output += 'No records found\n'
		
		segmentValue: str = ''
		if segmentColumnIndex is not None:
			segmentValue = _records[0][segmentColumnIndex]

		for record in _records:
			if segmentColumnIndex is not None and record[segmentColumnIndex] != segmentValue:
				output += self.getTableHeader() + '\n'
				segmentValue = record[segmentColumnIndex]
				
			output += self.toRow(record) + '\n'

		return output
	
	def toRow(self, record: List[str]) -> str:
		return ''.join([record[i].ljust(self.columnDefinitions[i].fieldlen + self.columnDefinitions[i].padlen) for i in range(len(self.columnDefinitions))])
