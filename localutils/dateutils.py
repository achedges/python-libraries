import datetime
import pytz
from localutils import stringutils


def generateDate(year, month, date):
	return datetime.date(year, month, date)


def generateDateTime(year: int, month: int, date: int, hour: int, minute: int, second: int, timezone: str='') -> datetime.datetime:
	dt = datetime.datetime(year, month, date, hour, minute, second)
	if timezone != '':
		tz = pytz.timezone(timezone)
		dt = tz.localize(dt)
	return dt


def getMinDate():
	return datetime.datetime(1,1,1).date()


def getDate(offset=0):
	return datetime.datetime.now().date() + datetime.timedelta(days=offset)


def getCurrentDateTime(zone: str=''):
	dt = datetime.datetime.now()
	if zone != '':
		tz = pytz.timezone(zone)
		dt = tz.localize(dt)
	return dt


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