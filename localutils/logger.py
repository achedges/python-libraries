import os
from datetime import datetime
from io import TextIOWrapper
from localutils import dateutils
from typing import Optional

class Logger:
	
	def __init__(self, logfilepath: str='logs', logfileprefix: str='log', timestampZone: str=''):
		self.logfilepath: str = logfilepath
		self.logfileprefix: str = logfileprefix
		self.logfilename: str = f'{logfileprefix}_{str(datetime.now()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "_")}.txt'
		self.timestampZone: str = timestampZone
		
		if not os.path.isdir(self.logfilepath):
			os.mkdir(self.logfilepath)
			
		self.__log: Optional[TextIOWrapper] = None
		
	def __enter__(self):
		self.__log = open(os.path.join(self.logfilepath, self.logfilename), 'w+')
		self.__log.write('Opened log file\n')
		return self
		
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.__log.write('Closing log file\n')
		self.__log.close()
		
	def log(self, msg: str, toConsole: bool=False) -> None:
		logmsg: str = f'{dateutils.getCurrentDateTime(self.timestampZone)} {msg}'
		if not self.__log.closed:
			self.__log.write(f'{logmsg}\n')
			self.__log.flush()
		if toConsole:
			print(logmsg)
		
		
if __name__ == '__main__':
	with Logger() as logger:
		logger.log('Doing stuff')
		logger.log('Doing more stuff', toConsole=True)