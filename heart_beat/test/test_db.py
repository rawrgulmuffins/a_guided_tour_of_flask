#pylint: disable=missing-docstring

import unittest
import uuid

import heart_beat
from heart_beat.views import insert_ping_data
from heart_beat.models import DiagnosticPingData

class TestDBOperations(unittest.TestCase):
    """
    Test all code which modifies or selects from the database.
    """
    maxDiff = None

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
        example_json_data = {
            "client_start_time": "1429572087",
            "logset_gather_time": "1429572066",
            "onefs_version": "7.2.0.0",
            "esrs_enabled": "False",
            "tool_version": heart_beat.app.config["VERSION"],
            "sr_number": "12345678910"}
        insert_ping_data(example_json_data)
        actual_data = DiagnosticPingData.query.filter_by(ping_id=1).first()
        expected_data = {
            "ping_id": 1,
            "client_start_time": "2015-04-20 23:21:27",
            "logset_gather_time": "2015-04-20 23:21:06",
            "onefs_version": "7.2.0.0",
            "esrs_enabled": False,
            "tool_version": heart_beat.app.config["VERSION"],
            "sr_number": 12345678910}
        actual_data = actual_data.get_dict()
        del actual_data["db_insert_time"] # going to be different every time.
        self.assertEqual(expected_data, actual_data)
