def isNoneOrEmpty(inputstring):
	if inputstring is None:
		return True

	inputstring = str(inputstring)
	if inputstring == 'None':
		return True
	else:
		return inputstring.strip() == ''


def padleft(inputstring, length, padchar=' '):
	i = str(inputstring)
	slack = length - len(i)
	return i if slack <= 0 else '{0}{1}'.format(padchar * slack, i)


def padright(inputstring, length, padchar=' '):
	i = str(inputstring)
	slack = length - len(i)
	return i if slack <= 0 else '{0}{1}'.format(i, padchar * slack)