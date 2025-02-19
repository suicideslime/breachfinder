import unittest
from src.credential_checker import Credential

class TestCredential(unittest.TestCase):
    def test_credential_from_valid_line(self):
        line = "http://example.com|user123|pass456"
        credential = Credential.from_line(line)
        
        self.assertIsNotNone(credential)
        self.assertEqual(credential.url, "http://example.com")
        self.assertEqual(credential.username, "user123")
        self.assertEqual(credential.password, "pass456")

    def test_credential_from_invalid_line(self):
        invalid_lines = [
            "invalid_line",
            "only|one|separator|extra",
            "|missing|fields",
            "||",
            ""
        ]
        
        for line in invalid_lines:
            credential = Credential.from_line(line)
            self.assertIsNone(credential)

    def test_credential_to_line(self):
        credential = Credential(
            url="http://test.com",
            username="testuser",
            password="testpass"
        )
        
        expected = "http://test.com|testuser|testpass"
        self.assertEqual(credential.to_line(), expected) 