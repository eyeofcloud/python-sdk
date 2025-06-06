# Copyright 2021, Eyeofcloud
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from eyeofcloud.config_manager import PollingConfigManager
from eyeofcloud.error_handler import NoOpErrorHandler
from eyeofcloud.event_dispatcher import EventDispatcher
from eyeofcloud.notification_center import NotificationCenter
from eyeofcloud.eyeofcloud_factory import EyeofcloudFactory
from eyeofcloud.user_profile import UserProfileService
from . import base


@mock.patch('requests.get')
class EyeofcloudFactoryTest(base.BaseTest):
    def setUp(self):
        self.datafile = '{ revision: "42" }'
        self.error_handler = NoOpErrorHandler()
        self.mock_client_logger = mock.MagicMock()
        self.notification_center = NotificationCenter(self.mock_client_logger)
        self.event_dispatcher = EventDispatcher()
        self.user_profile_service = UserProfileService()

    def test_default_instance__should_create_config_manager_when_sdk_key_is_given(self, _):
        eyeofcloud_instance = EyeofcloudFactory.default_instance('sdk_key')
        self.assertIsInstance(eyeofcloud_instance.config_manager, PollingConfigManager)

    def test_default_instance__should_create_config_manager_when_params_are_set_valid(self, _):
        EyeofcloudFactory.set_polling_interval(40)
        EyeofcloudFactory.set_blocking_timeout(5)
        EyeofcloudFactory.set_flush_interval(30)
        EyeofcloudFactory.set_batch_size(10)
        eyeofcloud_instance = EyeofcloudFactory.default_instance('sdk_key', datafile=self.datafile)
        # Verify that values set in EyeofcloudFactory are being used inside config manager.
        self.assertEqual(eyeofcloud_instance.config_manager.update_interval, 40)
        self.assertEqual(eyeofcloud_instance.config_manager.blocking_timeout, 5)
        # Verify values set for batch_size and flush_interval
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 30)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 10)

    def test_default_instance__should_create_config_set_default_values_params__invalid(self, _):
        EyeofcloudFactory.set_polling_interval(-40)
        EyeofcloudFactory.set_blocking_timeout(-85)
        EyeofcloudFactory.set_flush_interval(30)
        EyeofcloudFactory.set_batch_size(10)

        eyeofcloud_instance = EyeofcloudFactory.default_instance('sdk_key', datafile=self.datafile)
        # Verify that values set in EyeofcloudFactory are not being used inside config manager.
        self.assertEqual(eyeofcloud_instance.config_manager.update_interval, 300)
        self.assertEqual(eyeofcloud_instance.config_manager.blocking_timeout, 10)
        # Verify values set for batch_size and flush_interval
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 30)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 10)

    def test_default_instance__should_create_http_config_manager_with_the_same_components_as_the_instance(self, _):
        eyeofcloud_instance = EyeofcloudFactory.default_instance('sdk_key', None)
        self.assertEqual(eyeofcloud_instance.error_handler, eyeofcloud_instance.config_manager.error_handler)
        self.assertEqual(eyeofcloud_instance.logger, eyeofcloud_instance.config_manager.logger)
        self.assertEqual(eyeofcloud_instance.notification_center,
                         eyeofcloud_instance.config_manager.notification_center)

    def test_custom_instance__should_set_input_values_when_sdk_key_polling_interval_and_blocking_timeout_are_given(
            self, _):
        EyeofcloudFactory.set_polling_interval(50)
        EyeofcloudFactory.set_blocking_timeout(10)

        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key', None, self.event_dispatcher,
                                                                self.mock_client_logger, self.error_handler, False,
                                                                self.user_profile_service, None,
                                                                self.notification_center)

        self.assertEqual(eyeofcloud_instance.config_manager.update_interval, 50)
        self.assertEqual(eyeofcloud_instance.config_manager.blocking_timeout, 10)

    def test_custom_instance__should_set_default_values_when_sdk_key_polling_interval_and_blocking_timeout_are_invalid(
            self, _):
        EyeofcloudFactory.set_polling_interval(-50)
        EyeofcloudFactory.set_blocking_timeout(-10)
        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key', None, self.event_dispatcher,
                                                                self.mock_client_logger, self.error_handler, False,
                                                                self.user_profile_service, None,
                                                                self.notification_center)
        self.assertEqual(eyeofcloud_instance.config_manager.update_interval, 300)
        self.assertEqual(eyeofcloud_instance.config_manager.blocking_timeout, 10)

    def test_custom_instance__should_take_event_processor_when_flush_interval_and_batch_size_are_set_valid(self, _):
        EyeofcloudFactory.set_flush_interval(5)
        EyeofcloudFactory.set_batch_size(100)

        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key')
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 5)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 100)

    def test_custom_instance__should_take_event_processor_set_default_values_when_flush_int_and_batch_size_are_invalid(
            self, _):
        EyeofcloudFactory.set_flush_interval(-50)
        EyeofcloudFactory.set_batch_size(-100)
        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key')
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 30)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 10)

    def test_custom_instance__should_assign_passed_components_to_both_the_instance_and_config_manager(self, _):
        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key', None, self.event_dispatcher,
                                                                self.mock_client_logger, self.error_handler, False,
                                                                self.user_profile_service, None,
                                                                self.notification_center)
        # Config manager assertion
        self.assertEqual(self.error_handler, eyeofcloud_instance.config_manager.error_handler)
        self.assertEqual(self.mock_client_logger, eyeofcloud_instance.config_manager.logger)
        self.assertEqual(self.notification_center,
                         eyeofcloud_instance.config_manager.notification_center)

        # instance assertions
        self.assertEqual(self.error_handler, eyeofcloud_instance.error_handler)
        self.assertEqual(self.mock_client_logger, eyeofcloud_instance.logger)
        self.assertEqual(self.notification_center,
                         eyeofcloud_instance.notification_center)

    def test_set_batch_size_and_set_flush_interval___should_set_values_valid_or_invalid(self, _):

        # pass valid value so no default value is set
        EyeofcloudFactory.set_flush_interval(5)
        EyeofcloudFactory.set_batch_size(100)
        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key')
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 5)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 100)

        # pass invalid value so set default value
        EyeofcloudFactory.set_flush_interval('test')
        EyeofcloudFactory.set_batch_size('test')
        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key')
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 30)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 10)

        EyeofcloudFactory.set_flush_interval(20.5)
        EyeofcloudFactory.set_batch_size(85.5)
        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key')
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 20)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 10)

        EyeofcloudFactory.set_flush_interval(None)
        EyeofcloudFactory.set_batch_size(None)
        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key')
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 30)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 10)

        EyeofcloudFactory.set_flush_interval(True)
        EyeofcloudFactory.set_batch_size(True)
        eyeofcloud_instance = EyeofcloudFactory.custom_instance('sdk_key')
        self.assertEqual(eyeofcloud_instance.event_processor.flush_interval.seconds, 30)
        self.assertEqual(eyeofcloud_instance.event_processor.batch_size, 10)
