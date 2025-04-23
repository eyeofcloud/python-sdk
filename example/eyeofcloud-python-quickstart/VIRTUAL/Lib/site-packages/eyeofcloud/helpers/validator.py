_B=True
_A=False
import json,jsonschema,math,numbers
from six import string_types
from eyeofcloud.notification_center import NotificationCenter
from eyeofcloud.user_profile import UserProfile
from.import constants
def is_datafile_valid(datafile):
	' Given a datafile determine if it is valid or not.\n\n  Args:\n    datafile: JSON string representing the project.\n\n  Returns:\n    Boolean depending upon whether datafile is valid or not.\n  '
	try:A=json.loads(datafile)
	except:return _A
	try:jsonschema.Draft4Validator(constants.JSON_SCHEMA).validate(A)
	except:return _A
	return _B
def _has_method(obj,method):' Given an object determine if it supports the method.\n\n  Args:\n    obj: Object which needs to be inspected.\n    method: Method whose presence needs to be determined.\n\n  Returns:\n    Boolean depending upon whether the method is available or not.\n  ';return getattr(obj,method,None)is not None
def is_config_manager_valid(config_manager):' Given a config_manager determine if it is valid or not i.e. provides a get_config method.\n\n  Args:\n    config_manager: Provides a get_config method to handle exceptions.\n\n  Returns:\n    Boolean depending upon whether config_manager is valid or not.\n  ';return _has_method(config_manager,'get_config')
def is_event_processor_valid(event_processor):' Given an event_processor, determine if it is valid or not i.e. provides a process method.\n\n  Args:\n    event_processor: Provides a process method to create user events and then send requests.\n\n  Returns:\n    Boolean depending upon whether event_processor is valid or not.\n  ';return _has_method(event_processor,'process')
def is_error_handler_valid(error_handler):' Given a error_handler determine if it is valid or not i.e. provides a handle_error method.\n\n  Args:\n    error_handler: Provides a handle_error method to handle exceptions.\n\n  Returns:\n    Boolean depending upon whether error_handler is valid or not.\n  ';return _has_method(error_handler,'handle_error')
def is_event_dispatcher_valid(event_dispatcher):' Given a event_dispatcher determine if it is valid or not i.e. provides a dispatch_event method.\n\n  Args:\n    event_dispatcher: Provides a dispatch_event method to send requests.\n\n  Returns:\n    Boolean depending upon whether event_dispatcher is valid or not.\n  ';return _has_method(event_dispatcher,'dispatch_event')
def is_logger_valid(logger):' Given a logger determine if it is valid or not i.e. provides a log method.\n\n  Args:\n    logger: Provides a log method to log messages.\n\n  Returns:\n    Boolean depending upon whether logger is valid or not.\n  ';return _has_method(logger,'log')
def is_notification_center_valid(notification_center):' Given notification_center determine if it is valid or not.\n\n  Args:\n    notification_center: Instance of notification_center.NotificationCenter\n\n  Returns:\n    Boolean denoting instance is valid or not.\n  ';return isinstance(notification_center,NotificationCenter)
def are_attributes_valid(attributes):' Determine if attributes provided are dict or not.\n\n  Args:\n    attributes: User attributes which need to be validated.\n\n  Returns:\n    Boolean depending upon whether attributes are in valid format or not.\n  ';return type(attributes)is dict
def are_event_tags_valid(event_tags):' Determine if event tags provided are dict or not.\n\n  Args:\n    event_tags: Event tags which need to be validated.\n\n  Returns:\n    Boolean depending upon whether event_tags are in valid format or not.\n  ';return type(event_tags)is dict
def is_user_profile_valid(user_profile):
	" Determine if provided user profile is valid or not.\n\n  Args:\n    user_profile: User's profile which needs to be validated.\n\n  Returns:\n    Boolean depending upon whether profile is valid or not.\n  ";A=user_profile
	if not A:return _A
	if not type(A)is dict:return _A
	if UserProfile.USER_ID_KEY not in A:return _A
	if UserProfile.EXPERIMENT_BUCKET_MAP_KEY not in A:return _A
	B=A.get(UserProfile.EXPERIMENT_BUCKET_MAP_KEY)
	if not type(B)is dict:return _A
	for C in B.values():
		if type(C)is not dict or UserProfile.VARIATION_ID_KEY not in C:return _A
	return _B
def is_non_empty_string(input_id_key):
	' Determine if provided input_id_key is a non-empty string or not.\n\n  Args:\n    input_id_key: Variable which needs to be validated.\n\n  Returns:\n    Boolean depending upon whether input is valid or not.\n  ';A=input_id_key
	if A and isinstance(A,string_types):return _B
	return _A
def is_attribute_valid(attribute_key,attribute_value):
	' Determine if given attribute is valid.\n\n  Args:\n    attribute_key: Variable which needs to be validated\n    attribute_value: Variable which needs to be validated\n\n  Returns:\n    False if attribute_key is not a string\n    False if attribute_value is not one of the supported attribute types\n    True otherwise\n  ';A=attribute_value
	if not isinstance(attribute_key,string_types):return _A
	if isinstance(A,(string_types,bool)):return _B
	if isinstance(A,(numbers.Integral,float)):return is_finite_number(A)
	return _A
def is_finite_number(value):
	' Validates if the given value is a number, enforces\n   absolute limit of 2^53 and restricts NAN, INF, -INF.\n\n  Args:\n    value: Value to be validated.\n\n  Returns:\n    Boolean: True if value is a number and not NAN, INF, -INF or\n             greater than absolute limit of 2^53 else False.\n  ';A=value
	if not isinstance(A,(numbers.Integral,float)):return _A
	if isinstance(A,bool):return _A
	if isinstance(A,float):
		if math.isnan(A)or math.isinf(A):return _A
	if abs(A)>2**53:return _A
	return _B
def are_values_same_type(first_val,second_val):
	' Method to verify that both values belong to same type. Float and integer are\n  considered as same type.\n\n  Args:\n    first_val: Value to validate.\n    second_val: Value to validate.\n\n  Returns:\n    Boolean: True if both values belong to same type. Otherwise False.\n  ';B=second_val;A=first_val;C=type(A);D=type(B)
	if isinstance(A,string_types)and isinstance(B,string_types):return _B
	if isinstance(A,bool)or isinstance(B,bool):return C==D
	if isinstance(A,(numbers.Integral,float))and isinstance(B,(numbers.Integral,float)):return _B
	return _A