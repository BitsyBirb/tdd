"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

from src.counter import app

from src import status

# Shoudl be in counter.py instead
#from flask import Flask
#app = Flask(__name__)


class CounterTest(TestCase):
    """Counter Tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter."""
        #client = app.test_client()
        result = self.client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """Should successfully update a counter"""
        # Make a call to create a counter
        result = self.client.post('/counters/test')
        # Ensure that it returned a successful value code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # Check the counter value as a baseline
        self.assertEqual(result.json['test'], 0)
        # Make a call to update the counter that we just created
        toCompare = self.client.put('/counters/test')
        # Ensure that it returned a successful return code
        self.assertEqual(toCompare.status_code, status.HTTP_200_OK)
        # Check that the counter value is one more than the baseline measured in step 3
        self.assertEqual(result.json['test'] + 1, toCompare.json['test'])

    def test_get_a_counter(self):
        """Should successfully get a counter"""
        result = self.client.post('/counters/getTest')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        retrieved = self.client.get('/counters/getTest')
        self.assertEqual(retrieved.status_code, status.HTTP_200_OK)
        # Also want to make sure that the value in the counter itself is 0 as it was just made, compare to OG
        self.assertEqual(retrieved.json['getTest'], result.json['getTest'])

    def test_updating_nonexistent_counter(self):
        """Should successfully get 404 on an attempt to update a missing counter"""
        result = self.client.put('/counters/narnia')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_getting_nonexistent_counter(self):
        """Should successfully return 404 status on attempt to get missing counter"""
        result = self.client.get('counters/narnia')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)