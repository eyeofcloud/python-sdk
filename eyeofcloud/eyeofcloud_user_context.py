_A=None
import copy,threading
class EyeofcloudUserContext:
	'\n    Representation of an Eyeofcloud User Context using which APIs are to be called.\n    '
	def __init__(A,eyeofcloud_client,logger,user_id,user_attributes=_A):
		' Create an instance of the Eyeofcloud User Context.\n\n        Args:\n          eyeofcloud_client: client used when calling decisions for this user context\n          logger: logger for logging\n          user_id: user id of this user context\n          user_attributes: user attributes to use for this user context\n\n        Returns:\n          UserContext instance\n        ';B=user_attributes;A.client=eyeofcloud_client;A.logger=logger;A.user_id=user_id
		if not isinstance(B,dict):B={}
		A._user_attributes=B.copy()if B else{};A.lock=threading.Lock();A.forced_decisions_map={}
	class EyeofcloudDecisionContext:
		" Using class with attributes here instead of namedtuple because\n            class is extensible, it's easy to add another attribute if we wanted\n            to extend decision context.\n        "
		def __init__(A,flag_key,rule_key=_A):A.flag_key=flag_key;A.rule_key=rule_key
		def __hash__(A):return hash((A.flag_key,A.rule_key))
		def __eq__(A,other):B=other;return(A.flag_key,A.rule_key)==(B.flag_key,B.rule_key)
	class EyeofcloudForcedDecision:
		def __init__(A,variation_key):A.variation_key=variation_key
	def _clone(A):
		if not A.client:return
		B=EyeofcloudUserContext(A.client,A.logger,A.user_id,A.get_user_attributes())
		with A.lock:
			if A.forced_decisions_map:B.forced_decisions_map=copy.deepcopy(A.forced_decisions_map)
		return B
	def get_user_attributes(A):
		with A.lock:return A._user_attributes.copy()
	def set_attribute(A,attribute_key,attribute_value):
		'\n        sets a attribute by key for this user context.\n        Args:\n          attribute_key: key to use for attribute\n          attribute_value: attribute value\n\n        Returns:\n        None\n        '
		with A.lock:A._user_attributes[attribute_key]=attribute_value
	def decide(B,key,options=_A):
		'\n        Call decide on contained Eyeofcloud object\n        Args:\n          key: feature key\n          options: array of DecisionOption\n\n        Returns:\n            Decision object\n        ';A=options
		if isinstance(A,list):A=A[:]
		return B.client._decide(B._clone(),key,A)
	def decide_for_keys(B,keys,options=_A):
		'\n        Call decide_for_keys on contained eyeofcloud object\n        Args:\n          keys: array of feature keys\n          options: array of DecisionOption\n\n        Returns:\n          Dictionary with feature_key keys and Decision object values\n        ';A=options
		if isinstance(A,list):A=A[:]
		return B.client._decide_for_keys(B._clone(),keys,A)
	def decide_all(B,options=_A):
		'\n        Call decide_all on contained eyeofcloud instance\n        Args:\n          options: Array of DecisionOption objects\n\n        Returns:\n          Dictionary with feature_key keys and Decision object values\n        ';A=options
		if isinstance(A,list):A=A[:]
		return B.client._decide_all(B._clone(),A)
	def track_event(A,event_key,event_tags=_A):return A.client.track(event_key,A.user_id,A.get_user_attributes(),event_tags)
	def as_json(A):return{'user_id':A.user_id,'attributes':A.get_user_attributes()}
	def set_forced_decision(A,decision_context,decision):
		'\n        Sets the forced decision for a given decision context.\n\n        Args:\n            decision_context: a decision context.\n            decision: a forced decision.\n\n        Returns:\n            True if the forced decision has been set successfully.\n        '
		with A.lock:A.forced_decisions_map[decision_context]=decision
		return True
	def get_forced_decision(A,decision_context):'\n        Gets the forced decision (variation key) for a given decision context.\n\n        Args:\n            decision_context: a decision context.\n\n        Returns:\n            A forced_decision or None if forced decisions are not set for the parameters.\n        ';B=A.find_forced_decision(decision_context);return B
	def remove_forced_decision(A,decision_context):
		'\n        Removes the forced decision for a given decision context.\n\n        Args:\n            decision_context: a decision context.\n\n        Returns:\n            Returns: true if the forced decision has been removed successfully.\n        ';B=decision_context
		with A.lock:
			if B in A.forced_decisions_map:del A.forced_decisions_map[B];return True
		return False
	def remove_all_forced_decisions(A):
		'\n        Removes all forced decisions bound to this user context.\n\n        Returns:\n            True if forced decisions have been removed successfully.\n        '
		with A.lock:A.forced_decisions_map.clear()
		return True
	def find_forced_decision(A,decision_context):
		'\n        Gets forced decision from forced decision map.\n\n        Args:\n            decision_context: a decision context.\n\n        Returns:\n            Forced decision.\n        '
		with A.lock:
			if not A.forced_decisions_map:return
			return A.forced_decisions_map.get(decision_context)