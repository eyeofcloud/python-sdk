_C='Experiment key "%s" is not in datafile.'
_B=None
_A='id'
import json
from collections import OrderedDict
from.import entities
from.import exceptions
from.helpers import condition as condition_helper
from.helpers import enums
SUPPORTED_VERSIONS=[enums.DatafileVersions.V2,enums.DatafileVersions.V3,enums.DatafileVersions.V4]
RESERVED_ATTRIBUTE_PREFIX='$opt_'
class ProjectConfig:
	' Representation of the Eyeofcloud project config. '
	def __init__(A,datafile,logger,error_handler):
		' ProjectConfig init method to load and set project config data.\n\n        Args:\n            datafile: JSON string representing the project.\n            logger: Provides a logger instance.\n            error_handler: Provides a handle_error method to handle exceptions.\n        ';S='type';R='conditions';Q=False;K=datafile;F='key';B=json.loads(K);A._datafile='{}'.format(K);A.logger=logger;A.error_handler=error_handler;A.version=B.get('version')
		if A.version not in SUPPORTED_VERSIONS:raise exceptions.UnsupportedDatafileVersionException(enums.Errors.UNSUPPORTED_DATAFILE_VERSION.format(A.version))
		A.account_id=B.get('accountId');A.project_id=B.get('projectId');A.revision=B.get('revision');A.sdk_key=B.get('sdkKey',_B);A.environment_key=B.get('environmentKey',_B);A.groups=B.get('groups',[]);A.experiments=B.get('experiments',[]);A.events=B.get('events',[]);A.attributes=B.get('attributes',[]);A.audiences=B.get('audiences',[]);A.typed_audiences=B.get('typedAudiences',[]);A.feature_flags=B.get('featureFlags',[]);A.rollouts=B.get('rollouts',[]);A.anonymize_ip=B.get('anonymizeIP',Q);A.send_flag_decisions=B.get('sendFlagDecisions',Q);A.bot_filtering=B.get('botFiltering',_B);A.group_id_map=A._generate_key_map(A.groups,_A,entities.Group);A.experiment_id_map=A._generate_key_map(A.experiments,_A,entities.Experiment);A.event_key_map=A._generate_key_map(A.events,F,entities.Event);A.attribute_key_map=A._generate_key_map(A.attributes,F,entities.Attribute);A.audience_id_map=A._generate_key_map(A.audiences,_A,entities.Audience)
		for L in A.typed_audiences:L[R]=json.dumps(L[R])
		T=A._generate_key_map(A.typed_audiences,_A,entities.Audience);A.audience_id_map.update(T);A.rollout_id_map=A._generate_key_map(A.rollouts,_A,entities.Layer)
		for U in A.rollout_id_map.values():
			for C in U.experiments:A.experiment_id_map[C[_A]]=entities.Experiment(**C)
		A.audience_id_map=A._deserialize_audience(A.audience_id_map)
		for G in A.group_id_map.values():
			M=A._generate_key_map(G.experiments,_A,entities.Experiment)
			for C in M.values():C.__dict__.update({'groupId':G.id,'groupPolicy':G.policy})
			A.experiment_id_map.update(M)
		A.experiment_key_map={};A.variation_key_map={};A.variation_id_map={};A.variation_variable_usage_map={};A.variation_id_map_by_experiment_id={};A.variation_key_map_by_experiment_id={};A.flag_variations_map={}
		for C in A.experiment_id_map.values():
			A.experiment_key_map[C.key]=C;A.variation_key_map[C.key]=A._generate_key_map(C.variations,F,entities.Variation);A.variation_id_map[C.key]={};A.variation_id_map_by_experiment_id[C.id]={};A.variation_key_map_by_experiment_id[C.id]={}
			for D in A.variation_key_map.get(C.key).values():A.variation_id_map[C.key][D.id]=D;A.variation_id_map_by_experiment_id[C.id][D.id]=D;A.variation_key_map_by_experiment_id[C.id][D.key]=D;A.variation_variable_usage_map[D.id]=A._generate_key_map(D.variables,_A,entities.Variation.VariableUsage)
		A.feature_key_map=A._generate_key_map(A.feature_flags,F,entities.FeatureFlag);A.experiment_feature_map={}
		for E in A.feature_key_map.values():
			for H in A.feature_key_map[E.key].variables:
				V=H.get('subType','')
				if H[S]==entities.Variable.Type.STRING and V==entities.Variable.Type.JSON:H[S]=entities.Variable.Type.JSON
			E.variables=A._generate_key_map(E.variables,F,entities.Variable);I=[];J=[]
			for N in E.experimentIds:A.experiment_feature_map[N]=[E.id];I.append(A.experiment_id_map[N])
			O=_B if len(E.rolloutId)==0 else A.rollout_id_map[E.rolloutId]
			if O:
				for W in O.experiments:I.append(A.experiment_id_map[W[_A]])
			for X in I:
				for P in A.variation_id_map_by_experiment_id.get(X.id).values():
					if len(list(filter(lambda variation:variation.id==P.id,J)))==0:J.append(P)
			A.flag_variations_map[E.key]=J
	@staticmethod
	def _generate_key_map(entity_list,key,entity_class):
		' Helper method to generate map from key to entity object for given list of dicts.\n\n        Args:\n            entity_list: List consisting of dict.\n            key: Key in each dict which will be key in the map.\n            entity_class: Class representing the entity.\n\n        Returns:\n            Map mapping key to entity object.\n        ';A=OrderedDict()
		for B in entity_list:A[B[key]]=entity_class(**B)
		return A
	@staticmethod
	def _deserialize_audience(audience_map):
		' Helper method to de-serialize and populate audience map with the condition list and structure.\n\n        Args:\n            audience_map: Dict mapping audience ID to audience object.\n\n        Returns:\n            Dict additionally consisting of condition list and structure on every audience object.\n        ';A=audience_map
		for B in A.values():C,D=condition_helper.loads(B.conditions);B.__dict__.update({'conditionStructure':C,'conditionList':D})
		return A
	def get_rollout_experiments(A,rollout):' Helper method to get rollout experiments.\n\n        Args:\n            rollout: rollout\n\n        Returns:\n            Mapped rollout experiments.\n        ';B=A._generate_key_map(rollout.experiments,_A,entities.Experiment);C=[A for A in B.values()];return C
	def get_typecast_value(B,value,type):
		' Helper method to determine actual value based on type of feature variable.\n\n        Args:\n            value: Value in string form as it was parsed from datafile.\n            type: Type denoting the feature flag type.\n\n        Returns:\n            Value type-casted based on type of feature variable.\n        ';A=value
		if type==entities.Variable.Type.BOOLEAN:return A=='true'
		elif type==entities.Variable.Type.INTEGER:return int(A)
		elif type==entities.Variable.Type.DOUBLE:return float(A)
		elif type==entities.Variable.Type.JSON:return json.loads(A)
		else:return A
	def to_datafile(A):' Get the datafile corresponding to ProjectConfig.\n\n        Returns:\n            A JSON string representation of the project datafile.\n        ';return A._datafile
	def get_version(A):' Get version of the datafile.\n\n        Returns:\n            Version of the datafile.\n        ';return A.version
	def get_revision(A):' Get revision of the datafile.\n\n        Returns:\n            Revision of the datafile.\n        ';return A.revision
	def get_sdk_key(A):' Get sdk key from the datafile.\n\n        Returns:\n            Revision of the sdk key.\n        ';return A.sdk_key
	def get_environment_key(A):' Get environment key from the datafile.\n\n        Returns:\n            Revision of the environment key.\n        ';return A.environment_key
	def get_account_id(A):' Get account ID from the config.\n\n        Returns:\n            Account ID information from the config.\n        ';return A.account_id
	def get_project_id(A):' Get project ID from the config.\n\n        Returns:\n            Project ID information from the config.\n        ';return A.project_id
	def get_experiment_from_key(A,experiment_key):
		' Get experiment for the provided experiment key.\n\n        Args:\n            experiment_key: Experiment key for which experiment is to be determined.\n\n        Returns:\n            Experiment corresponding to the provided experiment key.\n        ';B=experiment_key;C=A.experiment_key_map.get(B)
		if C:return C
		A.logger.error(_C%B);A.error_handler.handle_error(exceptions.InvalidExperimentException(enums.Errors.INVALID_EXPERIMENT_KEY))
	def get_experiment_from_id(A,experiment_id):
		' Get experiment for the provided experiment ID.\n\n        Args:\n            experiment_id: Experiment ID for which experiment is to be determined.\n\n        Returns:\n            Experiment corresponding to the provided experiment ID.\n        ';B=experiment_id;C=A.experiment_id_map.get(B)
		if C:return C
		A.logger.error('Experiment ID "%s" is not in datafile.'%B);A.error_handler.handle_error(exceptions.InvalidExperimentException(enums.Errors.INVALID_EXPERIMENT_KEY))
	def get_group(A,group_id):
		' Get group for the provided group ID.\n\n        Args:\n            group_id: Group ID for which group is to be determined.\n\n        Returns:\n            Group corresponding to the provided group ID.\n        ';B=group_id;C=A.group_id_map.get(B)
		if C:return C
		A.logger.error('Group ID "%s" is not in datafile.'%B);A.error_handler.handle_error(exceptions.InvalidGroupException(enums.Errors.INVALID_GROUP_ID))
	def get_audience(A,audience_id):
		' Get audience object for the provided audience ID.\n\n        Args:\n            audience_id: ID of the audience.\n\n        Returns:\n            Dict representing the audience.\n        ';B=audience_id;C=A.audience_id_map.get(B)
		if C:return C
		A.logger.error('Audience ID "%s" is not in datafile.'%B);A.error_handler.handle_error(exceptions.InvalidAudienceException(enums.Errors.INVALID_AUDIENCE))
	def get_variation_from_key(A,experiment_key,variation_key):
		' Get variation given experiment and variation key.\n\n        Args:\n            experiment: Key representing parent experiment of variation.\n            variation_key: Key representing the variation.\n            Variation is of type variation object or None.\n\n        Returns\n            Object representing the variation.\n        ';C=variation_key;B=experiment_key;D=A.variation_key_map.get(B)
		if D:
			E=D.get(C)
			if E:return E
			else:A.logger.error('Variation key "%s" is not in datafile.'%C);A.error_handler.handle_error(exceptions.InvalidVariationException(enums.Errors.INVALID_VARIATION));return
		A.logger.error(_C%B);A.error_handler.handle_error(exceptions.InvalidExperimentException(enums.Errors.INVALID_EXPERIMENT_KEY))
	def get_variation_from_id(A,experiment_key,variation_id):
		' Get variation given experiment and variation ID.\n\n        Args:\n            experiment: Key representing parent experiment of variation.\n            variation_id: ID representing the variation.\n\n        Returns\n            Object representing the variation.\n        ';C=variation_id;B=experiment_key;D=A.variation_id_map.get(B)
		if D:
			E=D.get(C)
			if E:return E
			else:A.logger.error('Variation ID "%s" is not in datafile.'%C);A.error_handler.handle_error(exceptions.InvalidVariationException(enums.Errors.INVALID_VARIATION));return
		A.logger.error(_C%B);A.error_handler.handle_error(exceptions.InvalidExperimentException(enums.Errors.INVALID_EXPERIMENT_KEY))
	def get_event(A,event_key):
		' Get event for the provided event key.\n\n        Args:\n            event_key: Event key for which event is to be determined.\n\n        Returns:\n            Event corresponding to the provided event key.\n        ';B=event_key;C=A.event_key_map.get(B)
		if C:return C
		A.logger.error('Event "%s" is not in datafile.'%B);A.error_handler.handle_error(exceptions.InvalidEventException(enums.Errors.INVALID_EVENT_KEY))
	def get_attribute_id(B,attribute_key):
		' Get attribute ID for the provided attribute key.\n\n        Args:\n            attribute_key: Attribute key for which attribute is to be fetched.\n\n        Returns:\n            Attribute ID corresponding to the provided attribute key.\n        ';A=attribute_key;C=B.attribute_key_map.get(A);D=A.startswith(RESERVED_ATTRIBUTE_PREFIX)
		if C:
			if D:B.logger.warning('Attribute %s unexpectedly has reserved prefix %s; using attribute ID instead of reserved attribute name.'%(A,RESERVED_ATTRIBUTE_PREFIX))
			return C.id
		if D:return A
		B.logger.error('Attribute "%s" is not in datafile.'%A);B.error_handler.handle_error(exceptions.InvalidAttributeException(enums.Errors.INVALID_ATTRIBUTE))
	def get_feature_from_key(A,feature_key):
		' Get feature for the provided feature key.\n\n        Args:\n            feature_key: Feature key for which feature is to be fetched.\n\n        Returns:\n            Feature corresponding to the provided feature key.\n        ';B=feature_key;C=A.feature_key_map.get(B)
		if C:return C
		A.logger.error('Feature "%s" is not in datafile.'%B)
	def get_rollout_from_id(A,rollout_id):
		' Get rollout for the provided ID.\n\n        Args:\n            rollout_id: ID of the rollout to be fetched.\n\n        Returns:\n            Rollout corresponding to the provided ID.\n        ';B=rollout_id;C=A.rollout_id_map.get(B)
		if C:return C
		A.logger.error('Rollout with ID "%s" is not in datafile.'%B)
	def get_variable_value_for_variation(B,variable,variation):
		' Get the variable value for the given variation.\n\n        Args:\n            variable: The Variable for which we are getting the value.\n            variation: The Variation for which we are getting the variable value.\n\n        Returns:\n            The variable value or None if any of the inputs are invalid.\n        ';C=variable;A=variation
		if not C or not A:return
		if A.id not in B.variation_variable_usage_map:B.logger.error('Variation with ID "%s" is not in the datafile.'%A.id);return
		E=B.variation_variable_usage_map[A.id];D=_B
		if E:D=E.get(C.id)
		if D:F=D.value
		else:F=C.defaultValue
		return F
	def get_variable_for_feature(A,feature_key,variable_key):
		' Get the variable with the given variable key for the given feature.\n\n        Args:\n            feature_key: The key of the feature for which we are getting the variable.\n            variable_key: The key of the variable we are getting.\n\n        Returns:\n            Variable with the given key in the given variation.\n        ';D=feature_key;B=variable_key;C=A.feature_key_map.get(D)
		if not C:A.logger.error('Feature with key "%s" not found in the datafile.'%D);return
		if B not in C.variables:A.logger.error('Variable with key "%s" not found in the datafile.'%B);return
		return C.variables.get(B)
	def get_anonymize_ip_value(A):' Gets the anonymize IP value.\n\n        Returns:\n            A boolean value that indicates if the IP should be anonymized.\n        ';return A.anonymize_ip
	def get_send_flag_decisions_value(A):' Gets the Send Flag Decisions value.\n\n        Returns:\n            A boolean value that indicates if we should send flag decisions.\n        ';return A.send_flag_decisions
	def get_bot_filtering_value(A):' Gets the bot filtering value.\n\n        Returns:\n            A boolean value that indicates if bot filtering should be enabled.\n        ';return A.bot_filtering
	def is_feature_experiment(A,experiment_id):' Determines if given experiment is a feature test.\n\n        Args:\n            experiment_id: Experiment ID for which feature test is to be determined.\n\n        Returns:\n            A boolean value that indicates if given experiment is a feature test.\n        ';return experiment_id in A.experiment_feature_map
	def get_variation_from_id_by_experiment_id(A,experiment_id,variation_id):
		' Gets variation from variation id and specific experiment id\n\n            Returns:\n                The variation for the experiment id and variation id\n                or empty dict if not found\n        ';C=variation_id;B=experiment_id
		if B in A.variation_id_map_by_experiment_id and C in A.variation_id_map_by_experiment_id[B]:return A.variation_id_map_by_experiment_id[B][C]
		A.logger.error('Variation with id "%s" not defined in the datafile for experiment "%s".'%(C,B));return{}
	def get_variation_from_key_by_experiment_id(A,experiment_id,variation_key):
		' Gets variation from variation key and specific experiment id\n\n            Returns:\n                The variation for the experiment id and variation key\n                or empty dict if not found\n        ';C=variation_key;B=experiment_id
		if B in A.variation_key_map_by_experiment_id and C in A.variation_key_map_by_experiment_id[B]:return A.variation_key_map_by_experiment_id[B][C]
		A.logger.error('Variation with key "%s" not defined in the datafile for experiment "%s".'%(C,B));return{}
	def get_flag_variation(D,flag_key,variation_attribute,target_value):
		'\n        Gets variation by specified variation attribute.\n        For example if variation_attribute is id, the function gets variation by using variation_id.\n        If variation_attribute is key, the function gets variation by using variation_key.\n\n        We used to have two separate functions:\n        get_flag_variation_by_id()\n        get_flag_variation_by_key()\n\n        This function consolidates both functions into one.\n\n        Important to always relate variation_attribute to the target value.\n        Should never enter for example variation_attribute=key and target_value=variation_id.\n        Correct is object_attribute=key and target_value=variation_key.\n\n        Args:\n            flag_key: flag key\n            variation_attribute: (string) id or key for example. The part after the dot notation (id in variation.id)\n            target_value: target value we want to get for example variation_id or variation_key\n\n        Returns:\n            Variation as a map.\n        ';A=flag_key
		if not A:return
		B=D.flag_variations_map.get(A)
		if B:
			for C in B:
				if getattr(C,variation_attribute)==target_value:return C