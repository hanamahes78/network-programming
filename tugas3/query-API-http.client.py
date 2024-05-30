import sys
import unittest
from io import StringIO
from unittest import mock
from unittest.mock import patch, MagicMock
import http.client
import json

def get_post_count():
    # Create HTTPConnection to jsonplaceholder.typicode.com
    conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")

    # Send GET request for /posts
    conn.request("GET", "/posts")

    # Get response
    response = conn.getresponse()

    # Read response data
    data = response.read().decode("utf-8")

    # Parse response as JSON
    posts = json.loads(data)

    # Count number of posts containing word "voluptate" in the body
    count = sum(1 for post in posts if "voluptate" in post.get(
        "body", "").lower())

    # Close connection
    conn.close()

    return count

class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(
            f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestGetPostCount(unittest.TestCase):
    @patch('http.client.HTTPSConnection')
    def test_get_post_count(self, mock_conn):
        # Mock the response
        mock_response = mock.Mock()
        mock_response.read.return_value = b'[{"body": "voluptate"}, {"body": "non-voluptate"}]'
        mock_conn.return_value.getresponse.return_value = mock_response

        # Call the function under test
        result = get_post_count()

        # Assert the connection was made with the correct arguments
        mock_conn.assert_called_once_with('jsonplaceholder.typicode.com')
        print(f"connection called with: {mock_conn.call_args}")

        mock_conn.return_value.request.assert_called_once_with("GET", "/posts")
        print(
            f"request called with: {mock_conn.return_value.request.call_args}")

        mock_response.read.assert_called_once()
        print(f"response read called with: {mock_response.read.return_value}")

        mock_conn.return_value.close.assert_called_once()
        print(f"connection closed: {mock_conn.return_value.close.call_args}")

        # Assert the result
        assert_equal(result, 2)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        post_count = get_post_count()
        print(post_count)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
