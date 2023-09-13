import math

"""
Example of a test file
Test files should end with "_test" and all test files can be run by running "pytest" in the tests folder
A single test file can be run by passing the file name to the pytest command
"""


def test_sqaure_root():
    # this test should pass
    assert math.sqrt(9) == 3

    # this test should fail (intentionally)
    assert math.sqrt(9) == 5
