import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.test_config import TestConfig
from tests.test_credential import TestCredential
from tests.test_checker import TestCredentialChecker
from tests.test_worker import TestCredentialWorker

def run_tests():
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConfig))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCredential))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCredentialChecker))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCredentialWorker))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 