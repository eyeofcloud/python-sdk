import json
from.import condition as condition_helper,condition_tree_evaluator
def does_user_meet_audience_conditions(config,audience_conditions,audience_logs,logging_key,attributes,logger):
	' Determine for given experiment if user satisfies the audiences for the experiment.\n\n    Args:\n        config: project_config.ProjectConfig object representing the project.\n        audience_conditions: Audience conditions corresponding to the experiment or rollout rule.\n        audience_logs: Log class capturing the messages to be logged .\n        logging_key: String representing experiment key or rollout rule. To be used in log messages only.\n        attributes: Dict representing user attributes which will be used in determining\n                    if the audience conditions are met. If not provided, default to an empty dict.\n        logger: Provides a logger to send log messages to.\n\n    Returns:\n        Boolean representing if user satisfies audience conditions for any of the audiences or not\n        And an array of log messages representing decision making.\n    ';J=config;I=attributes;H=logging_key;G=None;E=audience_conditions;C=audience_logs;B=logger;D=[];A=C.EVALUATING_AUDIENCES_COMBINED.format(H,json.dumps(E));B.debug(A);D.append(A)
	if E is G or E==[]:A=C.AUDIENCE_EVALUATION_RESULT_COMBINED.format(H,'TRUE');B.info(A);D.append(A);return True,D
	if I is G:I={}
	def K(audience_id,index):A=J.get_audience(audience_id);C=condition_helper.CustomAttributeConditionEvaluator(A.conditionList,I,B);return C.evaluate(index)
	def L(audience_id):
		A=audience_id;D=J.get_audience(A)
		if D is G:return
		E=C.EVALUATING_AUDIENCE.format(A,D.conditions);B.debug(E);F=condition_tree_evaluator.evaluate(D.conditionStructure,lambda index:K(A,index));H=str(F).upper()if F is not G else'UNKNOWN';E=C.AUDIENCE_EVALUATION_RESULT.format(A,H);B.debug(E);return F
	F=condition_tree_evaluator.evaluate(E,L);F=F or False;A=C.AUDIENCE_EVALUATION_RESULT_COMBINED.format(H,str(F).upper());B.info(A);D.append(A);return F,D