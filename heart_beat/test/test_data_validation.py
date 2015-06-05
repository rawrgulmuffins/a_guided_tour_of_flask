#pylint: disable=missing-docstring
#pylint: disable=invalid-name

import uuid
import unittest
import json

import heart_beat

class TestPostData(unittest.TestCase):
    """
    Test both valid and invalid ping data from post requests.
    """
    def setUp(self):
        db_uri = 'sqlite:////tmp/{}'.format(uuid.uuid1())
        heart_beat.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        heart_beat.app.config['TESTING'] = True
        self.test_app = heart_beat.app.test_client()
        heart_beat.setup_db()

    def tearDown(self):
        heart_beat.teardown_db()
        heart_beat.load_configs()

    def test_ping_post_mismatched_tool_version_data(self):
        actual_version = heart_beat.app.config["VERSION"]
        example_json_data = {
            "client_start_time":"1429572087",
            "logset_gather_time":"1429572066",
            "onefs_version":"7.2.0.0",
            "esrs_enabled":"False",
            "tool_version":heart_beat.app.config["VERSION"],
            "sr_number":"12345678910"}
        example_json_data = json.dumps(example_json_data)
        heart_beat.app.config['VERSION'] = b'MisMatched'
        response = self.test_app.post(
            '/ping',
            content_type='application/json',
            data=example_json_data)
        self.assertEqual(response.status_code, 400)
        expected_message = \
            "Server version ({}) is not client version ({})".format(
                actual_version,
                heart_beat.app.config['VERSION'],)
        self.assertEqual(response.data, str.encode(expected_message))

    def test_ping_post_non_epoch_time_client_start(self):
        example_json_data = {
            "client_start_time":"2014/12/02",
            "logset_gather_time":"1429572066",
            "onefs_version":"7.2.0.0",
            "esrs_enabled":"False",
            "tool_version":heart_beat.app.config["VERSION"],
            "sr_number":"12345678910"}
        example_json_data = json.dumps(example_json_data)
        response = self.test_app.post(
            '/ping',
            content_type='application/json',
            data=example_json_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Given Non-unix timestamps")

    def test_ping_post_non_epoch_time_logset_gather(self):
        example_json_data = {
            "client_start_time":"1429572066",
            "logset_gather_time":"2014/12/02",
            "onefs_version":"7.2.0.0",
            "esrs_enabled":"False",
            "tool_version":heart_beat.app.config["VERSION"],
            "sr_number":"12345678910"}
        example_json_data = json.dumps(example_json_data)
        response = self.test_app.post(
            '/ping',
            content_type='application/json',
            data=example_json_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Given Non-unix timestamps")

    def test_ping_post_esrs_enabled_not_bool(self):
        example_json_data = {
            "client_start_time":"1429572066",
            "logset_gather_time":"1429572066",
            "onefs_version":"7.2.0.0",
            "esrs_enabled":"Not Bool",
            "tool_version":heart_beat.app.config["VERSION"],
            "sr_number":"12345678910"}
        example_json_data = json.dumps(example_json_data)
        response = self.test_app.post(
            '/ping',
            content_type='application/json',
            data=example_json_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"esrs_enabled not a bool")

    def test_ping_post_sr_number_not_integer(self):
        example_json_data = {
            "client_start_time":"1429572066",
            "logset_gather_time":"1429572066",
            "onefs_version":"7.2.0.0",
            "esrs_enabled":"True",
            "tool_version":heart_beat.app.config["VERSION"],
            "sr_number":"foobar"}
        example_json_data = json.dumps(example_json_data)
        response = self.test_app.post(
            '/ping',
            content_type='application/json',
            data=example_json_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"sr_number is not a integer")
