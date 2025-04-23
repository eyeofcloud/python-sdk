from.helpers import enums
from.import logger as eyeofcloud_logger
NOTIFICATION_TYPES=tuple(getattr(enums.NotificationTypes,A)for A in dir(enums.NotificationTypes)if not A.startswith('__'))
class NotificationCenter:
	' Class encapsulating methods to manage notifications and their listeners.\n  The enums.NotificationTypes includes predefined notifications.'
	def __init__(A,logger=None):
		A.listener_id=1;A.notification_listeners={}
		for B in NOTIFICATION_TYPES:A.notification_listeners[B]=[]
		A.logger=eyeofcloud_logger.adapt_logger(logger or eyeofcloud_logger.NoOpLogger())
	def add_notification_listener(A,notification_type,notification_callback):
		' Add a notification callback to the notification center for a given notification type.\n\n    Args:\n      notification_type: A string representing the notification type from helpers.enums.NotificationTypes\n      notification_callback: Closure of function to call when event is triggered.\n\n    Returns:\n      Integer notification ID used to remove the notification or\n      -1 if the notification listener has already been added or\n      if the notification type is invalid.\n    ';C=notification_callback;B=notification_type
		if B not in NOTIFICATION_TYPES:A.logger.error('Invalid notification_type: {} provided. Not adding listener.'.format(B));return-1
		for(F,D)in A.notification_listeners[B]:
			if D==C:A.logger.error('Listener has already been added. Not adding it again.');return-1
		A.notification_listeners[B].append((A.listener_id,C));E=A.listener_id;A.listener_id+=1;return E
	def remove_notification_listener(C,notification_id):
		' Remove a previously added notification callback.\n\n    Args:\n      notification_id: The numeric id passed back from add_notification_listener\n\n    Returns:\n      The function returns boolean true if found and removed, false otherwise.\n    '
		for A in C.notification_listeners.values():
			B=list(filter(lambda tup:tup[0]==notification_id,A))
			if len(B)>0:A.remove(B[0]);return True
		return False
	def clear_notification_listeners(B,notification_type):
		' Remove notification listeners for a certain notification type.\n\n    Args:\n      notification_type: String denoting notification type.\n    ';A=notification_type
		if A not in NOTIFICATION_TYPES:B.logger.error('Invalid notification_type: {} provided. Not removing any listener.'.format(A))
		B.notification_listeners[A]=[]
	def clear_notifications(A,notification_type):' (DEPRECATED since 3.2.0, use clear_notification_listeners)\n    Remove notification listeners for a certain notification type.\n\n    Args:\n      notification_type: key to the list of notifications .helpers.enums.NotificationTypes\n    ';A.clear_notification_listeners(notification_type)
	def clear_all_notification_listeners(A):
		' Remove all notification listeners. '
		for B in A.notification_listeners.keys():A.clear_notification_listeners(B)
	def clear_all_notifications(A):' (DEPRECATED since 3.2.0, use clear_all_notification_listeners)\n    Remove all notification listeners. ';A.clear_all_notification_listeners()
	def send_notifications(B,notification_type,*C):
		' Fires off the notification for the specific event.  Uses var args to pass in a\n        arbitrary list of parameter according to which notification type was fired.\n\n    Args:\n      notification_type: Type of notification to fire (String from .helpers.enums.NotificationTypes)\n      args: Variable list of arguments to the callback.\n    ';A=notification_type
		if A not in NOTIFICATION_TYPES:B.logger.error('Invalid notification_type: {} provided. Not triggering any notification.'.format(A));return
		if A in B.notification_listeners:
			for(E,D)in B.notification_listeners[A]:
				try:D(*C)
				except:B.logger.exception('Unknown problem when sending "{}" type notification.'.format(A))