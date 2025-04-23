class BaseErrorHandler:
	' Class encapsulating exception handling functionality.\n  Override with your own exception handler providing handle_error method. '
	@staticmethod
	def handle_error(*A):0
class NoOpErrorHandler(BaseErrorHandler):' Class providing handle_error method which suppresses the error. '
class RaiseExceptionErrorHandler(BaseErrorHandler):
	' Class providing handle_error method which raises provided exception. '
	@staticmethod
	def handle_error(error):raise error