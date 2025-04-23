_C=True
_B=False
_A=None
from.condition import ConditionOperatorTypes
def and_evaluator(conditions,leaf_evaluator):
	" Evaluates a list of conditions as if the evaluator had been applied\n  to each entry and the results AND-ed together.\n\n  Args:\n    conditions: List of conditions ex: [operand_1, operand_2].\n    leaf_evaluator: Function which will be called to evaluate leaf condition values.\n\n  Returns:\n    Boolean:\n      - True if all operands evaluate to True.\n      - False if a single operand evaluates to False.\n    None: if conditions couldn't be evaluated.\n  ";A=_B
	for C in conditions:
		B=evaluate(C,leaf_evaluator)
		if B is _B:return _B
		if B is _A:A=_C
	return _A if A else _C
def or_evaluator(conditions,leaf_evaluator):
	" Evaluates a list of conditions as if the evaluator had been applied\n  to each entry and the results OR-ed together.\n\n  Args:\n    conditions: List of conditions ex: [operand_1, operand_2].\n    leaf_evaluator: Function which will be called to evaluate leaf condition values.\n\n  Returns:\n    Boolean:\n      - True if any operand evaluates to True.\n      - False if all operands evaluate to False.\n    None: if conditions couldn't be evaluated.\n  ";A=_B
	for C in conditions:
		B=evaluate(C,leaf_evaluator)
		if B is _C:return _C
		if B is _A:A=_C
	return _A if A else _B
def not_evaluator(conditions,leaf_evaluator):
	" Evaluates a list of conditions as if the evaluator had been applied\n  to a single entry and NOT was applied to the result.\n\n  Args:\n    conditions: List of conditions ex: [operand_1, operand_2].\n    leaf_evaluator: Function which will be called to evaluate leaf condition values.\n\n  Returns:\n    Boolean:\n      - True if the operand evaluates to False.\n      - False if the operand evaluates to True.\n    None: if conditions is empty or condition couldn't be evaluated.\n  ";A=conditions
	if not len(A)>0:return
	B=evaluate(A[0],leaf_evaluator);return _A if B is _A else not B
EVALUATORS_BY_OPERATOR_TYPE={ConditionOperatorTypes.AND:and_evaluator,ConditionOperatorTypes.OR:or_evaluator,ConditionOperatorTypes.NOT:not_evaluator}
def evaluate(conditions,leaf_evaluator):
	" Top level method to evaluate conditions.\n\n  Args:\n    conditions: Nested array of and/or conditions, or a single leaf condition value of any type.\n                Example: ['and', '0', ['or', '1', '2']]\n    leaf_evaluator: Function which will be called to evaluate leaf condition values.\n\n  Returns:\n    Boolean: Result of evaluating the conditions using the operator rules and the leaf evaluator.\n    None: if conditions couldn't be evaluated.\n\n  ";B=leaf_evaluator;A=conditions
	if isinstance(A,list):
		if A[0]in list(EVALUATORS_BY_OPERATOR_TYPE.keys()):return EVALUATORS_BY_OPERATOR_TYPE[A[0]](A[1:],B)
		else:return EVALUATORS_BY_OPERATOR_TYPE[ConditionOperatorTypes.OR](A,B)
	C=A;return B(C)