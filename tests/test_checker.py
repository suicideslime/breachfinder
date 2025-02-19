import unittest
from unittest.mock import patch, MagicMock
from src.credential_checker import CredentialChecker, Credential
from src.logger import Logger

class TestCredentialChecker(unittest.TestCase):
    def setUp(self):
        self.logger = Logger("tests/test.log")
        self.checker = CredentialChecker(logger=self.logger)
        self.test_credential = Credential(
            url="http://test.com",
            username="user",
            password="pass"
        )

    @patch('requests.Session')
    def test_valid_credential(self, mock_session):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.return_value.post.return_value = mock_response

        result = self.checker.check_credential(self.test_credential)
        self.assertTrue(result)

    @patch('requests.Session')
    def test_invalid_credential(self, mock_session):
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_session.return_value.post.return_value = mock_response

        result = self.checker.check_credential(self.test_credential)
        self.assertFalse(result)

    @patch('requests.Session')
    def test_request_exception(self, mock_session):
        # Mock request exception
        mock_session.return_value.post.side_effect = Exception("Test error")

        result = self.checker.check_credential(self.test_credential)
        self.assertFalse(result) 