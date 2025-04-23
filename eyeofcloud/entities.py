_A=None
class BaseEntity:
	def __eq__(A,other):return A.__dict__==other.__dict__
class Attribute(BaseEntity):
	def __init__(A,id,key,**B):A.id=id;A.key=key
class Audience(BaseEntity):
	def __init__(A,id,name,conditions,conditionStructure=_A,conditionList=_A,**B):A.id=id;A.name=name;A.conditions=conditions;A.conditionStructure=conditionStructure;A.conditionList=conditionList
class Event(BaseEntity):
	def __init__(A,id,key,experimentIds,**B):A.id=id;A.key=key;A.experimentIds=experimentIds
class Experiment(BaseEntity):
	def __init__(A,id,key,status,audienceIds,variations,forcedVariations,trafficAllocation,layerId,audienceConditions=_A,groupId=_A,groupPolicy=_A,**B):A.id=id;A.key=key;A.status=status;A.audienceIds=audienceIds;A.audienceConditions=audienceConditions;A.variations=variations;A.forcedVariations=forcedVariations;A.trafficAllocation=trafficAllocation;A.layerId=layerId;A.groupId=groupId;A.groupPolicy=groupPolicy
	def get_audience_conditions_or_ids(A):' Returns audienceConditions if present, otherwise audienceIds. ';return A.audienceConditions if A.audienceConditions is not _A else A.audienceIds
	def __str__(A):return A.key
	@staticmethod
	def get_default():' returns an empty experiment object. ';A=Experiment(id='',key='',layerId='',status='',variations=[],trafficAllocation=[],audienceIds=[],audienceConditions=[],forcedVariations={});return A
class FeatureFlag(BaseEntity):
	def __init__(A,id,key,experimentIds,rolloutId,variables,groupId=_A,**B):A.id=id;A.key=key;A.experimentIds=experimentIds;A.rolloutId=rolloutId;A.variables=variables;A.groupId=groupId
class Group(BaseEntity):
	def __init__(A,id,policy,experiments,trafficAllocation,**B):A.id=id;A.policy=policy;A.experiments=experiments;A.trafficAllocation=trafficAllocation
class Layer(BaseEntity):
	'Layer acts as rollout.'
	def __init__(A,id,experiments,**B):A.id=id;A.experiments=experiments
class Variable(BaseEntity):
	class Type:BOOLEAN='boolean';DOUBLE='double';INTEGER='integer';JSON='json';STRING='string'
	def __init__(A,id,key,type,defaultValue,**B):A.id=id;A.key=key;A.type=type;A.defaultValue=defaultValue
class Variation(BaseEntity):
	class VariableUsage(BaseEntity):
		def __init__(A,id,value,**B):A.id=id;A.value=value
	def __init__(A,id,key,featureEnabled=False,variables=_A,**B):A.id=id;A.key=key;A.featureEnabled=featureEnabled;A.variables=variables or[]
	def __str__(A):return A.key