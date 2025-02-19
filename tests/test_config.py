import unittest
import os
import json
from src.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_config_path = "tests/test_config.json"
        self.test_config = Config(
            input_file="test_input.txt",
            output_file="test_output.txt",
            num_threads=2,
            max_retries=2,
            timeout=5,
            log_file="test.log",
            log_level="DEBUG"
        )

    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    def test_save_and_load_config(self):
        # Test saving config
        self.assertTrue(self.test_config.save_to_file(self.test_config_path))
        
        # Test loading config
        loaded_config = Config.load_from_file(self.test_config_path)
        self.assertIsNotNone(loaded_config)
        self.assertEqual(loaded_config.input_file, self.test_config.input_file)
        self.assertEqual(loaded_config.num_threads, self.test_config.num_threads) 