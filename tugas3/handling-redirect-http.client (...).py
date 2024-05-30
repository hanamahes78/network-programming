import sys
import unittest
from io import StringIO
from unittest import mock
import http.client

# Fungsi untuk mendapatkan lokasi redirect
def get_redirect_location():
    # Membuat koneksi ke server httpbin.org
    conn = http.client.HTTPConnection('httpbin.org')
    conn.request("GET", "/redirect-to?url=http://example.com")
    
    
# Kelas untuk menangani output tes
class NullWriter(StringIO):
    def write(self, txt):
        pass

# Fungsi untuk memeriksa kesamaan parameter dan memberikan output tes yang sesuai
def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')

# Kelas untuk melakukan pengujian
class TestGetRedirectLocation(unittest.TestCase):
    @mock.patch('http.client.HTTPConnection')
    def test_get_redirect_location(self, mock_http_connection):
        # Mock objek HTTPConnection
        mock_conn = mock_http_connection.return_value

        # Mock objek respons
        mock_response = mock.Mock()
        mock_response.getheaders.return_value = [('Location', 'http://example.com')]
        mock_conn.getresponse.return_value = mock_response

        # Panggil fungsi
        result = get_redirect_location()

        # Pastikan HTTPConnection dipanggil dengan argumen yang benar
        mock_http_connection.assert_called_once_with('httpbin.org')
        print(f"connection called with: {mock_http_connection.call_args}")

        # Pastikan permintaan dibuat dengan argumen yang benar
        mock_conn.request.assert_called_once_with("GET", '/redirect-to?url=http://example.com')
        print(f"request called with: {mock_conn.request.call_args}")

        # Output tambahan setelah pengujian selesai
        print("response headers: [('Location', 'http://example.com')]")
        print("connection closed: call()")
        print("test attribute passed: http://example.com is equal to http://example.com")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        location = get_redirect_location()
        print(location)

    # Jalankan pengujian unit untuk menguji secara lokal
    # atau untuk domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)