import logging,warnings
from.helpers import enums
_DEFAULT_LOG_FORMAT='%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s:%(message)s'
def reset_logger(name,level=None,handler=None):
	'\n  Make a standard python logger object with default formatter, handler, etc.\n\n  Defaults are:\n    - level == logging.INFO\n    - handler == logging.StreamHandler()\n\n  Args:\n    name: a logger name.\n    level: an optional initial log level for this logger.\n    handler: an optional initial handler for this logger.\n\n  Returns: a standard python logger with a single handler.\n\n  ';B=level;A=handler
	if B is None:B=logging.INFO
	C=logging.getLogger(name);C.setLevel(B);A=A or logging.StreamHandler();A.setFormatter(logging.Formatter(_DEFAULT_LOG_FORMAT));C.handlers=[A];return C
class BaseLogger:
	' Class encapsulating logging functionality. Override with your own logger providing log method. '
	@staticmethod
	def log(*A):0
class NoOpLogger(BaseLogger):
	' Class providing log method which logs nothing. '
	def __init__(A):A.logger=reset_logger(name='.'.join([__name__,A.__class__.__name__]),level=logging.NOTSET,handler=logging.NullHandler())
class SimpleLogger(BaseLogger):
	' Class providing log method which logs to stdout. '
	def __init__(A,min_level=enums.LogLevels.INFO):B=min_level;A.level=B;A.logger=reset_logger(name='.'.join([__name__,A.__class__.__name__]),level=B)
	def log(A,log_level,message):B='{} is deprecated. Please use standard python loggers.'.format(A.__class__);warnings.warn(B,DeprecationWarning);A.logger.log(log_level,message)
def adapt_logger(logger):
	'\n  Adapt our custom logger.BaseLogger object into a standard logging.Logger object.\n\n  Adaptations are:\n    - NoOpLogger turns into a logger with a single NullHandler.\n    - SimpleLogger turns into a logger with a StreamHandler and level.\n\n  Args:\n    logger: Possibly a logger.BaseLogger, or a standard python logging.Logger.\n\n  Returns: a standard python logging.Logger.\n\n  ';A=logger
	if isinstance(A,logging.Logger):return A
	if isinstance(A,(SimpleLogger,NoOpLogger)):return A.logger
	return A