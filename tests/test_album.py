#!/usr/bin/env python3

import unittest
from kmeldb import AlbumIndexEntry
from tests.create_media_files import single_cd


class TestAlbum(unittest.TestCase):

    def test_single_cd(self):
        album_name = 'Album 1'
        number_of_tracks = 10
        expected = list(range(number_of_tracks))

        # Create a disc worth of tracks
        mf = single_cd(
            album_name=album_name,
            number_of_tracks=number_of_tracks,
            disc_number=1,
            reversed=True)
        sorted_mf = list(reversed(mf))

        album = AlbumIndexEntry.AlbumIndexEntry(
            name=album_name,
            titles=mf,
            number=1)

        # Test disc/track number order
        self.assertEqual(expected, album.title_numbers)
        self.assertEqual(number_of_tracks, len(album.title_numbers))
        self.assertEqual(sorted_mf, album.tracks)

        # Test unordered titles
        self.assertEqual(number_of_tracks, album.number_of_titles)
        self.assertEqual(mf, album.titles)

        with self.assertRaises(TypeError):
            # Class should be frozen
            album.foo = 1

    def test_double_cd(self):
        album_name = 'Album 2'
        number_of_tracks = 10
        expected = list(range(2 * number_of_tracks))

        # Create two discs worth of tracks, with different disc numbers
        mf = single_cd(
            album_name=album_name,
            number_of_tracks=number_of_tracks,
            disc_number=1)
        mf.extend(single_cd(
            album_name=album_name,
            number_of_tracks=number_of_tracks,
            disc_number=2,
            offset=10,
            reversed=True))

        album = AlbumIndexEntry.AlbumIndexEntry(
            name=album_name,
            titles=mf,
            number=1)

        self.assertEqual(2 * number_of_tracks, len(album.title_numbers))
        self.assertEqual(expected, album.title_numbers)

        index = 0
        for track in album.tracks:
            self.assertEqual(track.index, index)
            index += 1

        self.assertEqual(2, len(album._discs_and_tracks))
        self.assertEqual(number_of_tracks, len(album._discs_and_tracks[1]))
        self.assertEqual(number_of_tracks, len(album._discs_and_tracks[2]))

    def test_duplicated_tracks(self):
        album_name = 'Album 2'
        number_of_tracks = 10
        expected = list(range(3 * number_of_tracks))

        # Create three discs worth of tracks, with the same disc number
        mf = single_cd(
            album_name=album_name,
            number_of_tracks=number_of_tracks,
            disc_number=1)
        mf.extend(single_cd(
            album_name=album_name,
            number_of_tracks=number_of_tracks,
            disc_number=1,
            offset=10))
        mf.extend(single_cd(
            album_name=album_name,
            number_of_tracks=number_of_tracks,
            disc_number=1,
            offset=20))

        album = AlbumIndexEntry.AlbumIndexEntry(
            name=album_name,
            titles=mf,
            number=1)
        self.assertEqual(3 * number_of_tracks, len(album.title_numbers))
        self.assertEqual(expected, album.title_numbers)

        index = 0
        for track in album.tracks:
            self.assertEqual(track.index, index)
            index += 1

        self.assertEqual(3, len(album._discs_and_tracks))
        self.assertEqual(number_of_tracks, len(album._discs_and_tracks[1]))
        self.assertEqual(number_of_tracks, len(album._discs_and_tracks[2]))
        self.assertEqual(number_of_tracks, len(album._discs_and_tracks[3]))
