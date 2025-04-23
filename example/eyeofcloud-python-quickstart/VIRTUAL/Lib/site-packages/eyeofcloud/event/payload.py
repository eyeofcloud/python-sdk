_A=None
import json
class EventBatch:
	' Class respresenting Event Batch. '
	def __init__(A,account_id,project_id,revision,client_name,client_version,anonymize_ip,enrich_decisions=True,visitors=_A):A.account_id=account_id;A.project_id=project_id;A.revision=revision;A.client_name=client_name;A.client_version=client_version;A.anonymize_ip=anonymize_ip;A.enrich_decisions=enrich_decisions;A.visitors=visitors or[]
	def __eq__(A,other):B=A.get_event_params();return B==other
	def _dict_clean(D,obj):
		' Helper method to remove keys from dictionary with None values. ';A={}
		for(B,C)in obj:
			if C is _A and B in['revenue','value','tags','decisions']:continue
			else:A[B]=C
		return A
	def get_event_params(A):' Method to return valid params for LogEvent payload. ';return json.loads(json.dumps(A.__dict__,default=lambda o:o.__dict__),object_pairs_hook=A._dict_clean)
class Decision:
	' Class respresenting Decision. '
	def __init__(A,campaign_id,experiment_id,variation_id,metadata):A.campaign_id=campaign_id;A.experiment_id=experiment_id;A.variation_id=variation_id;A.metadata=metadata
class Metadata:
	' Class respresenting Metadata. '
	def __init__(A,flag_key,rule_key,rule_type,variation_key,enabled):A.flag_key=flag_key;A.rule_key=rule_key;A.rule_type=rule_type;A.variation_key=variation_key;A.enabled=enabled
class Snapshot:
	' Class representing Snapshot. '
	def __init__(A,events,decisions=_A):A.events=events;A.decisions=decisions
class SnapshotEvent:
	' Class representing Snapshot Event. '
	def __init__(A,entity_id,uuid,key,timestamp,revenue=_A,value=_A,tags=_A):A.entity_id=entity_id;A.uuid=uuid;A.key=key;A.timestamp=timestamp;A.revenue=revenue;A.value=value;A.tags=tags
class Visitor:
	' Class representing Visitor. '
	def __init__(A,snapshots,attributes,visitor_id):A.snapshots=snapshots;A.attributes=attributes;A.visitor_id=visitor_id
class VisitorAttribute:
	' Class representing Visitor Attribute. '
	def __init__(A,entity_id,key,attribute_type,value):A.entity_id=entity_id;A.key=key;A.type=attribute_type;A.value=value