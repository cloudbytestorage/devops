import logging
import os
import sys


def getLogger(filename, name='NHC', loglevel='INFO'):
  logger = logging.getLogger(name)
  fn = filename.split('.py')
  fh = logging.FileHandler(os.path.join(fn[0] + '.log'), 'w')
  loglevel = getattr(logging, loglevel.upper(), logging.INFO)
  logger.setLevel(loglevel)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  handler = logging.StreamHandler()
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  fh.setFormatter(formatter)
  logger.addHandler(fh)
  if logger.name == 'NHC':
      logger.warning('Running: %s %s',
                     os.path.basename(sys.argv[0]),
                     ' '.join(sys.argv[1:]))
  return logger
	

	
	
#logfile = os.path.abspath(__file__)
#a = getLogger(logfile)
