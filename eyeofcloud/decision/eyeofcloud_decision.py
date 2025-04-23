_A=None
class EyeofcloudDecision:
	def __init__(A,variation_key=_A,enabled=_A,variables=_A,rule_key=_A,flag_key=_A,user_context=_A,reasons=_A):A.variation_key=variation_key;A.enabled=enabled or False;A.variables=variables or{};A.rule_key=rule_key;A.flag_key=flag_key;A.user_context=user_context;A.reasons=reasons or[]
	def as_json(A):return{'variation_key':A.variation_key,'enabled':A.enabled,'variables':A.variables,'rule_key':A.rule_key,'flag_key':A.flag_key,'user_context':A.user_context.as_json(),'reasons':A.reasons}