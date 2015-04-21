"""
This file will run automated tests to see if heart_beat is still running as
expected.

You can also choose to manually test heart_beat using:

curl --request POST 'http://localhost:5000/ping' --data-binary @test/test_data.json --header "Content-Type:application/json"
"""
import os
import tempfile
import uuid
import unittest
import json
from unittest import mock

import heart_beat

class TestURLMapping(unittest.TestCase):
    """
    Ensure that we have the correct get and post end points.
    """
    def setUp(self):
        # Putting things in tmp couples this project to Unix.
        db_uri = 'sqlite:////tmp/{}'.format(uuid.uuid1())
        heart_beat.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        heart_beat.app.config['TESTING'] = True
        self.test_app = heart_beat.app.test_client()
        heart_beat.setup_db()

    def tearDown(self):
        heart_beat.teardown_db()
        heart_beat.load_configs()

    def test_version_get_request(self):
        response = self.test_app.get('/version', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_version_returns_configured_version(self):
        heart_beat.app.config['VERSION'] = b'Testing'
        response = self.test_app.get('/version', content_type='html/text')
        self.assertEqual(response.data, heart_beat.app.config['VERSION'])

    def test_ping_fails_on_get_request(self):
        response = self.test_app.get('/ping', content_type='html/text')
        self.assertEqual(response.status_code, 405)

    def test_ping_post_request_bad_content_type(self):
        response = self.test_app.post('/ping', content_type='html/text')
        self.assertEqual(response.status_code, 406)

    def test_ping_post_request_correct_content_type_no_json(self):
        response = self.test_app.post('/ping', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_ping_post_valid_content_type_valid_data(self):
        example_json_data = {
            "client_start_time":"1429572087",
            "logset_gather_time":"1429572066",
            "onefs_version":"7.2.0.0",
            "esrs_enabled":"False",
            "tool_version":"0.0.0.1",
            "sr_number":"12345678910"}
        example_json_data = json.dumps(example_json_data)
        response = self.test_app.post(
            '/ping',
            content_type='application/json',
            data=example_json_data)
        self.assertEqual(response.data, b"success")
        self.assertEqual(response.status_code, 200)

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
        heart_beat.app.config['VERSION'] = b'MisMatched'
        example_json_data = {
            "client_start_time":"1429572087",
            "logset_gather_time":"1429572066",
            "onefs_version":"7.2.0.0",
            "esrs_enabled":"False",
            "tool_version":"0.0.0.1",
            "sr_number":"12345678910"}
        example_json_data = json.dumps(example_json_data)
        response = self.test_app.post(
            '/ping',
            content_type='application/json',
            data=example_json_data)
        self.assertEqual(response.status_code, 400)
        expected_message = \
            "Server version ({}) is not client version ({})".format(
                "0.0.0.1",
                heart_beat.app.config['VERSION'],)
        self.assertEqual(response.data, str.encode(expected_message))

    def test_ping_post_non_epoch_time_client_start(self):
        example_json_data = {
            "client_start_time":"2014/12/02",
            "logset_gather_time":"1429572066",
            "onefs_version":"7.2.0.0",
            "esrs_enabled":"False",
            "tool_version":"0.0.0.1",
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
            "tool_version":"0.0.0.1",
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
            "tool_version":"0.0.0.1",
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
            "tool_version":"0.0.0.1",
            "sr_number":"foobar"}
        example_json_data = json.dumps(example_json_data)
        response = self.test_app.post(
            '/ping',
            content_type='application/json',
            data=example_json_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"sr_number is not a integer")

class TestDBOperations(unittest.TestCase):
    """
    Test all code which modifies or selects from the database.
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
    
    def test_valid_dict_insertion(self):
        pass

if __name__ == '__main__':
    unittest.main()
