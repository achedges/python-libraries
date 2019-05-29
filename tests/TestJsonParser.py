import unittest
from localutils import jsonparser


class Test(unittest.TestCase):

	def testParser(self):

		json = '''{
			"object": {
				"string": "stringvalue",
				"int": 1,
				"float": 1.123,
				"bool": true,
				"null": null,
				"list": [
					"one",
					"two",
					"\\"three\\""
				]
			}
		}'''

		parser = jsonparser.JsonParser(jsonstring=json)
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


	def testSerializer(self):
		json = dict()
		json['string'] = 'string-value'
		json['integer'] = 123
		json['float'] = 4.56
		json['bool'] = True
		json['null'] = None
		json['list'] = [ 'list-value', 879, 0.12, False, None ]

		expected = '''{
	"string": "string-value",
	"integer": 123,
	"float": 4.56,
	"bool": true,
	"null": null,
	"list": [
		"list-value",
		879,
		0.12,
		false,
		null
	]
}'''

		jsonstring = jsonparser.JsonParser.serializeJsonObject(jsonobj=json)
		self.assertEqual(expected, jsonstring, msg='Serialized JSON object does not match input')

		return