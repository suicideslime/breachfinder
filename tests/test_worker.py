import unittest
from unittest.mock import patch, MagicMock
from src.worker import CredentialWorker
from src.config import Config
from src.credential_checker import Credential

class TestCredentialWorker(unittest.TestCase):
    def setUp(self):
        self.config = Config(
            input_file="test_input.txt",
            num_threads=2
        )
        self.worker = CredentialWorker(self.config)
        self.test_credentials = [
            Credential("http://test1.com", "user1", "pass1"),
            Credential("http://test2.com", "user2", "pass2"),
            Credential("http://test3.com", "user3", "pass3")
        ]

    @patch('src.credential_checker.CredentialChecker.check_credential')
    def test_process_credentials(self, mock_check):
        # Mock checker to alternate between valid and invalid credentials
        mock_check.side_effect = [True, False, True]

        valid_credentials = self.worker.process_credentials(self.test_credentials)
        
        self.assertEqual(len(valid_credentials), 2)
        self.assertEqual(valid_credentials[0].url, "http://test1.com")
        self.assertEqual(valid_credentials[1].url, "http://test3.com")

    @patch('src.credential_checker.CredentialChecker.check_credential')
    def test_process_empty_credentials(self, mock_check):
        valid_credentials = self.worker.process_credentials([])
        self.assertEqual(len(valid_credentials), 0)
        mock_check.assert_not_called() 