import json

import unittest
from flask import Flask
from flask_session import Session
import mongomock


def read_json_file(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def is_dict_json_friendly(dict_value):
    try:
        json.dumps(dict_value)
    except TypeError:
        return False
    return True


class BaseTestClass(unittest.TestCase):
    app = None
    mongo_client = None

    @classmethod
    def setUpClass(cls):
        cls.app = Flask('__test__')
        cls.app.config["TESTING"] = True
        cls.app.config["MONGO_URI"] = "mongomock://localhost"
        cls.app.config['SESSION_TYPE'] = 'filesystem'
        Session(cls.app)
        cls.client = cls.app.test_client()
        cls.mongo_client = mongomock.MongoClient()
        cls.db = cls.mongo_client.test_database

    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.close()

    def setUp(self):
        # App context for each test
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Pop the app context after each test
        self.app_context.pop()
        with self.client.session_transaction() as test_session:
            test_session.clear()
