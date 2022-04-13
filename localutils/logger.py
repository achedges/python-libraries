import os
from datetime import datetime
from io import TextIOWrapper
from typing import Optional

class Logger:
	
	def __init__(self, logfilepath: str='logs', logfileprefix: str='log'):
		self.logfilepath = logfilepath
		self.logfileprefix = logfileprefix
		self.logfilename = f'{logfileprefix}_{str(datetime.now()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "_")}.txt'
		
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
		if not self.__log.closed:
			self.__log.write(f'{msg}\n')
			self.__log.flush()
		if toConsole:
			print(msg)
		
		
if __name__ == '__main__':
	with Logger() as logger:
		logger.log('Doing stuff')
		logger.log('Doing more stuff', toConsole=True)