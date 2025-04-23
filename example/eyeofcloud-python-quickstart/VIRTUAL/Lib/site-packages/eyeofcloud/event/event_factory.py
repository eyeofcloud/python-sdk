import os
from eyeofcloud.helpers import enums,event_tag_utils,validator
from.import log_event
from.import payload
from.import user_event
CUSTOM_ATTRIBUTE_FEATURE_TYPE='custom'
class EventFactory:
	' EventFactory builds LogEvent object from a given UserEvent.\n  This class serves to separate concerns between events in the SDK and the API used\n  to record the events via the Eyeofcloud Events API ("https://developers.eyeofcloud.com/x/events/api/index.html")\n  ';EVENT_ENDPOINT=os.environ.get('EYEOFCLOUD_EVENT_URL','https://event.eyeofcloud.com/v1/events');HTTP_VERB='POST';HTTP_HEADERS={'Content-Type':'application/json'};ACTIVATE_EVENT_KEY='campaign_activated'
	@classmethod
	def create_log_event(C,user_events,logger):
		' Create LogEvent instance.\n\n    Args:\n      user_events: A single UserEvent instance or a list of UserEvent instances.\n      logger: Provides a logger instance.\n\n    Returns:\n      LogEvent instance.\n    ';B=user_events
		if not isinstance(B,list):B=[B]
		D=[]
		for G in B:
			E=C._create_visitor(G,logger)
			if E:D.append(E)
		if len(D)==0:return
		A=B[0].event_context;F=payload.EventBatch(A.account_id,A.project_id,A.revision,A.client_name,A.client_version,A.anonymize_ip,True);F.visitors=D;H=F.get_event_params();return log_event.LogEvent(C.EVENT_ENDPOINT,H,C.HTTP_VERB,C.HTTP_HEADERS)
	@classmethod
	def _create_visitor(J,event,logger):
		' Helper method to create Visitor instance for event_batch.\n\n    Args:\n      event: Instance of UserEvent.\n      logger: Provides a logger instance.\n\n    Returns:\n      Instance of Visitor. None if:\n      - event is invalid.\n    ';F=logger;A=event
		if isinstance(A,user_event.ImpressionEvent):
			B,G,H,I='','','',''
			if A.variation:H=A.variation.id;I=A.variation.key
			if A.experiment:B=A.experiment.layerId;G=A.experiment.id
			K=payload.Metadata(A.flag_key,A.rule_key,A.rule_type,I,A.enabled);L=payload.Decision(B,G,H,K);C=payload.SnapshotEvent(B,A.uuid,J.ACTIVATE_EVENT_KEY,A.timestamp);D=payload.Snapshot([C],[L]);E=payload.Visitor([D],A.visitor_attributes,A.user_id);return E
		elif isinstance(A,user_event.ConversionEvent):M=event_tag_utils.get_revenue_value(A.event_tags);N=event_tag_utils.get_numeric_value(A.event_tags,F);C=payload.SnapshotEvent(A.event.id,A.uuid,A.event.key,A.timestamp,M,N,A.event_tags);D=payload.Snapshot([C]);E=payload.Visitor([D],A.visitor_attributes,A.user_id);return E
		else:F.error('Invalid user event.');return
	@staticmethod
	def build_attribute_list(attributes,project_config):
		' Create Vistor Attribute List.\n\n    Args:\n      attributes: Dict representing user attributes and values which need to be recorded or None.\n      project_config: Instance of ProjectConfig.\n\n    Returns:\n      List consisting of valid attributes for the user. Empty otherwise.\n    ';D=project_config;C=attributes;A=[]
		if D is None:return A
		if isinstance(C,dict):
			for B in C.keys():
				E=C.get(B)
				if validator.is_attribute_valid(B,E):
					F=D.get_attribute_id(B)
					if F:A.append(payload.VisitorAttribute(F,B,CUSTOM_ATTRIBUTE_FEATURE_TYPE,E))
		G=D.get_bot_filtering_value()
		if isinstance(G,bool):A.append(payload.VisitorAttribute(enums.ControlAttributes.BOT_FILTERING,enums.ControlAttributes.BOT_FILTERING,CUSTOM_ATTRIBUTE_FEATURE_TYPE,G))
		return A