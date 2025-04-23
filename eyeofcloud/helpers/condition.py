_C=False
_B=True
_A=None
import json,numbers
from six import string_types
from.import validator
from.enums import CommonAudienceEvaluationLogs as audience_logs
from.enums import Errors
from.enums import VersionType
class ConditionOperatorTypes:AND='and';OR='or';NOT='not';operators=[AND,OR,NOT]
class ConditionMatchTypes:EXACT='exact';EXISTS='exists';GREATER_THAN='gt';GREATER_THAN_OR_EQUAL='ge';LESS_THAN='lt';LESS_THAN_OR_EQUAL='le';SEMVER_EQ='semver_eq';SEMVER_GE='semver_ge';SEMVER_GT='semver_gt';SEMVER_LE='semver_le';SEMVER_LT='semver_lt';SUBSTRING='substring'
class CustomAttributeConditionEvaluator:
	' Class encapsulating methods to be used in audience leaf condition evaluation. ';CUSTOM_ATTRIBUTE_CONDITION_TYPE='custom_attribute'
	def __init__(A,condition_data,attributes,logger):A.condition_data=condition_data;A.attributes=attributes or{};A.logger=logger
	def _get_condition_json(B,index):' Method to generate json for logging audience condition.\n\n    Args:\n      index: Index of the condition.\n\n    Returns:\n      String: Audience condition JSON.\n    ';A=B.condition_data[index];C={'name':A[0],'value':A[1],'type':A[2],'match':A[3]};return json.dumps(C)
	def is_value_type_valid_for_exact_conditions(B,value):
		' Method to validate if the value is valid for exact match type evaluation.\n\n    Args:\n      value: Value to validate.\n\n    Returns:\n      Boolean: True if value is a string, boolean, or number. Otherwise False.\n    ';A=value
		if isinstance(A,string_types)or isinstance(A,(numbers.Integral,float)):return _B
		return _C
	def is_value_a_number(B,value):
		A=value
		if isinstance(A,(numbers.Integral,float))and not isinstance(A,bool):return _B
		return _C
	def is_pre_release_version(D,version):
		' Method to check if given version is pre-release.\n            Criteria for pre-release includes:\n                - Version includes "-"\n\n        Args:\n          version: Given version in string.\n\n        Returns:\n          Boolean:\n            - True if the given version is pre-release\n            - False if it doesn\'t\n        ';A=version
		if VersionType.IS_PRE_RELEASE in A:
			C=A.find(VersionType.IS_PRE_RELEASE);B=A.find(VersionType.IS_BUILD)
			if C<B or B<0:return _B
		return _C
	def is_build_version(D,version):
		' Method to check given version is a build version.\n            Criteria for build version includes:\n                - Version includes "+"\n\n        Args:\n          version: Given version in string.\n\n        Returns:\n          Boolean:\n            - True if the given version is a build version\n            - False if it doesn\'t\n        ';A=version
		if VersionType.IS_BUILD in A:
			B=A.find(VersionType.IS_PRE_RELEASE);C=A.find(VersionType.IS_BUILD)
			if C<B or B<0:return _B
		return _C
	def has_white_space(A,version):' Method to check if the given version contains " " (white space)\n\n        Args:\n          version: Given version in string.\n\n        Returns:\n          Boolean:\n            - True if the given version does contain whitespace\n            - False if it doesn\'t\n        ';return' 'in version
	def compare_user_version_with_target_version(C,target_version,user_version):
		" Method to compare user version with target version.\n\n        Args:\n          target_version: String representing condition value\n          user_version: String representing user value\n\n        Returns:\n          Int:\n            -  0 if user version is equal to target version.\n            -  1 if user version is greater than target version.\n            - -1 if user version is less than target version or, in case of exact string match, doesn't match the target\n            version.\n          None:\n            - if the user version value format is not a valid semantic version.\n        ";H=user_version;F=target_version;E=C.is_pre_release_version(F);G=C.is_pre_release_version(H);K=C.is_build_version(F);D=C.split_version(F)
		if D is _A:return
		B=C.split_version(H)
		if B is _A:return
		L=len(B)
		for(A,M)in enumerate(D):
			if L<=A:return 1 if E or K else-1
			elif not B[A].isdigit():
				if B[A]<D[A]:return 1 if E and not G else-1
				elif B[A]>D[A]:return-1 if not E and G else 1
			else:
				I=int(B[A]);J=int(D[A])
				if I>J:return 1
				elif I<J:return-1
		if G and not E:return-1
		return 0
	def exact_evaluator(A,index):
		' Evaluate the given exact match condition for the user attributes.\n\n    Args:\n      index: Index of the condition to be evaluated.\n\n    Returns:\n      Boolean:\n        - True if the user attribute value is equal (===) to the condition value.\n        - False if the user attribute value is not equal (!==) to the condition value.\n      None:\n        - if the condition value or user attribute value has an invalid type.\n        - if there is a mismatch between the user attribute type and the condition value type.\n    ';C=index;E=A.condition_data[C][0];D=A.condition_data[C][1];B=A.attributes.get(E)
		if not A.is_value_type_valid_for_exact_conditions(D)or A.is_value_a_number(D)and not validator.is_finite_number(D):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(C)));return
		if not A.is_value_type_valid_for_exact_conditions(B)or not validator.are_values_same_type(D,B):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(C),type(B),E));return
		if A.is_value_a_number(B)and not validator.is_finite_number(B):A.logger.warning(audience_logs.INFINITE_ATTRIBUTE_VALUE.format(A._get_condition_json(C),E));return
		return D==B
	def exists_evaluator(A,index):' Evaluate the given exists match condition for the user attributes.\n\n      Args:\n        index: Index of the condition to be evaluated.\n\n      Returns:\n        Boolean: True if the user attributes have a non-null value for the given condition,\n                 otherwise False.\n    ';B=A.condition_data[index][0];return A.attributes.get(B)is not _A
	def greater_than_evaluator(A,index):
		" Evaluate the given greater than match condition for the user attributes.\n\n      Args:\n        index: Index of the condition to be evaluated.\n\n      Returns:\n        Boolean:\n          - True if the user attribute value is greater than the condition value.\n          - False if the user attribute value is less than or equal to the condition value.\n        None: if the condition value isn't finite or the user attribute value isn't finite.\n    ";B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not validator.is_finite_number(E):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not A.is_value_a_number(C):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		if not validator.is_finite_number(C):A.logger.warning(audience_logs.INFINITE_ATTRIBUTE_VALUE.format(A._get_condition_json(B),D));return
		return C>E
	def greater_than_or_equal_evaluator(A,index):
		" Evaluate the given greater than or equal to match condition for the user attributes.\n\n        Args:\n          index: Index of the condition to be evaluated.\n\n        Returns:\n          Boolean:\n            - True if the user attribute value is greater than or equal to the condition value.\n            - False if the user attribute value is less than the condition value.\n            None: if the condition value isn't finite or the user attribute value isn't finite.\n        ";B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not validator.is_finite_number(E):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not A.is_value_a_number(C):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		if not validator.is_finite_number(C):A.logger.warning(audience_logs.INFINITE_ATTRIBUTE_VALUE.format(A._get_condition_json(B),D));return
		return C>=E
	def less_than_evaluator(A,index):
		" Evaluate the given less than match condition for the user attributes.\n\n    Args:\n      index: Index of the condition to be evaluated.\n\n    Returns:\n      Boolean:\n        - True if the user attribute value is less than the condition value.\n        - False if the user attribute value is greater than or equal to the condition value.\n      None: if the condition value isn't finite or the user attribute value isn't finite.\n    ";B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not validator.is_finite_number(E):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not A.is_value_a_number(C):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		if not validator.is_finite_number(C):A.logger.warning(audience_logs.INFINITE_ATTRIBUTE_VALUE.format(A._get_condition_json(B),D));return
		return C<E
	def less_than_or_equal_evaluator(A,index):
		" Evaluate the given less than or equal to match condition for the user attributes.\n\n        Args:\n          index: Index of the condition to be evaluated.\n\n        Returns:\n          Boolean:\n            - True if the user attribute value is less than or equal to the condition value.\n            - False if the user attribute value is greater than the condition value.\n          None: if the condition value isn't finite or the user attribute value isn't finite.\n        ";B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not validator.is_finite_number(E):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not A.is_value_a_number(C):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		if not validator.is_finite_number(C):A.logger.warning(audience_logs.INFINITE_ATTRIBUTE_VALUE.format(A._get_condition_json(B),D));return
		return C<=E
	def substring_evaluator(A,index):
		" Evaluate the given substring match condition for the given user attributes.\n\n    Args:\n      index: Index of the condition to be evaluated.\n\n    Returns:\n      Boolean:\n        - True if the condition value is a substring of the user attribute value.\n        - False if the condition value is not a substring of the user attribute value.\n      None: if the condition value isn't a string or the user attribute value isn't a string.\n    ";B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not isinstance(E,string_types):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not isinstance(C,string_types):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		return E in C
	def semver_equal_evaluator(A,index):
		' Evaluate the given semantic version equal match target version for the user version.\n\n        Args:\n          index: Index of the condition to be evaluated.\n\n        Returns:\n          Boolean:\n            - True if the user version is equal (==) to the target version.\n            - False if the user version is not equal (!=) to the target version.\n          None:\n            - if the user version value is not string type or is null.\n        ';B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not isinstance(E,string_types):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not isinstance(C,string_types):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		F=A.compare_user_version_with_target_version(E,C)
		if F is _A:return
		return F==0
	def semver_greater_than_evaluator(A,index):
		' Evaluate the given semantic version greater than match target version for the user version.\n\n        Args:\n          index: Index of the condition to be evaluated.\n\n        Returns:\n          Boolean:\n            - True if the user version is greater than the target version.\n            - False if the user version is less than or equal to the target version.\n          None:\n            - if the user version value is not string type or is null.\n        ';B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not isinstance(E,string_types):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not isinstance(C,string_types):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		F=A.compare_user_version_with_target_version(E,C)
		if F is _A:return
		return F>0
	def semver_less_than_evaluator(A,index):
		' Evaluate the given semantic version less than match target version for the user version.\n\n        Args:\n          index: Index of the condition to be evaluated.\n\n        Returns:\n          Boolean:\n            - True if the user version is less than the target version.\n            - False if the user version is greater than or equal to the target version.\n          None:\n            - if the user version value is not string type or is null.\n        ';B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not isinstance(E,string_types):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not isinstance(C,string_types):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		F=A.compare_user_version_with_target_version(E,C)
		if F is _A:return
		return F<0
	def semver_less_than_or_equal_evaluator(A,index):
		' Evaluate the given semantic version less than or equal to match target version for the user version.\n\n        Args:\n          index: Index of the condition to be evaluated.\n\n        Returns:\n          Boolean:\n            - True if the user version is less than or equal to the target version.\n            - False if the user version is greater than the target version.\n          None:\n            - if the user version value is not string type or is null.\n        ';B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not isinstance(E,string_types):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not isinstance(C,string_types):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		F=A.compare_user_version_with_target_version(E,C)
		if F is _A:return
		return F<=0
	def semver_greater_than_or_equal_evaluator(A,index):
		' Evaluate the given semantic version greater than or equal to match target version for the user version.\n\n        Args:\n          index: Index of the condition to be evaluated.\n\n        Returns:\n          Boolean:\n            - True if the user version is greater than or equal to the target version.\n            - False if the user version is less than the target version.\n          None:\n            - if the user version value is not string type or is null.\n        ';B=index;D=A.condition_data[B][0];E=A.condition_data[B][1];C=A.attributes.get(D)
		if not isinstance(E,string_types):A.logger.warning(audience_logs.UNKNOWN_CONDITION_VALUE.format(A._get_condition_json(B)));return
		if not isinstance(C,string_types):A.logger.warning(audience_logs.UNEXPECTED_TYPE.format(A._get_condition_json(B),type(C),D));return
		F=A.compare_user_version_with_target_version(E,C)
		if F is _A:return
		return F>=0
	EVALUATORS_BY_MATCH_TYPE={ConditionMatchTypes.EXACT:exact_evaluator,ConditionMatchTypes.EXISTS:exists_evaluator,ConditionMatchTypes.GREATER_THAN:greater_than_evaluator,ConditionMatchTypes.GREATER_THAN_OR_EQUAL:greater_than_or_equal_evaluator,ConditionMatchTypes.LESS_THAN:less_than_evaluator,ConditionMatchTypes.LESS_THAN_OR_EQUAL:less_than_or_equal_evaluator,ConditionMatchTypes.SEMVER_EQ:semver_equal_evaluator,ConditionMatchTypes.SEMVER_GE:semver_greater_than_or_equal_evaluator,ConditionMatchTypes.SEMVER_GT:semver_greater_than_evaluator,ConditionMatchTypes.SEMVER_LE:semver_less_than_or_equal_evaluator,ConditionMatchTypes.SEMVER_LT:semver_less_than_evaluator,ConditionMatchTypes.SUBSTRING:substring_evaluator}
	def split_version(A,version):
		' Method to split the given version.\n\n        Args:\n          version: Given version.\n\n        Returns:\n          List:\n            - The array of version split into smaller parts i.e major, minor, patch etc\n          None:\n            - if the given version is invalid in format\n        ';B=version;E=B;F='';C=[]
		if A.has_white_space(B):A.logger.warning(Errors.INVALID_ATTRIBUTE_FORMAT);return
		if A.is_pre_release_version(B)or A.is_build_version(B):C=B.split(VersionType.IS_PRE_RELEASE,1)if A.is_pre_release_version(B)else B.split(VersionType.IS_BUILD,1)
		if C:
			if len(C)<1:A.logger.warning(Errors.INVALID_ATTRIBUTE_FORMAT);return
			E=str(C[0]);F=C[1:]
		G=E.count('.')
		if G>2:A.logger.warning(Errors.INVALID_ATTRIBUTE_FORMAT);return
		D=E.split('.')
		if len(D)!=G+1:A.logger.warning(Errors.INVALID_ATTRIBUTE_FORMAT);return
		for H in D:
			if not H.isdigit():A.logger.warning(Errors.INVALID_ATTRIBUTE_FORMAT);return
		if F:D.extend(F)
		return D
	def evaluate(A,index):
		" Given a custom attribute audience condition and user attributes, evaluate the\n        condition against the attributes.\n\n    Args:\n      index: Index of the condition to be evaluated.\n\n    Returns:\n      Boolean:\n        - True if the user attributes match the given condition.\n        - False if the user attributes don't match the given condition.\n      None: if the user attributes and condition can't be evaluated.\n    ";B=index
		if A.condition_data[B][2]!=A.CUSTOM_ATTRIBUTE_CONDITION_TYPE:A.logger.warning(audience_logs.UNKNOWN_CONDITION_TYPE.format(A._get_condition_json(B)));return
		C=A.condition_data[B][3]
		if C is _A:C=ConditionMatchTypes.EXACT
		if C not in A.EVALUATORS_BY_MATCH_TYPE:A.logger.warning(audience_logs.UNKNOWN_MATCH_TYPE.format(A._get_condition_json(B)));return
		if C!=ConditionMatchTypes.EXISTS:
			D=A.condition_data[B][0]
			if D not in A.attributes:A.logger.debug(audience_logs.MISSING_ATTRIBUTE_VALUE.format(A._get_condition_json(B),D));return
			if A.attributes.get(D)is _A:A.logger.debug(audience_logs.NULL_ATTRIBUTE_VALUE.format(A._get_condition_json(B),D));return
		return A.EVALUATORS_BY_MATCH_TYPE[C](A,B)
class ConditionDecoder:
	' Class which provides an object_hook method for decoding dict\n  objects into a list when given a condition_decoder. '
	def __init__(A,condition_decoder):A.condition_list=[];A.index=-1;A.decoder=condition_decoder
	def object_hook(A,object_dict):' Hook which when passed into a json.JSONDecoder will replace each dict\n    in a json string with its index and convert the dict to an object as defined\n    by the passed in condition_decoder. The newly created condition object is\n    appended to the conditions_list.\n\n    Args:\n      object_dict: Dict representing an object.\n\n    Returns:\n      An index which will be used as the placeholder in the condition_structure\n    ';B=A.decoder(object_dict);A.condition_list.append(B);A.index+=1;return A.index
def _audience_condition_deserializer(obj_dict):' Deserializer defining how dict objects need to be decoded for audience conditions.\n\n  Args:\n    obj_dict: Dict representing one audience condition.\n\n  Returns:\n    List consisting of condition key with corresponding value, type and match.\n  ';A=obj_dict;return[A.get('name'),A.get('value'),A.get('type'),A.get('match')]
def loads(conditions_string):' Deserializes the conditions property into its corresponding\n  components: the condition_structure and the condition_list.\n\n  Args:\n    conditions_string: String defining valid and/or conditions.\n\n  Returns:\n    A tuple of (condition_structure, condition_list).\n    condition_structure: nested list of operators and placeholders for operands.\n    condition_list: list of conditions whose index correspond to the values of the placeholders.\n  ';A=ConditionDecoder(_audience_condition_deserializer);B=json.JSONDecoder(object_hook=A.object_hook);C=B.decode(conditions_string);D=A.condition_list;return C,D