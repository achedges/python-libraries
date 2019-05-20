class JsonToken:

	def __init__(self, token: str, text: str):
		self.token = token
		self.text = text

	def __repr__(self):
		return '{0} ({1})'.format(self.token, self.text)

class JsonParser:

	def __init__(self, jsonstring: str):
		self.input = jsonstring.strip()
		self.n = len(self.input)
		self.i = 0
		self.result = dict()
		self.__stream = []


	def parse(self):
		self.__tokenizeInput()
		self.i = 0

		if self.__stream[0].token != '{':
			raise Exception("JSON documents must start with '{'")

		self.result = self.__parseObject()
		return self.result


	def __tokenizeInput(self):

		_WS = [ ' ', '\t', '\n', '\r' ]
		_TK = [ '{', '}', '[', ']', ',', ':' ]

		while self.input[self.i] != '{':
			self.i += 1 # advance to the first open brace

		while self.i < self.n:
			if self.input[self.i] in _WS:
				self.i += 1
				continue

			if self.input[self.i] in _TK:
				self.__stream.append(JsonToken(self.input[self.i], self.input[self.i]))

			elif self.input[self.i] == '"':
				_id = []
				self.i += 1
				while self.i < self.n:
					if self.input[self.i] == '"' and self.input[self.i-1] != '\\':
						break

					if self.input[self.i] == '"' and self.input[self.i-1] == '\\':
						_id[-1] = '"' # double-quotes are escaped, so replace the backslash
					else:
						_id.append(self.input[self.i])

					self.i += 1

				self.__stream.append(JsonToken('ID', ''.join(_id)))

			else:
				_lit = self.input[self.i]
				self.i += 1
				while self.i < self.n:
					if self.input[self.i] in [ ',', ']', '}' ]:
						self.i -= 1 # back-up so we can capture the ending token in the stream
						break
					elif self.input[self.i] not in _WS:
						_lit += self.input[self.i]

					self.i += 1

				self.__stream.append(JsonToken('LIT', _lit))

			self.i += 1

		return


	def __nextToken(self) -> JsonToken:
		self.i += 1
		if self.i < len(self.__stream):
			return self.__stream[self.i]
		else:
			return JsonToken('EOF', 'EOF')


	@staticmethod
	def __parseLiteral(text):
		if text == 'true':
			return True
		elif text == 'false':
			return False
		elif text == 'null':
			return None
		elif '.' in text:
			return float(text)
		else:
			return int(text)


	def __parseList(self):
		lst = []
		token = self.__nextToken()
		while token.token != ']':
			if token.token == 'ID':
				lst.append(token.text)
			elif token.token == 'LIT':
				lst.append(JsonParser.__parseLiteral(token.text))
			elif token.token == '{':
				lst.append(self.__parseObject())
			elif token.token == '[':
				lst.append(self.__parseList())

			token = self.__nextToken()
			if token.token == 'EOF':
				break

		return lst


	def __parseObject(self):
		obj = {}

		key = self.__nextToken()

		while key.token != '}':

			if key.token == ',':
				key = self.__nextToken()

			separator = self.__nextToken()
			value = self.__nextToken()

			if key.token != 'ID':
				raise Exception('Invalid token detected for object key: {0}'.format(key.token))
			if separator.token != ':':
				raise Exception('Invalid token detected for key-value separator: {0}'.format(separator.token))

			if value.token == '{':
				obj[key.text] = self.__parseObject()
			elif value.token == '[':
				obj[key.text] = self.__parseList()
			elif value.token == 'ID':
				obj[key.text] = value.text
			elif value.token == 'LIT':
				obj[key.text] = JsonParser.__parseLiteral(value.text)

			key = self.__nextToken()

		return obj


	@staticmethod
	def serializeJsonObject(jsonobj: dict) -> str:
		if type(jsonobj) is not dict:
			raise Exception('JSON serializer needs an object input')

		return JsonParser.__serializeObject(jsonobj, 1)


	@staticmethod
	def __serializeObject(obj: dict, indent:int=0) -> str:
		ret = ['{', '\n']
		for key in obj:
			ret.append('{0}"{1}":'.format('\t' * indent, key))
			if type(obj[key]) is dict:
				ret.append(JsonParser.__serializeObject(obj[key], indent+1))
			elif type(obj[key]) is list:
				ret.append(JsonParser.__serializeList(obj[key], indent+1))
			elif type(obj[key]) is str:
				ret.append('"{0}"'.format(obj[key]))
			elif type(obj[key]) is bool:
				ret.append('true' if obj[key] else 'false')
			elif obj[key] is None:
				ret.append('null')
			else:
				ret.append('{0}'.format(obj[key]))
			ret.append(',')
			ret.append('\n')

		ret[-2] = '}' # replace last comma with closing brace
		return ''.join(ret)


	@staticmethod
	def __serializeList(lst: list, indent:int=0):
		ret = ['[', '\n']
		for item in lst:
			ret.append('\t' * indent)
			if type(item) is dict:
				ret.append(JsonParser.__serializeObject(item, indent+1))
			elif type(item) is list:
				ret.append(JsonParser.__serializeList(item, indent+1))
			elif type(item) is str:
				ret.append('"{0}"'.format(item))
			elif type(item) is bool:
				ret.append('true' if item else 'false')
			elif item is None:
				ret.append('null')
			else:
				ret.append(str(item))
			ret.append(',')
			ret.append('\n')

		ret[-2] = '\n{0}]'.format('\t' * (indent-1))
		return ''.join(ret)