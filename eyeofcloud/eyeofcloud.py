_T='Provided decide options is not an array. Using default decide options.'
_S='Feature "%s" is not enabled for user "%s".'
_R='Feature "%s" is enabled for user "%s".'
_Q='notification_center'
_P='error_handler'
_O='logger'
_N='decide'
_M='user_context'
_L='source_info'
_K='source'
_J='feature_enabled'
_I='Unable to cast value. Returning None.'
_H='Got variable value "%s" for variable "%s" of feature flag "%s".'
_G='variation_key'
_F='feature_key'
_E=True
_D='experiment_key'
_C='user_id'
_B=False
_A=None
from six import string_types
from.import decision_service
from.import entities
from.import event_builder
from.import exceptions
from.import logger as _logging
from.config_manager import AuthDatafilePollingConfigManager
from.config_manager import PollingConfigManager
from.config_manager import StaticConfigManager
from.decision.eyeofcloud_decide_option import EyeofcloudDecideOption
from.decision.eyeofcloud_decision import EyeofcloudDecision
from.decision.eyeofcloud_decision_message import EyeofcloudDecisionMessage
from.decision_service import Decision
from.error_handler import NoOpErrorHandler as noop_error_handler
from.event import event_factory,user_event_factory
from.event.event_processor import ForwardingEventProcessor
from.event_dispatcher import EventDispatcher as default_event_dispatcher
from.helpers import enums,validator
from.helpers.enums import DecisionSources
from.notification_center import NotificationCenter
from.eyeofcloud_config import EyeofcloudConfigService
from.eyeofcloud_user_context import EyeofcloudUserContext
class Eyeofcloud:
	' Class encapsulating all SDK functionality. '
	def __init__(A,datafile=_A,event_dispatcher=_A,logger=_A,error_handler=_A,skip_json_validation=_B,user_profile_service=_A,sdk_key=_A,config_manager=_A,notification_center=_A,event_processor=_A,datafile_access_token=_A,default_decide_options=_A):
		' Eyeofcloud init method for managing Custom projects.\n\n        Args:\n          datafile: Optional JSON string representing the project. Must provide at least one of datafile or sdk_key.\n          event_dispatcher: Provides a dispatch_event method which if given a URL and params sends a request to it.\n          logger: Optional component which provides a log method to log messages. By default nothing would be logged.\n          error_handler: Optional component which provides a handle_error method to handle exceptions.\n                         By default all exceptions will be suppressed.\n          skip_json_validation: Optional boolean param which allows skipping JSON schema validation upon object\n          invocation.\n                                By default JSON schema validation will be performed.\n          user_profile_service: Optional component which provides methods to store and manage user profiles.\n          sdk_key: Optional string uniquely identifying the datafile corresponding to project and environment\n          combination.\n                   Must provide at least one of datafile or sdk_key.\n          config_manager: Optional component which implements eyeofcloud.config_manager.BaseConfigManager.\n          notification_center: Optional instance of notification_center.NotificationCenter. Useful when providing own\n                               config_manager.BaseConfigManager implementation which can be using the\n                               same NotificationCenter instance.\n          event_processor: Optional component which processes the given event(s).\n                           By default eyeofcloud.event.event_processor.ForwardingEventProcessor is used\n                           which simply forwards events to the event dispatcher.\n                           To enable event batching configure and use\n                           eyeofcloud.event.event_processor.BatchEventProcessor.\n          datafile_access_token: Optional string used to fetch authenticated datafile for a secure project environment.\n          default_decide_options: Optional list of decide options used with the decide APIs.\n        ';E=default_decide_options;D=datafile_access_token;C=sdk_key;A.logger_name='.'.join([__name__,A.__class__.__name__]);A.is_valid=_E;A.event_dispatcher=event_dispatcher or default_event_dispatcher;A.logger=_logging.adapt_logger(logger or _logging.NoOpLogger());A.error_handler=error_handler or noop_error_handler;A.config_manager=config_manager;A.notification_center=notification_center or NotificationCenter(A.logger);A.event_processor=event_processor or ForwardingEventProcessor(A.event_dispatcher,logger=A.logger,notification_center=A.notification_center)
		if E is _A:A.default_decide_options=[]
		else:A.default_decide_options=E
		if isinstance(A.default_decide_options,list):A.default_decide_options=A.default_decide_options[:]
		else:A.logger.debug('Provided default decide options is not a list.');A.default_decide_options=[]
		try:A._validate_instantiation_options()
		except exceptions.InvalidInputException as F:A.is_valid=_B;A.logger=_logging.reset_logger(A.logger_name);A.logger.exception(str(F));return
		B={'datafile':datafile,_O:A.logger,_P:A.error_handler,_Q:A.notification_center,'skip_json_validation':skip_json_validation}
		if not A.config_manager:
			if C:
				B['sdk_key']=C
				if D:B['datafile_access_token']=D;A.config_manager=AuthDatafilePollingConfigManager(**B)
				else:A.config_manager=PollingConfigManager(**B)
			else:A.config_manager=StaticConfigManager(**B)
		A.event_builder=event_builder.EventBuilder();A.decision_service=decision_service.DecisionService(A.logger,user_profile_service)
	def _validate_instantiation_options(A):
		' Helper method to validate all instantiation parameters.\n\n        Raises:\n          Exception if provided instantiation options are valid.\n        '
		if A.config_manager and not validator.is_config_manager_valid(A.config_manager):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format('config_manager'))
		if not validator.is_event_dispatcher_valid(A.event_dispatcher):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format('event_dispatcher'))
		if not validator.is_logger_valid(A.logger):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format(_O))
		if not validator.is_error_handler_valid(A.error_handler):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format(_P))
		if not validator.is_notification_center_valid(A.notification_center):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format(_Q))
		if not validator.is_event_processor_valid(A.event_processor):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format('event_processor'))
	def _validate_user_inputs(A,attributes=_A,event_tags=_A):
		' Helper method to validate user inputs.\n\n        Args:\n          attributes: Dict representing user attributes.\n          event_tags: Dict representing metadata associated with an event.\n\n        Returns:\n          Boolean True if inputs are valid. False otherwise.\n\n        ';C=event_tags;B=attributes
		if B and not validator.are_attributes_valid(B):A.logger.error('Provided attributes are in an invalid format.');A.error_handler.handle_error(exceptions.InvalidAttributeException(enums.Errors.INVALID_ATTRIBUTE_FORMAT));return _B
		if C and not validator.are_event_tags_valid(C):A.logger.error('Provided event tags are in an invalid format.');A.error_handler.handle_error(exceptions.InvalidEventTagException(enums.Errors.INVALID_EVENT_TAG_FORMAT));return _B
		return _E
	def _send_impression_event(A,project_config,experiment,variation,flag_key,rule_key,rule_type,enabled,user_id,attributes):
		' Helper method to send impression event.\n\n        Args:\n          project_config: Instance of ProjectConfig.\n          experiment: Experiment for which impression event is being sent.\n          variation: Variation picked for user for the given experiment.\n          flag_key: key for a feature flag.\n          rule_key: key for an experiment.\n          rule_type: type for the source.\n          enabled: boolean representing if feature is enabled\n          user_id: ID for user.\n          attributes: Dict representing user attributes and values which need to be recorded.\n        ';E=attributes;D=user_id;C=variation;B=experiment
		if not B:B=entities.Experiment.get_default()
		G=C.id if C is not _A else _A;F=user_event_factory.UserEventFactory.create_impression_event(project_config,B,G,flag_key,rule_key,rule_type,enabled,D,E);A.event_processor.process(F)
		if len(A.notification_center.notification_listeners[enums.NotificationTypes.ACTIVATE])>0:H=event_factory.EventFactory.create_log_event(F,A.logger);A.notification_center.send_notifications(enums.NotificationTypes.ACTIVATE,B,D,E,C,H.__dict__)
	def _get_feature_variable_for_type(A,project_config,feature_key,variable_key,variable_type,user_id,attributes):
		" Helper method to determine value for a certain variable attached to a feature flag based on type of variable.\n\n        Args:\n          project_config: Instance of ProjectConfig.\n          feature_key: Key of the feature whose variable's value is being accessed.\n          variable_key: Key of the variable whose value is to be accessed.\n          variable_type: Type of variable which could be one of boolean/double/integer/string.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Value of the variable. None if:\n          - Feature key is invalid.\n          - Variable key is invalid.\n          - Mismatch with type of variable.\n        ";O='variable_key';J=attributes;H=user_id;G=variable_key;F=project_config;D=variable_type;B=feature_key
		if not validator.is_non_empty_string(B):A.logger.error(enums.Errors.INVALID_INPUT.format(_F));return
		if not validator.is_non_empty_string(G):A.logger.error(enums.Errors.INVALID_INPUT.format(O));return
		if not isinstance(H,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return
		if not A._validate_user_inputs(J):return
		M=F.get_feature_from_key(B)
		if not M:return
		E=F.get_variable_for_feature(B,G)
		if not E:return
		D=D or E.type
		if E.type!=D:A.logger.warning('Requested variable type "%s", but variable is of type "%s". Use correct API to retrieve value. Returning None.'%(D,E.type));return
		K=_B;N={};I=E.defaultValue;P=A.create_user_context(H,J);C,Q=A.decision_service.get_variation_for_feature(F,M,P)
		if C.variation:
			K=C.variation.featureEnabled
			if K:I=F.get_variable_value_for_variation(E,C.variation);A.logger.info(_H%(I,G,B))
			else:A.logger.info('Feature "%s" is not enabled for user "%s". Returning the default variable value "%s".'%(B,H,I))
		else:A.logger.info('User "%s" is not in any variation or rollout rule. Returning default value for variable "%s" of feature flag "%s".'%(H,G,B))
		if C.source==enums.DecisionSources.FEATURE_TEST:N={_D:C.experiment.key,_G:C.variation.key}
		try:L=F.get_typecast_value(I,D)
		except:A.logger.error(_I);L=_A
		A.notification_center.send_notifications(enums.NotificationTypes.DECISION,enums.DecisionNotificationTypes.FEATURE_VARIABLE,H,J or{},{_F:B,_J:K,_K:C.source,O:G,'variable_value':L,'variable_type':D,_L:N});return L
	def _get_all_feature_variables_for_type(A,project_config,feature_key,user_id,attributes):
		" Helper method to determine value for all variables attached to a feature flag.\n\n        Args:\n          project_config: Instance of ProjectConfig.\n          feature_key: Key of the feature whose variable's value is being accessed.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Dictionary of all variables. None if:\n          - Feature key is invalid.\n        ";G=attributes;E=project_config;D=user_id;B=feature_key
		if not validator.is_non_empty_string(B):A.logger.error(enums.Errors.INVALID_INPUT.format(_F));return
		if not isinstance(D,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return
		if not A._validate_user_inputs(G):return
		H=E.get_feature_from_key(B)
		if not H:return
		F=_B;M={};O=A.create_user_context(D,G);C,P=A.decision_service.get_variation_for_feature(E,H,O)
		if C.variation:
			F=C.variation.featureEnabled
			if F:A.logger.info(_R%(B,D))
			else:A.logger.info(_S%(B,D))
		else:A.logger.info('User "%s" is not in any variation or rollout rule. Returning default value for all variables of feature flag "%s".'%(D,B))
		I={}
		for J in H.variables:
			K=E.get_variable_for_feature(B,J);L=K.defaultValue
			if F:L=E.get_variable_value_for_variation(K,C.variation);A.logger.debug(_H%(L,J,B))
			try:N=E.get_typecast_value(L,K.type)
			except:A.logger.error(_I);N=_A
			I[J]=N
		if C.source==enums.DecisionSources.FEATURE_TEST:M={_D:C.experiment.key,_G:C.variation.key}
		A.notification_center.send_notifications(enums.NotificationTypes.DECISION,enums.DecisionNotificationTypes.ALL_FEATURE_VARIABLES,D,G or{},{_F:B,_J:F,'variable_values':I,_K:C.source,_L:M});return I
	def activate(A,experiment_key,user_id,attributes=_A):
		' Buckets visitor and sends impression event to Eyeofcloud.\n\n        Args:\n          experiment_key: Experiment which needs to be activated.\n          user_id: ID for user.\n          attributes: Dict representing user attributes and values which need to be recorded.\n\n        Returns:\n          Variation key representing the variation the user will be bucketed in.\n          None if user is not in experiment or if experiment is not Running.\n        ';I='activate';F=attributes;C=experiment_key;B=user_id
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(I));return
		if not validator.is_non_empty_string(C):A.logger.error(enums.Errors.INVALID_INPUT.format(_D));return
		if not isinstance(B,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return
		D=A.config_manager.get_config()
		if not D:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(I));return
		G=A.get_variation(C,B,F)
		if not G:A.logger.info('Not activating user "%s".'%B);return
		E=D.get_experiment_from_key(C);H=D.get_variation_from_key(C,G);A.logger.info('Activating user "%s" in experiment "%s".'%(B,E.key));A._send_impression_event(D,E,H,'',E.key,enums.DecisionSources.EXPERIMENT,_E,B,F);return H.key
	def track(A,event_key,user_id,attributes=_A,event_tags=_A):
		' Send conversion event to Eyeofcloud.\n\n        Args:\n          event_key: Event key representing the event which needs to be recorded.\n          user_id: ID for user.\n          attributes: Dict representing visitor attributes and values which need to be recorded.\n          event_tags: Dict representing metadata associated with the event.\n        ';H='track';E=event_tags;D=attributes;C=user_id;B=event_key
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(H));return
		if not validator.is_non_empty_string(B):A.logger.error(enums.Errors.INVALID_INPUT.format('event_key'));return
		if not isinstance(C,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return
		if not A._validate_user_inputs(D,E):return
		F=A.config_manager.get_config()
		if not F:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(H));return
		I=F.get_event(B)
		if not I:A.logger.info('Not tracking user "%s" for event "%s".'%(C,B));return
		G=user_event_factory.UserEventFactory.create_conversion_event(F,B,C,D,E);A.event_processor.process(G);A.logger.info('Tracking event "%s" for user "%s".'%(B,C))
		if len(A.notification_center.notification_listeners[enums.NotificationTypes.TRACK])>0:J=event_factory.EventFactory.create_log_event(G,A.logger);A.notification_center.send_notifications(enums.NotificationTypes.TRACK,B,C,D,E,J.__dict__)
	def get_variation(A,experiment_key,user_id,attributes=_A):
		' Gets variation where user will be bucketed.\n\n        Args:\n          experiment_key: Experiment for which user variation needs to be determined.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Variation key representing the variation the user will be bucketed in.\n          None if user is not in experiment or if experiment is not Running.\n        ';J='get_variation';E=attributes;C=user_id;B=experiment_key
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(J));return
		if not validator.is_non_empty_string(B):A.logger.error(enums.Errors.INVALID_INPUT.format(_D));return
		if not isinstance(C,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return
		D=A.config_manager.get_config()
		if not D:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(J));return
		F=D.get_experiment_from_key(B);G=_A
		if not F:A.logger.info('Experiment key "%s" is invalid. Not activating user "%s".'%(B,C));return
		if not A._validate_user_inputs(E):return
		K=A.create_user_context(C,E);H,L=A.decision_service.get_variation(D,F,K)
		if H:G=H.key
		if D.is_feature_experiment(F.id):I=enums.DecisionNotificationTypes.FEATURE_TEST
		else:I=enums.DecisionNotificationTypes.AB_TEST
		A.notification_center.send_notifications(enums.NotificationTypes.DECISION,I,C,E or{},{_D:B,_G:G});return G
	def is_feature_enabled(B,feature_key,user_id,attributes=_A):
		' Returns true if the feature is enabled for the given user.\n\n        Args:\n          feature_key: The key of the feature for which we are determining if it is enabled or not for the given user.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          True if the feature is enabled for the user. False otherwise.\n        ';J='is_feature_enabled';G=attributes;F=feature_key;C=user_id
		if not B.is_valid:B.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(J));return _B
		if not validator.is_non_empty_string(F):B.logger.error(enums.Errors.INVALID_INPUT.format(_F));return _B
		if not isinstance(C,string_types):B.logger.error(enums.Errors.INVALID_INPUT.format(_C));return _B
		if not B._validate_user_inputs(G):return _B
		D=B.config_manager.get_config()
		if not D:B.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(J));return _B
		H=D.get_feature_from_key(F)
		if not H:return _B
		E=_B;I={};K=B.create_user_context(C,G);A,N=B.decision_service.get_variation_for_feature(D,H,K);L=A.source==enums.DecisionSources.FEATURE_TEST;M=A.source==enums.DecisionSources.ROLLOUT
		if A.variation:
			if A.variation.featureEnabled is _E:E=_E
		if(M or not A.variation)and D.get_send_flag_decisions_value():B._send_impression_event(D,A.experiment,A.variation,H.key,A.experiment.key if A.experiment else'',A.source,E,C,G)
		if L and A.variation:I={_D:A.experiment.key,_G:A.variation.key};B._send_impression_event(D,A.experiment,A.variation,H.key,A.experiment.key,A.source,E,C,G)
		if E:B.logger.info(_R%(F,C))
		else:B.logger.info(_S%(F,C))
		B.notification_center.send_notifications(enums.NotificationTypes.DECISION,enums.DecisionNotificationTypes.FEATURE,C,G or{},{_F:F,_J:E,_K:A.source,_L:I});return E
	def get_enabled_features(A,user_id,attributes=_A):
		' Returns the list of features that are enabled for the user.\n\n        Args:\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          A list of the keys of the features that are enabled for the user.\n        ';G='get_enabled_features';D=attributes;C=user_id;B=[]
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(G));return B
		if not isinstance(C,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return B
		if not A._validate_user_inputs(D):return B
		E=A.config_manager.get_config()
		if not E:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(G));return B
		for F in E.feature_key_map.values():
			if A.is_feature_enabled(F.key,C,D):B.append(F.key)
		return B
	def get_feature_variable(A,feature_key,variable_key,user_id,attributes=_A):
		" Returns value for a variable attached to a feature flag.\n\n        Args:\n          feature_key: Key of the feature whose variable's value is being accessed.\n          variable_key: Key of the variable whose value is to be accessed.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Value of the variable. None if:\n          - Feature key is invalid.\n          - Variable key is invalid.\n        ";B=A.config_manager.get_config()
		if not B:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format('get_feature_variable'));return
		return A._get_feature_variable_for_type(B,feature_key,variable_key,_A,user_id,attributes)
	def get_feature_variable_boolean(A,feature_key,variable_key,user_id,attributes=_A):
		" Returns value for a certain boolean variable attached to a feature flag.\n\n        Args:\n          feature_key: Key of the feature whose variable's value is being accessed.\n          variable_key: Key of the variable whose value is to be accessed.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Boolean value of the variable. None if:\n          - Feature key is invalid.\n          - Variable key is invalid.\n          - Mismatch with type of variable.\n        ";C=entities.Variable.Type.BOOLEAN;B=A.config_manager.get_config()
		if not B:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format('get_feature_variable_boolean'));return
		return A._get_feature_variable_for_type(B,feature_key,variable_key,C,user_id,attributes)
	def get_feature_variable_double(A,feature_key,variable_key,user_id,attributes=_A):
		" Returns value for a certain double variable attached to a feature flag.\n\n        Args:\n          feature_key: Key of the feature whose variable's value is being accessed.\n          variable_key: Key of the variable whose value is to be accessed.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Double value of the variable. None if:\n          - Feature key is invalid.\n          - Variable key is invalid.\n          - Mismatch with type of variable.\n        ";C=entities.Variable.Type.DOUBLE;B=A.config_manager.get_config()
		if not B:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format('get_feature_variable_double'));return
		return A._get_feature_variable_for_type(B,feature_key,variable_key,C,user_id,attributes)
	def get_feature_variable_integer(A,feature_key,variable_key,user_id,attributes=_A):
		" Returns value for a certain integer variable attached to a feature flag.\n\n        Args:\n          feature_key: Key of the feature whose variable's value is being accessed.\n          variable_key: Key of the variable whose value is to be accessed.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Integer value of the variable. None if:\n          - Feature key is invalid.\n          - Variable key is invalid.\n          - Mismatch with type of variable.\n        ";C=entities.Variable.Type.INTEGER;B=A.config_manager.get_config()
		if not B:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format('get_feature_variable_integer'));return
		return A._get_feature_variable_for_type(B,feature_key,variable_key,C,user_id,attributes)
	def get_feature_variable_string(A,feature_key,variable_key,user_id,attributes=_A):
		" Returns value for a certain string variable attached to a feature.\n\n        Args:\n          feature_key: Key of the feature whose variable's value is being accessed.\n          variable_key: Key of the variable whose value is to be accessed.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          String value of the variable. None if:\n          - Feature key is invalid.\n          - Variable key is invalid.\n          - Mismatch with type of variable.\n        ";C=entities.Variable.Type.STRING;B=A.config_manager.get_config()
		if not B:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format('get_feature_variable_string'));return
		return A._get_feature_variable_for_type(B,feature_key,variable_key,C,user_id,attributes)
	def get_feature_variable_json(A,feature_key,variable_key,user_id,attributes=_A):
		" Returns value for a certain JSON variable attached to a feature.\n\n        Args:\n          feature_key: Key of the feature whose variable's value is being accessed.\n          variable_key: Key of the variable whose value is to be accessed.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Dictionary object of the variable. None if:\n          - Feature key is invalid.\n          - Variable key is invalid.\n          - Mismatch with type of variable.\n        ";C=entities.Variable.Type.JSON;B=A.config_manager.get_config()
		if not B:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format('get_feature_variable_json'));return
		return A._get_feature_variable_for_type(B,feature_key,variable_key,C,user_id,attributes)
	def get_all_feature_variables(A,feature_key,user_id,attributes=_A):
		" Returns dictionary of all variables and their corresponding values in the context of a feature.\n\n        Args:\n          feature_key: Key of the feature whose variable's value is being accessed.\n          user_id: ID for user.\n          attributes: Dict representing user attributes.\n\n        Returns:\n          Dictionary mapping variable key to variable value. None if:\n          - Feature key is invalid.\n        ";B=A.config_manager.get_config()
		if not B:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format('get_all_feature_variables'));return
		return A._get_all_feature_variables_for_type(B,feature_key,user_id,attributes)
	def set_forced_variation(A,experiment_key,user_id,variation_key):
		' Force a user into a variation for a given experiment.\n\n        Args:\n         experiment_key: A string key identifying the experiment.\n         user_id: The user ID.\n         variation_key: A string variation key that specifies the variation which the user.\n         will be forced into. If null, then clear the existing experiment-to-variation mapping.\n\n        Returns:\n          A boolean value that indicates if the set completed successfully.\n        ';E='set_forced_variation';C=user_id;B=experiment_key
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(E));return _B
		if not validator.is_non_empty_string(B):A.logger.error(enums.Errors.INVALID_INPUT.format(_D));return _B
		if not isinstance(C,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return _B
		D=A.config_manager.get_config()
		if not D:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(E));return _B
		return A.decision_service.set_forced_variation(D,B,C,variation_key)
	def get_forced_variation(A,experiment_key,user_id):
		' Gets the forced variation for a given user and experiment.\n\n        Args:\n          experiment_key: A string key identifying the experiment.\n          user_id: The user ID.\n\n        Returns:\n          The forced variation key. None if no forced variation key.\n        ';F='get_forced_variation';C=user_id;B=experiment_key
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(F));return
		if not validator.is_non_empty_string(B):A.logger.error(enums.Errors.INVALID_INPUT.format(_D));return
		if not isinstance(C,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return
		D=A.config_manager.get_config()
		if not D:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(F));return
		E,G=A.decision_service.get_forced_variation(D,B,C);return E.key if E else _A
	def get_eyeofcloud_config(A):
		" Gets EyeofcloudConfig instance for the current project config.\n\n        Returns:\n            EyeofcloudConfig instance. None if the eyeofcloud instance is invalid or\n            project config isn't available.\n        ";C='get_eyeofcloud_config'
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(C));return
		B=A.config_manager.get_config()
		if not B:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(C));return
		if hasattr(A.config_manager,'eyeofcloud_config'):return A.config_manager.eyeofcloud_config
		return EyeofcloudConfigService(B).get_config()
	def create_user_context(A,user_id,attributes=_A):
		'\n        We do not check for is_valid here as a user context can be created successfully\n        even when the SDK is not fully configured.\n\n        Args:\n            user_id: string to use as user id for user context\n            attributes: dictionary of attributes or None\n\n        Returns:\n            UserContext instance or None if the user id or attributes are invalid.\n        ';C=user_id;B=attributes
		if not isinstance(C,string_types):A.logger.error(enums.Errors.INVALID_INPUT.format(_C));return
		if B is not _A and type(B)is not dict:A.logger.error(enums.Errors.INVALID_INPUT.format('attributes'));return
		return EyeofcloudUserContext(A,A.logger,C,B)
	def _decide(A,user_context,key,decide_options=_A):
		'\n        decide calls eyeofcloud decide with feature key provided\n        Args:\n            user_context: UserContent with userid and attributes\n            key: feature key\n            decide_options: list of EyeofcloudDecideOption\n\n        Returns:\n            Decision object\n        ';G=decide_options;D=key;C=user_context
		if not isinstance(C,EyeofcloudUserContext):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format(_M))
		B=[]
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format(_N));B.append(EyeofcloudDecisionMessage.SDK_NOT_READY);return EyeofcloudDecision(flag_key=D,user_context=C,reasons=B)
		if not isinstance(D,string_types):A.logger.error('Key parameter is invalid');B.append(EyeofcloudDecisionMessage.FLAG_KEY_INVALID.format(D));return EyeofcloudDecision(flag_key=D,user_context=C,reasons=B)
		E=A.config_manager.get_config()
		if not E:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(_N));B.append(EyeofcloudDecisionMessage.SDK_NOT_READY);return EyeofcloudDecision(flag_key=D,user_context=C,reasons=B)
		M=E.get_feature_from_key(D)
		if M is _A:A.logger.error("No feature flag was found for key '#{key}'.");B.append(EyeofcloudDecisionMessage.FLAG_KEY_INVALID.format(D));return EyeofcloudDecision(flag_key=D,user_context=C,reasons=B)
		if isinstance(G,list):G+=A.default_decide_options
		else:A.logger.debug(_T);G=A.default_decide_options
		U=C.user_id;V=C.get_user_attributes();N=_A;F=_A;I=_B;J=_A;K=D;O={};L=_A;P=DecisionSources.ROLLOUT;W={};X=_B;a=EyeofcloudUserContext.EyeofcloudDecisionContext(flag_key=D,rule_key=J);b=A.decision_service.validated_forced_decision(E,a,C);F,Q=b;B+=Q
		if F:H=Decision(_A,F,enums.DecisionSources.FEATURE_TEST)
		else:H,Q=A.decision_service.get_variation_for_feature(E,M,C,G);B+=Q
		if H.experiment is not _A:L=H.experiment;W['experiment']=L;J=L.key if L else _A
		if H.variation is not _A:F=H.variation;N=F.key;I=F.featureEnabled;P=H.source;W['variation']=F
		if EyeofcloudDecideOption.DISABLE_DECISION_EVENT not in G:
			if P==DecisionSources.FEATURE_TEST or E.send_flag_decisions:A._send_impression_event(E,L,F,K,J or'',P,I,U,V);X=_E
		if EyeofcloudDecideOption.EXCLUDE_VARIABLES not in G:
			for R in M.variables:
				S=E.get_variable_for_feature(K,R);T=S.defaultValue
				if I:T=E.get_variable_value_for_variation(S,H.variation);A.logger.debug(_H%(T,R,K))
				try:Y=E.get_typecast_value(T,S.type)
				except:A.logger.error(_I);Y=_A
				O[R]=Y
		Z=EyeofcloudDecideOption.INCLUDE_REASONS in G;A.notification_center.send_notifications(enums.NotificationTypes.DECISION,enums.DecisionNotificationTypes.FLAG,U,V or{},{'flag_key':K,'enabled':I,'variables':O,_G:N,'rule_key':J,'reasons':B if Z else[],'decision_event_dispatched':X});return EyeofcloudDecision(variation_key=N,enabled=I,variables=O,rule_key=J,flag_key=K,user_context=C,reasons=B if Z else[])
	def _decide_all(A,user_context,decide_options=_A):
		'\n        decide_all will return a decision for every feature key in the current config\n        Args:\n            user_context: UserContent object\n            decide_options: Array of DecisionOption\n\n        Returns:\n            A dictionary of feature key to Decision\n        ';B=user_context
		if not isinstance(B,EyeofcloudUserContext):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format(_M))
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format('decide_all'));return{}
		C=A.config_manager.get_config()
		if not C:A.logger.error(enums.Errors.INVALID_PROJECT_CONFIG.format(_N));return{}
		D=[]
		for E in C.feature_flags:D.append(E['key'])
		return A._decide_for_keys(B,D,decide_options)
	def _decide_for_keys(A,user_context,keys,decide_options=_A):
		'\n        Args:\n            user_context: UserContent\n            keys: list of feature keys to run decide on.\n            decide_options: an array of DecisionOption objects\n\n        Returns:\n            An dictionary of feature key to Decision\n        ';D=user_context;C=decide_options
		if not isinstance(D,EyeofcloudUserContext):raise exceptions.InvalidInputException(enums.Errors.INVALID_INPUT.format(_M))
		if not A.is_valid:A.logger.error(enums.Errors.INVALID_OPTIMIZELY.format('decide_for_keys'));return{}
		B=[]
		if isinstance(C,list):B=C[:];B+=A.default_decide_options
		else:A.logger.debug(_T);B=A.default_decide_options
		H=EyeofcloudDecideOption.ENABLED_FLAGS_ONLY in B;E={}
		for F in keys:
			G=A._decide(D,F,C)
			if H and not G.enabled:continue
			E[F]=G
		return E