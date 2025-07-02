#!/usr/bin/env python3
"""
Test runner for PythonPageAutomation
Runs all unit tests in the tests directory
"""
import unittest
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_tests():
    """Discover and run all tests"""
    # Discover tests in the tests directory
    loader = unittest.TestLoader()
    start_dir = os.path.join(project_root, 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())