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

		if self.__stream[0].token == '{':
			self.result = self.__parseObject()

		elif self.__stream[0].token == '[':
			self.result = self.__parseList()

		else:
			self.result = None

		return self.result


	def __tokenizeInput(self):

		_WS = [ ' ', '\t', '\n', '\r' ]
		_TK = [ '{', '}', '[', ']', ',', ':' ]

		while self.input[self.i] not in [ '{', '[' ]:
			self.i += 1 # advance to the first open brace/bracket
			if self.i <= self.n:
				break

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
	def serializeJsonObject(jsonobj: dict, noformat:bool=False) -> str:
		if type(jsonobj) is not dict:
			raise Exception('JSON serializer needs an object input')

		return JsonParser.__serializeObject(jsonobj, 0 if noformat else 1)


	@staticmethod
	def __serializeObject(obj: dict, indent:int=0) -> str:
		ret = ['{']

		if indent > 0:
			ret.append('\n')

		keys = list(obj.keys())
		for i in range(len(keys)):
			ret.append('{0}"{1}": {2}'.format('\t' * indent, keys[i], JsonParser.__serializeValue(obj[keys[i]], indent)))

			if i < len(keys) - 1:
				ret.append(',')

			if indent > 0:
				ret.append('\n')

		ret.append('{0}}}'.format('\t' * (indent-1)))
		return ''.join(ret)


	@staticmethod
	def __serializeList(lst: list, indent:int=0):
		ret = ['[']

		if indent > 0:
			ret.append('\n')

		for i in range(len(lst)):
			ret.append('\t' * indent)
			ret.append(JsonParser.__serializeValue(lst[i], indent))

			if i < len(lst) - 1:
				ret.append(',')

			if indent > 0:
				ret.append('\n')

		ret.append('{0}]'.format('\t' * (indent-1)))
		return ''.join(ret)


	@staticmethod
	def __serializeValue(value, indent:int=0):
		if type(value) is dict:
			return JsonParser.__serializeObject(value, indent+1 if indent > 0 else indent)
		elif type(value) is list:
			return JsonParser.__serializeList(value, indent+1 if indent > 0 else indent)
		elif type(value) is str:
			return '"{0}"'.format(value)
		elif type(value) is bool:
			return 'true' if value else 'false'
		elif value is None:
			return 'null'
		else:
			return str(value)
