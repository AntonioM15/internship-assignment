import unittest

TESTS_PATH = './unit_tests'


if __name__ == '__main__':
    """ Run all the tests under a given directory 
        source: https://stackoverflow.com/a/40437679
    """
    loader = unittest.TestLoader()
    suite = loader.discover(TESTS_PATH)

    runner = unittest.TextTestRunner()
    runner.run(suite)
