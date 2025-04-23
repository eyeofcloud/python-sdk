_A=None
from.import enums
import math,numbers
REVENUE_METRIC_TYPE='revenue'
NUMERIC_METRIC_TYPE='value'
def get_revenue_value(event_tags):
	A=event_tags
	if A is _A:return
	if not isinstance(A,dict):return
	if REVENUE_METRIC_TYPE not in A:return
	B=A[REVENUE_METRIC_TYPE]
	if isinstance(B,bool):return
	if not isinstance(B,numbers.Integral):return
	return B
def get_numeric_value(event_tags,logger=_A):
	"\n  A smart getter of the numeric value from the event tags.\n\n  Args:\n      event_tags: A dictionary of event tags.\n      logger: Optional logger.\n\n  Returns:\n      A float numeric metric value is returned when the provided numeric\n      metric value is in the following format:\n          - A string (properly formatted, e.g., no commas)\n          - An integer\n          - A float or double\n      None is returned when the provided numeric metric values is in\n      the following format:\n          - None\n          - A boolean\n          - inf, -inf, nan\n          - A string not properly formatted (e.g., '1,234')\n          - Any values that cannot be cast to a float (e.g., an array or dictionary)\n  ";D=event_tags;B=logger;C=_A;A=_A
	if D is _A:return A
	elif not isinstance(D,dict):
		if B:B.log(enums.LogLevels.ERROR,'Event tags is not a dictionary.')
		return A
	elif NUMERIC_METRIC_TYPE not in D:return A
	else:
		A=D[NUMERIC_METRIC_TYPE]
		try:
			if isinstance(A,(numbers.Integral,float,str)):
				E=float(A)
				if not isinstance(E,float)or math.isnan(E)or math.isinf(E):C='Provided numeric value {} is in an invalid format.'.format(A);A=_A
				elif isinstance(A,bool):C='Provided numeric value is a boolean, which is an invalid format.';A=_A
				else:A=E
			else:C='Numeric metric value is not in integer, float, or string form.';A=_A
		except ValueError:C='Value error while casting numeric metric value to a float.';A=_A
	if B and C:B.log(enums.LogLevels.DEBUG,C)
	if A is not _A:
		if B:B.log(enums.LogLevels.INFO,'The numeric metric value {} will be sent to results.'.format(A))
	elif B:B.log(enums.LogLevels.WARNING,'The provided numeric metric value {} is in an invalid format and will not be sent to results.'.format(A))
	return A