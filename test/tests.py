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
from unittest import mock

import heart_beat

class TestURLMapping(unittest.TestCase):
    """
    Ensure that we have the correct get and post end points.
    """
    def setUp(self):
        db_uri = 'sqlite:////tmp/{}'.format(uuid.uuid1())
        heart_beat.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        heart_beat.app.config['TESTING'] = True
        self.app = heart_beat.app.test_client()
        heart_beat.init_db()

    def tearDown(self):
        heart_beat.tear_down_db()

    def test_version_get_request():
        pass

    def test_ping_fails_on_get_request():
        pass

    def test_ping_post_request_bad_content_type():
        pass

    def test_ping_post_request_bad_correct_content_type():
        pass

class TestPostData(unittest.TestCase):
    """
    Test both valid and invalid ping data from post requests.
    """
    def setUp(self):
        db_uri = 'sqlite:////tmp/{}'.format(uuid.uuid1())
        heart_beat.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        heart_beat.app.config['TESTING'] = True
        self.app = heart_beat.app.test_client()
        heart_beat.init_db()

    def tearDown(self):
        heart_beat.tear_down_db()

    def test_ping_post_valid_data():
        pass

    def test_ping_post_mismatched_tool_version_data():
        pass

    def test_ping_post_non_epoch_time_client_start():
        pass

    def test_ping_post_non_epoch_time_logset_gather():
        pass

    def test_ping_post_esrs_enabled_not_bool():
        pass

    def test_ping_post_sr_number_not_integer():
        pass

class TestDBOperations(unittest.TestCase):
    """
    Test all code which modifies or selects from the database.
    """
    def setUp(self):
        db_uri = 'sqlite:////tmp/{}'.format(uuid.uuid1())
        heart_beat.app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        heart_beat.app.config['TESTING'] = True
        self.app = heart_beat.app.test_client()
        heart_beat.init_db()

    def tearDown(self):
        heart_beat.tear_down_db()
    
    def test_valid_dict_insertion(self):
        pass

if __name__ == '__main__':
    unittest.main()
