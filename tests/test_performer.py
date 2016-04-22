#!/usr/bin/env python3

import unittest
from kmeldb.PerformerIndexEntry import PerformerIndexEntry, PerformerException
from tests.create_media_files import single_performer


class TestPerformer(unittest.TestCase):

    def test_single_cd(self):
        performer_name = 'Performer 1'
        number_of_tracks = 10

        # Create a disc worth of tracks
        mf = single_performer(
            performer_name=performer_name,
            number_of_tracks=number_of_tracks)

        performer = PerformerIndexEntry(
            name=performer_name,
            titles=mf,
            number=1)

        self.assertEqual(number_of_tracks, performer.number_of_titles)
        self.assertEqual(number_of_tracks, len(performer.titles))

        # Test exceptions

        with self.assertRaises(PerformerException):
            # Haven't initialised albums
            e = performer.album_numbers()
        with self.assertRaises(PerformerException):
            # Haven't initialised albums
            e = performer.number_of_albums()

        with self.assertRaises(TypeError):
            # Class should be frozen
            performer.foo = 1

        # Test no album
        self.assertEqual(None, performer.album(0))

        # Initialise the albums
        # performer.init_albums(albums)
