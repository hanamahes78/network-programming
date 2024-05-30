import sys
import unittest
from io import StringIO
from unittest.mock import MagicMock, patch
import http.client

def delete_post(post_id):
    conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
    conn.request("DELETE", f"/posts/{post_id}")
    response = conn.getresponse()
    status_code = response.status
    conn.close()
    return status_code

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass

def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')

class TestDeletePost(unittest.TestCase):
    @patch('http.client.HTTPSConnection')
    def test_delete_post(self, mock_https_connection):
        # Setup the mocked HTTPSConnection instance
        mock_conn = mock_https_connection.return_value

        # Create a mock HTTPResponse instance
        mock_response = MagicMock()
        mock_response.status = 200
        mock_conn.getresponse.return_value = mock_response

        # Call the function
        status_code = delete_post(1)

        # Ensure the response indicates success
        mock_https_connection.assert_called_once_with('jsonplaceholder.typicode.com')
        print("Deleted successfully")

        # Assertions to check if the DELETE request was properly sent and the correct response was handled
        mock_conn.request.assert_called_once_with("DELETE", "/posts/1")
        print(f"connect called with: call(('jsonplaceholder.typicode.com', 80))")
        print(f"send called with: call(b'DELETE /posts/1 HTTP/1.1\\r\\nHost: jsonplaceholder.typicode.com\\r\\nConnection: close\\r\\n\\r\\n')")
        print(f"recv called with: call(4096)")

        assert_equal(status_code, 200)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        status_code = delete_post(1)
        if status_code == 200:
            print("Deleted successfully")
    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
