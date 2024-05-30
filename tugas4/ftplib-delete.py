import ftplib
import sys
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock


def delete_file_from_ftp(host, username, password, file_to_delete):
    # Create an FTP object and connect to the FTP server
    ftp = ftplib.FTP(host)

    # Log in to the server
    welcome_msg = ftp.getwelcome()
    print(welcome_msg)
    ftp.login(username, password)
    print("230 Login successful.")

    # Use delete to remove the file from the server
    ftp.delete(file_to_delete)
    print("250 File deleted successfully.")

    # Properly close the connection
    ftp.quit()
    print("221 Goodbye.")

    # Return a confirmation message
    return f"The file {file_to_delete} has been successfully deleted."


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestDeleteFileFromFTP(unittest.TestCase):
    @patch('ftplib.FTP')
    def test_delete_file_successfully(self, mock_ftp):
        # Arrange
        host = 'localhost'
        username = 'user'
        password = '123'
        file_to_delete = 'unwantedfile.txt'
        expected_result = f"The file {file_to_delete} has been successfully deleted."
        expected_welcome_msg = "220-FileZilla Server 1.7.0\r\n220 Please visit https://filezilla-project.org/"
        expected_login_msg = "230 Login successful."
        expected_delete_msg = "250 File deleted successfully."
        expected_quit_msg = "221 Goodbye."

        # Mock FTP instance
        ftp_instance = mock_ftp.return_value
        ftp_instance.getwelcome.return_value = expected_welcome_msg
        ftp_instance.login.return_value = expected_login_msg
        ftp_instance.delete.return_value = expected_delete_msg
        ftp_instance.quit.return_value = expected_quit_msg

        # Act
        result = delete_file_from_ftp(host, username, password, file_to_delete)

        # Assert
        mock_ftp.assert_called_once_with(host)
        ftp_instance.getwelcome.assert_called_once()
        print(f"login called with {ftp_instance.login.call_args}")
        print(f"delete called with {ftp_instance.delete.call_args}")
        ftp_instance.login.assert_called_once_with(username, password)
        ftp_instance.delete.assert_called_once_with(file_to_delete)
        ftp_instance.quit.assert_called_once()
        assert_equal(result, expected_result)
        assert_equal(ftp_instance.getwelcome(), expected_welcome_msg)
        assert_equal(ftp_instance.login(username, password), expected_login_msg)
        assert_equal(ftp_instance.delete(file_to_delete), expected_delete_msg)
        assert_equal(ftp_instance.quit(), expected_quit_msg)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        host = 'localhost'
        username = 'user'
        password = '123'
        file_to_delete = 'unwantedfile.txt'

        result = delete_file_from_ftp(host, username, password, file_to_delete)
        print(result)
    else:
        runner = unittest.TextTestRunner(stream=NullWriter())
        unittest.main(testRunner=runner, exit=False)