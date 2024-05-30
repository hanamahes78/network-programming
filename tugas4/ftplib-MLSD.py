import sys
import unittest
from io import StringIO
from unittest.mock import patch
from ftplib import FTP

def list_ftp_directory(host, username, password, directory):
    # Create an FTP object and connect to the FTP server
    ftp = FTP(host)

    # Log in to the server with the provided username and password
    welcome_msg = ftp.getwelcome()
    print(welcome_msg)
    login_msg = ftp.login(username, password)
    print(login_msg)

    # Use mlsd to get detailed list of files in the specified directory
    print(f"Contents of directory {directory}:")
    for entry in ftp.mlsd(directory):
        name, facts = entry
        print(f"{name}:")
        for key, value in facts.items():
            print(f"  {key}: {value}")

    # Properly close the connection
    quit_msg = ftp.quit()
    print(quit_msg)

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass

def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')

class TestFTPListDirectory(unittest.TestCase):
    @patch('__main__.FTP')
    def test_list_ftp_directory(self, MockFTP):
        host = 'localhost'
        username = 'user'
        password = '123'
        directory = '/'
        expected_welcome_msg = "220-FileZilla Server 1.7.0\n220 Please visit https://filezilla-project.org/"
        expected_login_msg = "230 Login successful."
        expected_quit_msg = "221 Goodbye."

        # Set up the mock FTP object
        mock_ftp_instance = MockFTP.return_value
        mock_ftp_instance.getwelcome.return_value = expected_welcome_msg
        mock_ftp_instance.login.return_value = expected_login_msg
        mock_ftp_instance.mlsd.return_value = [
            ('file1.txt', {'type': 'file', 'size': '32', 'modify': '20210515094500', 'perms': 'awr'}),
            ('file2.txt', {'type': 'file', 'size': '174', 'modify': '20210516094500', 'perms': 'awr'}),
        ]
        mock_ftp_instance.quit.return_value = expected_quit_msg

        # Capture printed output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            list_ftp_directory(host, username, password, directory)

            # Get printed output
            printed_output = mock_stdout.getvalue().strip().split('\n')

        # Define the expected output
        expected_output = [
            "220-FileZilla Server 1.7.0",
            "220 Please visit https://filezilla-project.org/",
            "230 Login successful.",
            "Contents of directory /:",
            "file1.txt:",
            "  type: file",
            "  size: 32",
            "  modify: 20210515094500",
            "  perms: awr",
            "file2.txt:",
            "  type: file"
        ]

        # Verify the mock FTP methods were called correctly
        MockFTP.assert_called_with(host)
        mock_ftp_instance.login.assert_called_with(username, password)
        print(f"login called with {mock_ftp_instance.login.call_args}")

        mock_ftp_instance.mlsd.assert_called_with(directory)
        print(f"mlsd called with {mock_ftp_instance.mlsd.call_args}")
        mock_ftp_instance.quit.assert_called()

        # Verify the printed output
        for actual, expected in zip(printed_output, expected_output):
            assert_equal(actual, expected)

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        host = 'localhost'
        username = 'user'
        password = '123'
        directory = '.'
        list_ftp_directory(host, username, password, directory)
    else:
        runner = unittest.TextTestRunner(stream=NullWriter())
        unittest.main(testRunner=runner, exit=False)