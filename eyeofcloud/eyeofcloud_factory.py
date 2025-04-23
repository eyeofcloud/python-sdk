_H='notification_center'
_G='error_handler'
_F='logger'
_E='datafile'
_D='blocking_timeout'
_C='update_interval'
_B='sdk_key'
_A=None
from.import logger as eyeofcloud_logger
from.config_manager import PollingConfigManager
from.error_handler import NoOpErrorHandler
from.event.event_processor import BatchEventProcessor
from.event_dispatcher import EventDispatcher
from.notification_center import NotificationCenter
from.eyeofcloud import Eyeofcloud
class EyeofcloudFactory:
	' Eyeofcloud factory to provides basic utility to instantiate the Eyeofcloud\n        SDK with a minimal number of configuration options.';max_event_batch_size=_A;max_event_flush_interval=_A;polling_interval=_A;blocking_timeout=_A
	@staticmethod
	def set_batch_size(batch_size):' Convenience method for setting the maximum number of events contained within a batch.\n        Args:\n          batch_size: Sets size of event_queue.\n         ';EyeofcloudFactory.max_event_batch_size=batch_size;return EyeofcloudFactory.max_event_batch_size
	@staticmethod
	def set_flush_interval(flush_interval):' Convenience method for setting the maximum time interval in milliseconds between event dispatches.\n        Args:\n          flush_interval: Time interval between event dispatches.\n         ';EyeofcloudFactory.max_event_flush_interval=flush_interval;return EyeofcloudFactory.max_event_flush_interval
	@staticmethod
	def set_polling_interval(polling_interval):' Method to set frequency at which datafile has to be polled.\n            Args:\n              polling_interval: Time in seconds after which to update datafile.\n        ';EyeofcloudFactory.polling_interval=polling_interval;return EyeofcloudFactory.polling_interval
	@staticmethod
	def set_blocking_timeout(blocking_timeout):' Method to set time in seconds to block the config call until config has been initialized.\n            Args:\n              blocking_timeout: Time in seconds to block the config call.\n       ';EyeofcloudFactory.blocking_timeout=blocking_timeout;return EyeofcloudFactory.blocking_timeout
	@staticmethod
	def default_instance(sdk_key,datafile=_A):' Returns a new eyeofcloud instance..\n          Args:\n            sdk_key:  Required string uniquely identifying the fallback datafile corresponding to project.\n            datafile: Optional JSON string datafile.\n        ';D=datafile;C=sdk_key;E=NoOpErrorHandler();A=eyeofcloud_logger.NoOpLogger();B=NotificationCenter(A);F={_B:C,_C:EyeofcloudFactory.polling_interval,_D:EyeofcloudFactory.blocking_timeout,_E:D,_F:A,_G:E,_H:B};G=PollingConfigManager(**F);H=BatchEventProcessor(event_dispatcher=EventDispatcher(),logger=A,batch_size=EyeofcloudFactory.max_event_batch_size,flush_interval=EyeofcloudFactory.max_event_flush_interval,notification_center=B);I=Eyeofcloud(D,_A,A,E,_A,_A,C,G,B,H);return I
	@staticmethod
	def default_instance_with_config_manager(config_manager):return Eyeofcloud(config_manager=config_manager)
	@staticmethod
	def custom_instance(sdk_key,datafile=_A,event_dispatcher=_A,logger=_A,error_handler=_A,skip_json_validation=_A,user_profile_service=_A,config_manager=_A,notification_center=_A):" Returns a new eyeofcloud instance.\n             if max_event_batch_size and max_event_flush_interval are None then default batch_size and flush_interval\n             will be used to setup BatchEventProcessor.\n\n             Args:\n               sdk_key: Required string uniquely identifying the fallback datafile corresponding to project.\n               datafile: Optional JSON string datafile.\n               event_dispatcher: Optional EventDispatcher interface provides a dispatch_event method which if given a\n                                 URL and params sends a request to it.\n               logger: Optional Logger interface provides a log method to log messages.\n                       By default nothing would be logged.\n               error_handler: Optional ErrorHandler interface which provides a handle_error method to handle exceptions.\n                              By default all exceptions will be suppressed.\n               skip_json_validation: Optional boolean param to skip JSON schema validation of the provided datafile.\n               user_profile_service: Optional UserProfileService interface provides methods to store and retrieve\n                                     user profiles.\n               config_manager: Optional ConfigManager interface responds to 'config' method.\n               notification_center: Optional Instance of NotificationCenter.\n        ";H=skip_json_validation;G=event_dispatcher;F=datafile;E=sdk_key;D=config_manager;C=error_handler;B=notification_center;A=logger;C=C or NoOpErrorHandler();A=A or eyeofcloud_logger.NoOpLogger();B=B if isinstance(B,NotificationCenter)else NotificationCenter(A);I=BatchEventProcessor(event_dispatcher=G or EventDispatcher(),logger=A,batch_size=EyeofcloudFactory.max_event_batch_size,flush_interval=EyeofcloudFactory.max_event_flush_interval,notification_center=B);J={_B:E,_C:EyeofcloudFactory.polling_interval,_D:EyeofcloudFactory.blocking_timeout,_E:F,_F:A,_G:C,'skip_json_validation':H,_H:B};D=D or PollingConfigManager(**J);return Eyeofcloud(F,G,A,C,H,user_profile_service,E,D,B,I)