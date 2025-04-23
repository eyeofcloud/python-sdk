import time,uuid
from eyeofcloud import version
CLIENT_NAME='python-sdk'
class UserEvent:
	' Class respresenting User Event. '
	def __init__(A,event_context,user_id,visitor_attributes,bot_filtering=None):A.event_context=event_context;A.user_id=user_id;A.visitor_attributes=visitor_attributes;A.bot_filtering=bot_filtering;A.uuid=A._get_uuid();A.timestamp=A._get_time()
	def _get_time(A):return int(round(time.time()*1000))
	def _get_uuid(A):return str(uuid.uuid4())
class ImpressionEvent(UserEvent):
	' Class representing Impression Event. '
	def __init__(A,event_context,user_id,experiment,visitor_attributes,variation,flag_key,rule_key,rule_type,enabled,bot_filtering=None):super(ImpressionEvent,A).__init__(event_context,user_id,visitor_attributes,bot_filtering);A.experiment=experiment;A.variation=variation;A.flag_key=flag_key;A.rule_key=rule_key;A.rule_type=rule_type;A.enabled=enabled
class ConversionEvent(UserEvent):
	' Class representing Conversion Event. '
	def __init__(A,event_context,event,user_id,visitor_attributes,event_tags,bot_filtering=None):super(ConversionEvent,A).__init__(event_context,user_id,visitor_attributes,bot_filtering);A.event=event;A.event_tags=event_tags
class EventContext:
	' Class respresenting User Event Context. '
	def __init__(A,account_id,project_id,revision,anonymize_ip):A.account_id=account_id;A.project_id=project_id;A.revision=revision;A.client_name=CLIENT_NAME;A.client_version=version.__version__;A.anonymize_ip=anonymize_ip