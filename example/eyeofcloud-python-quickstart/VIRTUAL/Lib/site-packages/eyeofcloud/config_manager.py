_B='Fetching datafile from {} failed. Error: {}'
_A=None
import abc,numbers,requests,threading,time
from requests import codes as http_status_codes,exceptions as requests_exceptions
from.import exceptions as eyeofcloud_exceptions
from.import logger as eyeofcloud_logger
from.import project_config
from.error_handler import NoOpErrorHandler
from.notification_center import NotificationCenter
from.helpers import enums
from.helpers import validator
from.eyeofcloud_config import EyeofcloudConfigService
ABC=abc.ABCMeta('ABC',(object,),{'__slots__':()})
class BaseConfigManager(ABC):
	" Base class for Eyeofcloud's config manager. "
	def __init__(A,logger=_A,error_handler=_A,notification_center=_A):' Initialize config manager.\n\n        Args:\n            logger: Provides a logger instance.\n            error_handler: Provides a handle_error method to handle exceptions.\n            notification_center: Provides instance of notification_center.NotificationCenter.\n        ';A.logger=eyeofcloud_logger.adapt_logger(logger or eyeofcloud_logger.NoOpLogger());A.error_handler=error_handler or NoOpErrorHandler();A.notification_center=notification_center or NotificationCenter(A.logger);A._validate_instantiation_options()
	def _validate_instantiation_options(A):
		' Helper method to validate all parameters.\n\n        Raises:\n            Exception if provided options are invalid.\n        '
		if not validator.is_logger_valid(A.logger):raise eyeofcloud_exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format('logger'))
		if not validator.is_error_handler_valid(A.error_handler):raise eyeofcloud_exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format('error_handler'))
		if not validator.is_notification_center_valid(A.notification_center):raise eyeofcloud_exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format('notification_center'))
	@abc.abstractmethod
	def get_config(self):' Get config for use by eyeofcloud.Eyeofcloud.\n        The config should be an instance of project_config.ProjectConfig.'
class StaticConfigManager(BaseConfigManager):
	' Config manager that returns ProjectConfig based on provided datafile. '
	def __init__(A,datafile=_A,logger=_A,error_handler=_A,notification_center=_A,skip_json_validation=False):' Initialize config manager. Datafile has to be provided to use.\n\n        Args:\n            datafile: JSON string representing the Eyeofcloud project.\n            logger: Provides a logger instance.\n            error_handler: Provides a handle_error method to handle exceptions.\n            notification_center: Notification center to generate config update notification.\n            skip_json_validation: Optional boolean param which allows skipping JSON schema\n                                  validation upon object invocation. By default\n                                  JSON schema validation will be performed.\n        ';super(StaticConfigManager,A).__init__(logger=logger,error_handler=error_handler,notification_center=notification_center);A._config=_A;A.eyeofcloud_config=_A;A.validate_schema=not skip_json_validation;A._set_config(datafile)
	def _set_config(A,datafile):
		' Looks up and sets datafile and config based on response body.\n\n        Args:\n            datafile: JSON string representing the Eyeofcloud project.\n        ';H='datafile';E=datafile
		if A.validate_schema:
			if not validator.is_datafile_valid(E):A.logger.error(enums.Errors.INVALID_INPUT.format(H));return
		B=_A;D=_A;C=_A
		try:C=project_config.ProjectConfig(E,A.logger,A.error_handler)
		except eyeofcloud_exceptions.UnsupportedDatafileVersionException as F:B=F.args[0];D=F
		except:B=enums.Errors.INVALID_INPUT.format(H);D=eyeofcloud_exceptions.InvalidInputException(B)
		finally:
			if B:A.logger.error(B);A.error_handler.handle_error(D);return
		G=A._config.get_revision()if A._config else _A
		if G==C.get_revision():return
		A._config=C;A.eyeofcloud_config=EyeofcloudConfigService(C).get_config();A.notification_center.send_notifications(enums.NotificationTypes.OPTIMIZELY_CONFIG_UPDATE);A.logger.debug('Received new datafile and updated config. Old revision number: {}. New revision number: {}.'.format(G,C.get_revision()))
	def get_config(A):' Returns instance of ProjectConfig.\n\n        Returns:\n            ProjectConfig. None if not set.\n        ';return A._config
class PollingConfigManager(StaticConfigManager):
	' Config manager that polls for the datafile and updated ProjectConfig based on an update interval. ';DATAFILE_URL_TEMPLATE=enums.ConfigManager.DATAFILE_URL_TEMPLATE
	def __init__(A,sdk_key=_A,datafile=_A,update_interval=_A,blocking_timeout=_A,url=_A,url_template=_A,logger=_A,error_handler=_A,notification_center=_A,skip_json_validation=False):' Initialize config manager. One of sdk_key or url has to be set to be able to use.\n\n        Args:\n            sdk_key: Optional string uniquely identifying the datafile.\n            datafile: Optional JSON string representing the project.\n            update_interval: Optional floating point number representing time interval in seconds\n                             at which to request datafile and set ProjectConfig.\n            blocking_timeout: Optional Time in seconds to block the get_config call until config object\n                              has been initialized.\n            url: Optional string representing URL from where to fetch the datafile. If set it supersedes the sdk_key.\n            url_template: Optional string template which in conjunction with sdk_key\n                          determines URL from where to fetch the datafile.\n            logger: Provides a logger instance.\n            error_handler: Provides a handle_error method to handle exceptions.\n            notification_center: Notification center to generate config update notification.\n            skip_json_validation: Optional boolean param which allows skipping JSON schema\n                                  validation upon object invocation. By default\n                                  JSON schema validation will be performed.\n\n        ';A._config_ready_event=threading.Event();super(PollingConfigManager,A).__init__(datafile=datafile,logger=logger,error_handler=error_handler,notification_center=notification_center,skip_json_validation=skip_json_validation);A.datafile_url=A.get_datafile_url(sdk_key,url,url_template or A.DATAFILE_URL_TEMPLATE);A.set_update_interval(update_interval);A.set_blocking_timeout(blocking_timeout);A.last_modified=_A;A._polling_thread=threading.Thread(target=A._run);A._polling_thread.setDaemon(True);A._polling_thread.start()
	@staticmethod
	def get_datafile_url(sdk_key,url,url_template):
		' Helper method to determine URL from where to fetch the datafile.\n\n        Args:\n          sdk_key: Key uniquely identifying the datafile.\n          url: String representing URL from which to fetch the datafile.\n          url_template: String representing template which is filled in with\n                        SDK key to determine URL from which to fetch the datafile.\n\n        Returns:\n          String representing URL to fetch datafile from.\n\n        Raises:\n          eyeofcloud.exceptions.InvalidInputException if:\n          - One of sdk_key or url is not provided.\n          - url_template is invalid.\n        ';C=url_template;B=sdk_key;A=url
		if B is _A and A is _A:raise eyeofcloud_exceptions.InvalidInputException('Must provide at least one of sdk_key or url.')
		if A is _A:
			try:return C.format(sdk_key=B)
			except(AttributeError,KeyError):raise eyeofcloud_exceptions.InvalidInputException('Invalid url_template {} provided.'.format(C))
		return A
	def _set_config(A,datafile):
		' Looks up and sets datafile and config based on response body.\n\n        Args:\n            datafile: JSON string representing the Eyeofcloud project.\n        ';B=datafile
		if B or A._config_ready_event.is_set():super(PollingConfigManager,A)._set_config(datafile=B);A._config_ready_event.set()
	def get_config(A):' Returns instance of ProjectConfig. Returns immediately if project config is ready otherwise\n        blocks maximum for value of blocking_timeout in seconds.\n\n        Returns:\n            ProjectConfig. None if not set.\n        ';A._config_ready_event.wait(A.blocking_timeout);return A._config
	def set_update_interval(B,update_interval):
		' Helper method to set frequency at which datafile has to be polled and ProjectConfig updated.\n\n        Args:\n            update_interval: Time in seconds after which to update datafile.\n        ';A=update_interval
		if A is _A:A=enums.ConfigManager.DEFAULT_UPDATE_INTERVAL;B.logger.debug('Setting config update interval to default value {}.'.format(A))
		if not isinstance(A,(int,float)):raise eyeofcloud_exceptions.InvalidInputException('Invalid update_interval "{}" provided.'.format(A))
		if A<=0:B.logger.debug('update_interval value {} too small. Defaulting to {}'.format(A,enums.ConfigManager.DEFAULT_UPDATE_INTERVAL));A=enums.ConfigManager.DEFAULT_UPDATE_INTERVAL
		B.update_interval=A
	def set_blocking_timeout(B,blocking_timeout):
		' Helper method to set time in seconds to block the config call until config has been initialized.\n\n        Args:\n            blocking_timeout: Time in seconds to block the config call.\n        ';A=blocking_timeout
		if A is _A:A=enums.ConfigManager.DEFAULT_BLOCKING_TIMEOUT;B.logger.debug('Setting config blocking timeout to default value {}.'.format(A))
		if not isinstance(A,(numbers.Integral,float)):raise eyeofcloud_exceptions.InvalidInputException('Invalid blocking timeout "{}" provided.'.format(A))
		if A<0:B.logger.debug('blocking timeout value {} too small. Defaulting to {}'.format(A,enums.ConfigManager.DEFAULT_BLOCKING_TIMEOUT));A=enums.ConfigManager.DEFAULT_BLOCKING_TIMEOUT
		B.blocking_timeout=A
	def set_last_modified(A,response_headers):' Looks up and sets last modified time based on Last-Modified header in the response.\n\n        Args:\n            response_headers: requests.Response.headers\n        ';A.last_modified=response_headers.get(enums.HTTPHeaders.LAST_MODIFIED)
	def _handle_response(A,response):
		' Helper method to handle response containing datafile.\n\n        Args:\n            response: requests.Response\n        ';B=response
		try:B.raise_for_status()
		except requests_exceptions.RequestException as C:A.logger.error(_B.format(A.datafile_url,str(C)));return
		if B.status_code==http_status_codes.not_modified:A.logger.debug('Not updating config as datafile has not updated since {}.'.format(A.last_modified));return
		A.set_last_modified(B.headers);A._set_config(B.content)
	def fetch_datafile(A):
		' Fetch datafile and set ProjectConfig. ';B={}
		if A.last_modified:B[enums.HTTPHeaders.IF_MODIFIED_SINCE]=A.last_modified
		try:C=requests.get(A.datafile_url,headers=B,timeout=enums.ConfigManager.REQUEST_TIMEOUT)
		except requests_exceptions.RequestException as D:A.logger.error(_B.format(A.datafile_url,str(D)));return
		A._handle_response(C)
	@property
	def is_running(self):' Check if polling thread is alive or not. ';return self._polling_thread.is_alive()
	def _run(A):
		' Triggered as part of the thread which fetches the datafile and sleeps until next update interval. '
		try:
			while A.is_running:A.fetch_datafile();time.sleep(A.update_interval)
		except(OSError,OverflowError)as B:A.logger.error('Error in time.sleep. Provided update_interval value may be too big. Error: {}'.format(str(B)));raise
	def start(A):
		' Start the config manager and the thread to periodically fetch datafile. '
		if not A.is_running:A._polling_thread.start()
class AuthDatafilePollingConfigManager(PollingConfigManager):
	' Config manager that polls for authenticated datafile using access token. ';DATAFILE_URL_TEMPLATE=enums.ConfigManager.AUTHENTICATED_DATAFILE_URL_TEMPLATE
	def __init__(A,datafile_access_token,*B,**C):' Initialize config manager. One of sdk_key or url has to be set to be able to use.\n\n        Args:\n            datafile_access_token: String to be attached to the request header to fetch the authenticated datafile.\n            *args: Refer to arguments descriptions in PollingConfigManager.\n            **kwargs: Refer to keyword arguments descriptions in PollingConfigManager.\n        ';A._set_datafile_access_token(datafile_access_token);super(AuthDatafilePollingConfigManager,A).__init__(*B,**C)
	def _set_datafile_access_token(B,datafile_access_token):
		' Checks for valid access token input and sets it. ';A=datafile_access_token
		if not A:raise eyeofcloud_exceptions.InvalidInputException('datafile_access_token cannot be empty or None.')
		B.datafile_access_token=A
	def fetch_datafile(A):
		' Fetch authenticated datafile and set ProjectConfig. ';B={enums.HTTPHeaders.AUTHORIZATION:enums.ConfigManager.AUTHORIZATION_HEADER_DATA_TEMPLATE.format(datafile_access_token=A.datafile_access_token)}
		if A.last_modified:B[enums.HTTPHeaders.IF_MODIFIED_SINCE]=A.last_modified
		try:C=requests.get(A.datafile_url,headers=B,timeout=enums.ConfigManager.REQUEST_TIMEOUT)
		except requests_exceptions.RequestException as D:A.logger.error(_B.format(A.datafile_url,str(D)));return
		A._handle_response(C)