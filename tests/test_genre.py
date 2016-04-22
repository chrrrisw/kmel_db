#!/usr/bin/env python3

import unittest
from kmeldb.GenreIndexEntry import GenreIndexEntry, GenreException
from kmeldb.PerformerIndexEntry import PerformerIndexEntry
from kmeldb.AlbumIndexEntry import AlbumIndexEntry
from tests import create_media_files as cmf


class TestGenre(unittest.TestCase):

    def test_single_genre(self):
        cmf.random_tracks()

        # Create some albums
        albums = []
        album_index = 0
        for name in cmf.ALL_ALBUM_NAMES:
            albums.append(AlbumIndexEntry(
                name=name,
                titles=cmf.ALBUM_FILES[name],
                number=album_index))
            album_index += 1

        # Create some performers
        performers = []
        performer_index = 0
        for name in cmf.PERFORMER_NAMES:
            performers.append(PerformerIndexEntry(
                name=name,
                titles=cmf.PERFORMER_FILES[name],
                number=performer_index))
            performer_index += 1

        genres = []
        genre_index = 0
        for genre in cmf.GENRE_NAMES:
            genres.append(GenreIndexEntry(
                name=genre,
                titles=cmf.GENRE_FILES[genre],
                number=genre_index))
            genre_index += 1

        for genre in genres:
            num_titles = len(cmf.GENRE_FILES[genre._name[:-1]])
            self.assertEqual(num_titles, genre.number_of_titles)
            self.assertEqual(num_titles, len(genre.titles))

            # Test exceptions

            with self.assertRaises(GenreException):
                # Haven't initialised performers
                e = genre.performer_numbers()
            with self.assertRaises(GenreException):
                # Haven't initialised performers
                e = genre.number_of_performers()

            with self.assertRaises(GenreException):
                # Haven't initialised albums
                e = genre.album_numbers()
            with self.assertRaises(GenreException):
                # Haven't initialised albums
                e = genre.number_of_albums()

            with self.assertRaises(TypeError):
                # Class should be frozen
                genre.foo = 1

            genre.init_performers(performers)
            genre.init_albums(albums)

            # TODO: Some meaningful check
            print('Genre {} has {} performers {}'.format(
                genre._name[:-1],
                genre.number_of_performers,
                genre.performer_numbers))


            # TODO: Some meaningful check
            print('Genre {} has {} albums {}'.format(
                genre._name[:-1],
                genre.number_of_albums,
                genre.album_numbers))

    # performer_numbers
    # number_of_performers
    # init_albums
    # album_numbers
    # number_of_albums
    # performer
    # number_of_albums_for_performer
    # number_of_titles_for_performer
    # number_of_titles_for_album
    # number_of_titles_for_album_for_performer

    # def test_double_cd(self):
    #     genre_name = 'Genre 2'
    #     number_of_tracks = 10
    #     expected = list(range(2 * number_of_tracks))

    #     # Create two discs worth of tracks, with different disc numbers
    #     mf = single_genre(
    #         genre_name=genre_name,
    #         number_of_tracks=number_of_tracks)
    #     mf.extend(single_genre(
    #         genre_name=genre_name,
    #         number_of_tracks=number_of_tracks,
    #         offset=10))

    #     genre = GenreIndexEntry(
    #         name=genre_name,
    #         titles=mf,
    #         number=1)

    #     self.assertEqual(2 * number_of_tracks, len(genre.title_numbers))
    #     self.assertEqual(expected, genre.title_numbers)

    #     index = 0
    #     for track in genre.tracks:
    #         self.assertEqual(track.index, index)
    #         index += 1

    #     self.assertEqual(2, len(genre._discs_and_tracks))
    #     self.assertEqual(number_of_tracks, len(genre._discs_and_tracks[1]))
    #     self.assertEqual(number_of_tracks, len(genre._discs_and_tracks[2]))

    # def test_duplicated_tracks(self):
    #     genre_name = 'Genre 2'
    #     number_of_tracks = 10
    #     expected = list(range(3 * number_of_tracks))

    #     # Create three discs worth of tracks, with the same disc number
    #     mf = single_genre(
    #         genre_name=genre_name,
    #         number_of_tracks=number_of_tracks)
    #     mf.extend(single_genre(
    #         genre_name=genre_name,
    #         number_of_tracks=number_of_tracks,
    #         offset=10))
    #     mf.extend(single_genre(
    #         genre_name=genre_name,
    #         number_of_tracks=number_of_tracks,
    #         offset=20))

    #     genre = GenreIndexEntry(
    #         name=genre_name,
    #         titles=mf,
    #         number=1)
    #     self.assertEqual(3 * number_of_tracks, len(genre.title_numbers))
    #     self.assertEqual(expected, genre.title_numbers)

    #     index = 0
    #     for track in genre.tracks:
    #         self.assertEqual(track.index, index)
    #         index += 1

    #     self.assertEqual(3, len(genre._discs_and_tracks))
    #     self.assertEqual(number_of_tracks, len(genre._discs_and_tracks[1]))
    #     self.assertEqual(number_of_tracks, len(genre._discs_and_tracks[2]))
    #     self.assertEqual(number_of_tracks, len(genre._discs_and_tracks[3]))
