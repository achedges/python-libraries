from localutils.jsonparser import JsonParser
from unittest import TestCase


class Test(TestCase):

	def testObjectParser(self):

		with open('parse-obj.json', 'r') as jsonFile:
			json = jsonFile.read()

		parser = JsonParser(jsonstring=json)
		parser.parse()
		result = parser.result

		self.assertEqual(len(result), 1, msg='[result] dict is not the right size')
		self.assertTrue('object' in result, msg='[result] dict does not contain [object] dict')
		self.assertEqual(len(result['object']), 6, msg='[object] dict is not the right size')

		self.assertTrue('string' in result['object'], msg='[object] dict does not contain [string]')
		self.assertEqual(result['object']['string'], 'stringvalue', msg='Incorrect value found at [object][string]')

		self.assertTrue('int' in result['object'], msg='[object] dict does not contain [int]')
		self.assertEqual(result['object']['int'], 1, msg='Incorrect value found at [object][int]')

		self.assertTrue('float' in result['object'], msg='[object] dict does not contain [float]')
		self.assertEqual(result['object']['float'], 1.123, msg='Incorrect value found at [object][float]')

		self.assertTrue('bool' in result['object'], msg='[object] dict does not contain [bool]')
		self.assertEqual(result['object']['bool'], True, msg='Incorrect value found at [object][bool]')

		self.assertTrue('null' in result['object'], msg='[object] dict does not contain [null]')
		self.assertEqual(result['object']['null'], None, msg='Incorrect value found at [object][null]')

		self.assertTrue('list' in result['object'], msg='[object] dict does not contain [list]')
		self.assertEqual(len(result['object']['list']), 3, msg='[list] list is not the right size')
		self.assertEqual(result['object']['list'][0], 'one', msg='Incorrect value found at [object][list][0]')
		self.assertEqual(result['object']['list'][1], 'two', msg='Incorrect value found at [object][list][1]')
		self.assertEqual(result['object']['list'][2], '"three"', msg='Incorrect value found at [object][list][2]')

		return


	def testListParser(self):

		with open('parse-list.json', 'r') as jsonFile:
			json = jsonFile.read()

		parser = JsonParser(json)
		parser.parse()
		result = parser.result

		self.assertTrue(isinstance(result, list), msg='Result should be a list')
		self.assertEqual(len(result), 2, msg='Result list size is incorrect')

		for i in range(len(result)):
			self.assertTrue(isinstance(result[i], dict), msg='List item is not an object')
			self.assertTrue('key' in result[i], msg='Object does not contain key')
			self.assertTrue('value' in result[i], msg='Object does not contain value')
			self.assertEqual(result[i]['key'], f'some-key-{i}', msg='Incorrect key')
			self.assertEqual(result[i]['value'], f'some-value-{i}', msg='Incorrect value')

		return


	def testSerializer(self):
		json = dict()
		json['string'] = 'string-value'
		json['integer'] = 123
		json['float'] = 4.56
		json['bool'] = True
		json['null'] = None
		json['list'] = [ 'list-value', 879, 0.12, False, None ]

		with open('serialized-full.json', 'r') as serializedFile:
			expected = serializedFile.read()

		jsonstring = JsonParser.serializeJsonObject(json=json)
		self.assertEqual(expected, jsonstring, msg='Serialized JSON object does not match input')

		with open('serialized-min.json', 'r') as serializedFile:
			expected = serializedFile.read()

		jsonstring = JsonParser.serializeJsonObject(json=json, noformat=True)
		self.assertEqual(expected, jsonstring, msg='Serialized JSON object (no-format) does not match input')

		return
	
	
	def testTypeParser(self):
		
		class NestedType:
			def __init__(self):
				self.nestedInt: int = 0
				self.nestedBool: bool = False
		
		class ParsedType:
			def __init__(self):
				self.stringValue: str = ''
				self.intValue: int = 0
				self.floatValue: float = 0.
				self.boolValue: bool = False
				self.nullValue = None
				self.objectValue: NestedType = NestedType()
				self.dictValue: dict = {}
		
		with open('parse-type.json') as file:
			json: str = file.read()
			
		parser: JsonParser = JsonParser(json)
		obj: ParsedType = parser.parseToType(ParsedType)
		
		self.assertEqual(obj.stringValue, 'abc123')
		self.assertEqual(obj.intValue, 717)
		self.assertEqual(obj.floatValue, 3.14159)
		self.assertEqual(obj.boolValue, True)
		self.assertEqual(obj.nullValue, None)
		self.assertEqual(obj.objectValue.nestedInt, 171)
		self.assertEqual(obj.objectValue.nestedBool, False)
		self.assertEqual(obj.dictValue['dictFloat'], 0.3)
		self.assertEqual(obj.dictValue['dictNull'], None)
		
		return
	