import datetime
from localutils import stringutils


def generateDate(year, month, date):
	return datetime.date(year, month, date)


def getMinDate():
	return datetime.datetime(1,1,1).date()


def getDate(offset=0):
	return datetime.datetime.now().date() + datetime.timedelta(days=offset)


def getCurrentDateTime():
	return datetime.datetime.now()


def getDateTimeFromTimestamp(timestamp):
	try:
		return datetime.datetime.fromtimestamp(timestamp)
	except:
		return None


def parse(inputdate):
	if stringutils.isNoneOrEmpty(inputdate):
		return None

	if isinstance(inputdate, datetime.date):
		return inputdate

	if isinstance(inputdate, datetime.datetime):
		return inputdate.date()

	try:
		pattern = '%Y-%m-%d'
		ret = datetime.datetime.strptime(inputdate, pattern)
		return None if ret.date() == getMinDate() else ret.date()
	except:
		pass

	try:
		pattern = '%d-%b-%y'
		ret = datetime.datetime.strptime(inputdate, pattern)
		return None if ret.date() == getMinDate() else ret.date()
	except:
		return None