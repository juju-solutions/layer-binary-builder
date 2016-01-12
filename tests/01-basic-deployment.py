#!/usr/bin/env python3

import unittest
import amulet


class TestDeploy(unittest.TestCase):
    """
    Trivial deployment test for Gobblin builder.
    """

    def test_deploy(self):
        self.d = amulet.Deployment(series='trusty')
        self.d.add('gobblin-binary-builder', 'gbuilder')
        self.d.setup(timeout=900)
        self.d.sentry.wait(timeout=1800)
        self.unit = self.d.sentry['gbuilder'][0]


if __name__ == '__main__':
    unittest.main()
