#!/usr/bin/env python3

import unittest
from kmeldb.SubIndexEntry import SubIndexEntry
# from tests.create_media_files import single_genre


class TestSubIndex(unittest.TestCase):

    def test_frozen(self):
        subindex = SubIndexEntry()
        with self.assertRaises(TypeError):
            # Class should be frozen
            subindex.foo = 1
