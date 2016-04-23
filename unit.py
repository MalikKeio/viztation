#!/usr/bin/env python3

import unittest

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    # verbosity=2 => verbose mode
    unittest.TextTestRunner(verbosity=2).run(testsuite)
