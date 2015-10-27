#!/usr/bin/python3
# encoding: utf-8
'''
DapGen -- a Kenwood database generator.

DapGen is a media file scanner that scans a path for all media files, and
generates a database for Kenwood car stereos.

It defines the following classes:
    Playlist
    MainIndexEntry
    GenreIndexEntry
    PerformerIndexEntry
    AlbumIndexEntry
    PlaylistIndexEntry
    SubIndexEntry
    MediaFile
    KenwoodDatabase
    MediaLocation

@author:     Chris Willoughby

@copyright:  2014 Chris Willoughby. All rights reserved.

@license:    Apache License 2.0

@contact:    chrrrisw <at> gmail <dot> com
@deffield    updated: Updated
'''

import sys
import os
import logging
import struct
from hsaudiotag import auto

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from MediaFile import MediaFile
from MainIndexEntry import MainIndexEntry
from GenreIndexEntry import GenreIndexEntry
from PerformerIndexEntry import PerformerIndexEntry
from AlbumIndexEntry import AlbumIndexEntry

log = logging.getLogger(__name__)

__all__ = []
__version__ = 0.1
__date__ = '2014-05-12'
__updated__ = '2014-05-12'

DEBUG = 0
TESTRUN = 1
PROFILE = 0

STRING_ENCODING = "utf_16_le"

valid_media_files = ['mp3', 'wma']
valid_media_playlists = []

OFFSETS_OFFSET = 0x40

# The following is the list of offsets in the offset table - DO NOT CHANGE
# TO INCLUDE ANYTHING ELSE
(
    main_index_offset,
    title_offset,
    shortdir_offset,
    shortfile_offset,

    longdir_offset,
    longfile_offset,
    alpha_title_order_offset,
    genre_index_offset,

    genre_name_offset,
    genre_title_offset,
    genre_title_order_offset,
    performer_index_offset,

    performer_name_offset,
    performer_title_offset,
    performer_title_order_offset,
    album_index_offset,

    album_name_offset,
    album_title_offset,
    album_title_order_offset,
    u20_offset,

    playlist_index_offset,
    playlist_name_offset,
    playlist_title_offset,
    u24_offset,

    u25_offset,
    u26_offset,
    u27_offset,
    sub_index_offset,

    u29_offset,
    u30_offset,
    u31_offset,
    u32_offset,
    end_offsets
) = list(range(33))

(
    sub_0_genre_performers,
    sub_1_genre_performer_albums,
    sub_2_genre_performer_album_titles,
    sub_3_genre_ordered_titles,
    sub_4_genre_albums,
    sub_5_genre_album_titles,
    sub_6_genre_titles,
    sub_7_performer_albums,
    sub_8_performer_album_titles,
    sub_9_performer_titles,
    sub_10_genre_performers,
    sub_11_genre_performer_titles,
    sub_12_genre_ordered_titles,
    end_subindex_offsets
) = list(range(14))


class Playlist(object):
    """
    An object to hold a playlist. Reads a previously created playlist for
    inclusion in the database.
    """

    def __init__(self):
        """
        Not yet implemented.
        """

        log.debug("Playlist created")


class PlaylistIndexEntry(object):
    def __init__(self, name, titles, number):
        self.number = number
        self.name = name + '\x00'
        self.name_length = len(self.name.encode(STRING_ENCODING))
        self.name_char_length = 2

        # TODO: Set later
        self.name_offset = 0

        self.num_titles = len(titles)
        self.titles = titles

        # TODO: Set later
        self.title_entry_offset = 0

        print("\nPlaylistIndexEntry\n\tName:{}: Length:{}: Num_Titles:{}:\n".format(self.name, self.name_length, self.num_titles))

    def set_name_offset(self, name_offset):
        self.name_offset = name_offset

    def set_title_entry_offset(self, title_entry_offset):
        self.title_entry_offset = title_entry_offset

    def get_representation(self):
        return struct.pack("<HHIHHHH",
                           self.name_length, self.name_char_length, self.name_offset,
                           0x0000,
                           self.num_titles, self.title_entry_offset,
                           0x0000)


class SubIndexEntry(object):
    def __init__(self):
        self._offset = 0
        self._size = 0
        self._count = 0

    def set_offset(self, offset):
        self._offset = offset

    def set_size(self, size):
        self._size = size

    def set_count(self, count):
        self._count = count

    def get_representation(self):
        return struct.pack("<IHH", self._offset, self._size, self._count)


class KenwoodDatabase(object):
    """
    The class responsible for writing the Kendwood database file.
    """

    def __init__(self, path):
        """
        Stores the path to the database and opens the file for writing.
        """

        log.debug("KenwoodDatabase created at: {}.".format(path))

        self.db_path = path
        # Open a file for writing
        self.db_file = open(os.path.join(self.db_path, "kenwood.dap"), mode='wb')

        # Create the empty list of offsets
        self.offsets = []
        for offset in range(end_offsets):
            self.offsets.append(0)

        self.subIndex = []
        for sub in range(end_subindex_offsets):
            self.subIndex.append(SubIndexEntry())

    def write_signature(self):
        """
        Writes the first eight bytes of the database file (signature block).
        """
        self.db_file.write(b"\x4b\x57\x44\x42\x00\x01\x03\x01")

    def write_counts(self):
        """
        Count of main index
        Size of main index entry (always 0x0040)

        Count of TCON index
        Size of TCON index entry (always 0x0010)

        Count of TPE1 index
        Size of TPE1 index entry (always 0x0010)

        Count of TALB index
        Size of TALB index entry (always 0x0010)

        Count of Playlist index
        Size of Playlist index entry (always 0x0010)

        Count of unknown 9 (always 0x0001)
        Size of unknown 9 (always 0x0014)
        """

        self.db_file.write(struct.pack("<HH", self.number_of_entries, 0x0040))
        self.db_file.write(struct.pack("<HH", self.number_of_genres, 0x0010))
        self.db_file.write(struct.pack("<HH", self.number_of_performers, 0x0010))
        self.db_file.write(struct.pack("<HH", self.number_of_albums, 0x0010))
        self.db_file.write(struct.pack("<HH", self.number_of_playlists, 0x0010))
        self.db_file.write(struct.pack("<HH", 0x0001, 0x0014))

        self.db_file.write(b"\x01\x00\x02\x00\x00\x00\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00")
        self.db_file.write(b"\x00\x00\x06\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    def write_offsets(self):
        """
        The int at offset 0x40 is the offset to the main index.
        The int at offset 0x44 is the offset to the title table.
        The int at offset 0x48 is the offset to the short directory table.
        The int at offset 0x4c is the offset to the short file table.

        The int at offset 0x50 is the offset to the long directory table.
        The int at offset 0x54 is the offset to the long file table.
        The int at offset 0x58 is the offset to a list of alphabetically ordered titles.
        The int at offset 0x5c is the offset to the Genre (TCON) index.

        The int at offset 0x60 is the offset to the Genre (TCON) name table.
        The int at offset 0x64 is the offset to the Genre (TCON) title table.
        The int at offset 0x68 is the offset to a list of Genre ordered titles.
        The int at offset 0x6c is the offset to the Performer (TPE1) index.

        The int at offset 0x70 is the offset to the Performer (TPE1) name table.
        The int at offset 0x74 is the offset to the Performer (TPE1) title table.
        The int at offset 0x78 is the offset to a list of Performer ordered titles.
        The int at offset 0x7c is the offset to the Album (TALB) index.

        The int at offset 0x80 is the offset to the Album (TALB) name table.
        The int at offset 0x84 is the offset to the Album (TALB) title table.
        The int at offset 0x88 is the offset to a list of Album ordered titles.
        The int at offset 0x8c is the offset to unknown table 8.

        The int at offset 0x90 is the offset to the playlist index.
        The int at offset 0x94 is the offset to the playlist name table.
        The int at offset 0x98 is the offset to the playlist title table.
        The int at offset 0x9c is the offset to unknown table 9.

        The int at offset 0xa0 is the offset to unknown table 10.
        The int at offset 0xa4 is the offset to unknown table 11.
        The int at offset 0xa8 is the offset to unknown table 12.
        The int at offset 0xac is the offset to the sub-indices.

        The int at offset 0xb0 is always 0
        The int at offset 0xb4 is always 0
        The int at offset 0xb8 is always 0
        The int at offset 0xbc is always 0
        """

        for offset in self.offsets:
            self.db_file.write(struct.pack("<I", offset))

    def write_main_index(self):
        """
        For each of the entries in the main index, write it's representation
        to file.
        """

        for miEntry in self.mainIndex:
            self.db_file.write(miEntry.get_representation())

    def write_title_table(self):
        """
        For each of the entries in the main index, store the offset of its
        title and write the title to file.
        """

        start_of_titles = self.db_file.tell()
        for miEntry in self.mainIndex:
            miEntry.set_title_offset(self.db_file.tell() - start_of_titles)
            self.db_file.write(miEntry.get_title().encode(STRING_ENCODING))

    def write_shortdir_table(self):
        """
        For each of the entries in the main index, if the short directory
        name is not already written then store the offset of its entry
        and write its name to file.
        If it is already written, just store the offset.
        """

        start_of_shortdirs = self.db_file.tell()
        self.shortdirs = {}
        for miEntry in self.mainIndex:
            if miEntry.get_shortdir() not in self.shortdirs:
                self.shortdirs[miEntry.get_shortdir()] = self.db_file.tell() - start_of_shortdirs
                self.db_file.write(miEntry.get_shortdir().encode("ascii"))
            miEntry.set_shortdir_offset(self.shortdirs[miEntry.get_shortdir()])

    def write_shortfile_table(self):
        """
        For each of the entries in the main index, write its short filename to file and store
        its offset in the main index entry.
        """

        start_of_shortfiles = self.db_file.tell()
        for miEntry in self.mainIndex:
            miEntry.set_shortfile_offset(self.db_file.tell() - start_of_shortfiles)
            self.db_file.write(miEntry.get_shortfile().encode("ascii"))

    def write_longdir_table(self):
        """
        For each of the entries in the main index, if the long directory name is
        not already written then store the offset of its entry and write its name to file.
        If it is already written, just store the offset.
        """

        start_of_longdirs = self.db_file.tell()
        self.longdirs = {}
        for miEntry in self.mainIndex:
            if miEntry.get_longdir() not in self.longdirs:
                self.longdirs[miEntry.get_longdir()] = self.db_file.tell() - start_of_longdirs
                self.db_file.write(miEntry.get_longdir().encode(STRING_ENCODING))
            miEntry.set_longdir_offset(self.longdirs[miEntry.get_longdir()])

    def write_longfile_table(self):
        """
        For each of the entries in the main index, write its long filename to file and store
        its offset in the main index entry.
        """

        start_of_longfiles = self.db_file.tell()
        for miEntry in self.mainIndex:
            miEntry.set_longfile_offset(self.db_file.tell() - start_of_longfiles)
            self.db_file.write(miEntry.get_longfile().encode(STRING_ENCODING))

    def write_alpha_ordered_title_table(self):
        """
        """

        print("\nAlpha Ordered Title Table")
        for title in self.alpha_ordered_titles:
            print(title, self.mainIndex[title].get_title())
            self.db_file.write(struct.pack("<H", title))

    # GENRE

    def write_all_genre_tables(self):
        """
        """

        self.offsets[genre_index_offset] = self.db_file.tell()
        self.write_genre_index()

        self.offsets[genre_name_offset] = self.db_file.tell()
        self.write_genre_name_table()

        self.offsets[genre_title_offset] = self.db_file.tell()
        self.write_genre_title_table()

        self.offsets[genre_title_order_offset] = self.db_file.tell()
        self.write_genre_title_order_table()

    def write_genre_index(self):
        """
        For each entry in the Genre Index, write its representation to file.
        """
        for giEntry in self.genreIndex:
            # Write to file
            self.db_file.write(giEntry.get_representation())

    def write_genre_name_table(self):
        """
        For each entry in the Genre Index, write its name to file and store the
        offset to the name.
        """
        start_of_names = self.db_file.tell()
        for giEntry in self.genreIndex:
            giEntry.set_name_offset(self.db_file.tell() - start_of_names)
            self.db_file.write(giEntry.name.encode(STRING_ENCODING))

    def write_genre_title_table(self):
        """
        For each entry in the Genre Index, write the indices of all media files in the Genre
        and store the offset to the start of the indices.

        Sort by genre, then album, then title
        """
        start_of_titles = self.db_file.tell()
        self.genre_title_table_length = 0
        for giEntry in self.genreIndex:
            giEntry.set_title_entry_offset(self.db_file.tell() - start_of_titles)

            for album in sorted(giEntry.get_albums()):
                for title in sorted(self.albumIndex[album].get_title_numbers()):
                    if self.mainIndex[title].get_genre_number() == giEntry.number and \
                            self.mainIndex[title].get_album_number() == album:
                        self.db_file.write(struct.pack("<H", self.mainIndex[title].get_index()))
                        self.genre_title_table_length += 1

            # for mf in giEntry.titles:
            #     self.db_file.write(struct.pack("<H", mf.get_index()))
            #     self.genre_title_table_length += 1

        # TODO:
        if self.genre_title_table_length != len(self.mainIndex):
            print("1#############################################")

    def write_genre_title_order_table(self):
        """
        Sort by genre, then performer, then album, then title
        """
        self.genre_title_order_table_length = 0
        for giEntry in self.genreIndex:
            for performer in sorted(giEntry.get_performers()):
                for album in sorted(self.performerIndex[performer].get_albums()):
                    for title in sorted(self.albumIndex[album].get_title_numbers()):
                        if self.mainIndex[title].get_genre_number() == giEntry.number and \
                                self.mainIndex[title].get_performer_number() == performer and \
                                self.mainIndex[title].get_album_number() == album:
                            self.db_file.write(struct.pack("<H", self.mainIndex[title].get_index()))
                            self.genre_title_order_table_length += 1

        # TODO:
        if self.genre_title_order_table_length != len(self.mainIndex):
            print("2#############################################")

    # PERFORMER

    def write_all_performer_tables(self):
        self.offsets[performer_index_offset] = self.db_file.tell()
        self.write_performer_index()

        self.offsets[performer_name_offset] = self.db_file.tell()
        self.write_performer_name_table()

        self.offsets[performer_title_offset] = self.db_file.tell()
        self.write_performer_title_table()

        self.offsets[performer_title_order_offset] = self.db_file.tell()
        self.write_performer_title_order_table()

    def write_performer_index(self):
        for piEntry in self.performerIndex:
            # Write to file
            self.db_file.write(piEntry.get_representation())

    def write_performer_name_table(self):
        start_of_names = self.db_file.tell()
        for piEntry in self.performerIndex:
            piEntry.set_name_offset(self.db_file.tell() - start_of_names)
            self.db_file.write(piEntry.name.encode(STRING_ENCODING))

    def write_performer_title_table(self):
        start_of_titles = self.db_file.tell()
        self.performer_title_table_length = 0
        for piEntry in self.performerIndex:
            piEntry.set_title_entry_offset(self.db_file.tell() - start_of_titles)

            for album in sorted(piEntry.get_albums()):
                for title in sorted(self.albumIndex[album].get_title_numbers()):
                    if self.mainIndex[title].get_performer_number() == piEntry.number and \
                            self.mainIndex[title].get_album_number() == album:
                        self.db_file.write(struct.pack("<H", self.mainIndex[title].get_index()))
                        self.performer_title_table_length += 1

            #for mf in piEntry.titles:
            #    self.db_file.write(struct.pack("<H", mf.get_index()))
            #    self.performer_title_table_length += 1

    def write_performer_title_order_table(self):
        '''
        Sort by performer, then album, then title
        '''
        for piEntry in self.performerIndex:
            for album in sorted(piEntry.get_albums()):
                for title in sorted(self.albumIndex[album].get_title_numbers()):
                    if self.mainIndex[title].get_performer_number() == piEntry.number and \
                            self.mainIndex[title].get_album_number() == album:
                        self.db_file.write(struct.pack("<H", self.mainIndex[title].get_index()))
            #for mf in piEntry.titles:
            #    self.db_file.write(struct.pack("<H", mf.get_index()))

    # ALBUM

    def write_all_album_tables(self):
        self.offsets[album_index_offset] = self.db_file.tell()
        self.write_album_index()

        self.offsets[album_name_offset] = self.db_file.tell()
        self.write_album_name_table()

        self.offsets[album_title_offset] = self.db_file.tell()
        self.write_album_title_table()

        self.offsets[album_title_order_offset] = self.db_file.tell()
        self.write_album_title_order_table()

    def write_album_index(self):
        for aiEntry in self.albumIndex:
            self.db_file.write(aiEntry.get_representation())

    def write_album_name_table(self):
        start_of_names = self.db_file.tell()
        for aiEntry in self.albumIndex:
            aiEntry.set_name_offset(self.db_file.tell() - start_of_names)
            self.db_file.write(aiEntry.name.encode(STRING_ENCODING))

    def write_album_title_table(self):
        start_of_titles = self.db_file.tell()
        for aiEntry in self.albumIndex:
            aiEntry.set_title_entry_offset(self.db_file.tell() - start_of_titles)
            for mf in aiEntry.titles:
                self.db_file.write(struct.pack("<H", mf.get_index()))

    def write_album_title_order_table(self):
        for aiEntry in self.albumIndex:
            for mf in aiEntry.titles:
                self.db_file.write(struct.pack("<H", mf.get_index()))

    # Was table 8
    def write_u20(self):
        """
        Table 20 has no contents - pass.
        """
        pass

    # PLAYLIST

    def write_all_playlist_tables(self):
        """
        Write all playlist tables to file.
        """
        self.offsets[playlist_index_offset] = self.db_file.tell()
        self.write_playlist_index()

        self.offsets[playlist_name_offset] = self.db_file.tell()
        self.write_playlist_name_table()

        self.offsets[playlist_title_offset] = self.db_file.tell()
        self.write_playlist_title_table()

    def write_playlist_index(self):
        for piEntry in self.playlistIndex:
            self.db_file.write(piEntry.get_representation())

    def write_playlist_name_table(self):
        """
        TODO: Not yet implemented
        """
        log.warning("write_playlist_name_table NYI")
        pass

    def write_playlist_title_table(self):
        """
        TODO: Not yet implemented
        """
        log.warning("write_playlist_title_table NYI")
        pass

    # Was table 9
    def write_u24(self):
        self.db_file.write(b"\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    # Was table 10
    def write_u25(self):
        self.db_file.write(b"\x00\x00")

    # Was table 11
    def write_u26(self):
        for aiEntry in range(len(self.albumIndex)):
            self.db_file.write(b"\x00\x00\x00\x00")

    # Was table 12
    def write_u27(self):
        for miEntry in range(len(self.mainIndex)):
            self.db_file.write(b"\x00\x00\x00\x00")

    # SUB-INDICES
    def write_all_sub_indices(self):
        """
        Sub-indices starts with a relative offset (int) to the start of more tables.
        """

        # Write a filler
        temp_offset_1 = self.db_file.tell()
        self.db_file.write(struct.pack("<I", 0x00000000))

        # Write the sub index
        self.write_sub_index()

        self.subIndex[sub_0_genre_performers].offset = self.db_file.tell()
        self.write_sub_0()

        self.subIndex[sub_1_genre_performer_albums].offset = self.db_file.tell()
        self.write_sub_1()

        self.subIndex[sub_2_genre_performer_album_titles].offset = self.db_file.tell()
        self.write_sub_2()

        self.subIndex[sub_3_genre_ordered_titles].offset = self.db_file.tell()
        self.write_sub_3()

        self.subIndex[sub_4_genre_albums].offset = self.db_file.tell()
        self.write_sub_4()

        self.subIndex[sub_5_genre_album_titles].offset = self.db_file.tell()
        self.write_sub_5()

        self.subIndex[sub_6_genre_titles].offset = self.db_file.tell()
        self.write_sub_6()

        self.subIndex[sub_7_performer_albums].offset = self.db_file.tell()
        self.write_sub_7()

        self.subIndex[sub_8_performer_album_titles].offset = self.db_file.tell()
        self.write_sub_8()

        self.subIndex[sub_9_performer_titles].offset = self.db_file.tell()
        self.write_sub_9()

        self.subIndex[sub_10_genre_performers].offset = self.db_file.tell()
        self.write_sub_10()

        self.subIndex[sub_11_genre_performer_titles].offset = self.db_file.tell()
        self.write_sub_11()

        self.subIndex[sub_12_genre_ordered_titles].offset = self.db_file.tell()
        self.write_sub_12()

        # Go back and update offsets
        temp_offset_2 = self.db_file.tell()
        self.db_file.seek(temp_offset_1)
        self.db_file.write(struct.pack("<I", self.subIndex[sub_0_genre_performers].offset - temp_offset_1))
        self.write_sub_index()
        self.db_file.seek(temp_offset_2)

    def write_sub_index(self):
        """
        This is then followed by a number (always 13) of entries that seem to consist of
        an absolute offset (int), a size (short int) and a count (short int).

        The absolute offset points to another table that either contains "count"
        short ints (if "size" is 2), or "count" arrays of 4 short ints (if "size" is 8).

        """
        for sie in self.subIndex:
            self.db_file.write(sie.get_representation())

    def write_sub_0(self):
        """
        Sub-indices _Genre_ _Performers_ offsets and counts (0)

        This table contains the number of _Performers_ per _Genre_.

        The number of entries is the number of _Genres_ minus 1 (_Genre_ 0 is excluded). The format of each entry is four short ints.

        The first short int is the _Genre_ number (ascending order).
        The second short int is an offset into the next table (_Genre_ _Performer_ _Albums_).
        The third short int is the number of _Performers_ in this _Genre_.
        The last short int is always 0.
        """

        self.subIndex[sub_0_genre_performers].set_offset(self.db_file.tell())
        self.subIndex[sub_0_genre_performers].set_size(8)
        self.subIndex[sub_0_genre_performers].set_count(len(self.genreIndex) - 1)

        entry_offset = 0
        for giEntry in self.genreIndex[1:]:
            self.db_file.write(struct.pack("<HHHH", giEntry.number, entry_offset, giEntry.get_number_of_performers(), 0x0000))
            entry_offset += giEntry.get_number_of_performers()

    def write_sub_1(self):
        """
        Sub-indices _Genre_ _Performer_ _Albums_ offsets and counts (1)

        This table contains the number of _Albums_ per _Performer_ per _Genre_.

        The first short int is the _Performer_ number. Ascending order within _Genre_.
        The second short int is an offset into the next table (_Genre_ _Performer_ _Album_ _Titles_).
        The third short int is the number of _Albums_ for that _Performer_ that contain the _Genre_.
        The last short int is always 0.
        """
        self.subIndex[sub_1_genre_performer_albums].set_offset(self.db_file.tell())
        self.subIndex[sub_1_genre_performer_albums].set_size(8)

        entry_offset = 0
        count = 0
        for giEntry in self.genreIndex[1:]:
            for performer in sorted(giEntry.get_performers()):
                print("Sub1 Performer: {}".format(performer))
                self.db_file.write(struct.pack("<HHHH", performer, entry_offset, self.performerIndex[performer].get_number_of_albums(), 0x0000))
                entry_offset += self.performerIndex[performer].get_number_of_albums()
                count += 1

        self.subIndex[sub_1_genre_performer_albums].set_count(count)

    def write_sub_2(self):
        """
        Sub-indices _Genre_ _Performer_ _Album_ _Titles_ offsets and counts (2)

        This table seems to contain the number of _Titles_ per _Album_ per _Performer_ per _Genre_.

        The first short int is the _Album_ number.<br>
        The second short int is an offset into the next table (Genre-Ordered-Titles).<br>
        The third short int is the number of _Titles_.<br>
        The last short int is always zero.
        """
        self.subIndex[sub_2_genre_performer_album_titles].set_offset(self.db_file.tell())
        self.subIndex[sub_2_genre_performer_album_titles].set_size(8)

        # The first entry starts at genre 1 (genre 0 is for those files without a genre)
        entry_offset = len(self.genreIndex[0].titles)
        count = 0
        for giEntry in self.genreIndex[1:]:
            for performer in sorted(giEntry.get_performers()):
                for album in sorted(self.performerIndex[performer].get_albums()):
                    print("Sub2 Album: {}".format(album))
                    self.db_file.write(struct.pack("<HHHH", album, entry_offset, self.albumIndex[album].get_number_of_titles(), 0x0000))
                    entry_offset += self.albumIndex[album].get_number_of_titles()
                    count += 1

        self.subIndex[sub_2_genre_performer_album_titles].set_count(count)

    def write_sub_3(self):
        """
        Sub-indices Genre-Ordered-Title List (3)

        Points to table Genre-Ordered-Title List
        """
        self.subIndex[sub_3_genre_ordered_titles].set_offset(self.offsets[genre_title_order_offset])
        self.subIndex[sub_3_genre_ordered_titles].set_size(2)
        self.subIndex[sub_3_genre_ordered_titles].set_count(self.genre_title_order_table_length) # TODO: Could be len(mainIndex)

    def write_sub_4(self):
        """
        Sub-indices _Genre_ _Albums_ offsets and counts (4)

        This table seems to contain the number of _Albums_ per _Genre_.

        The number of entries is the number of _Genres_ minus 1 (_Genre_ 0 is excluded). The format of each entry is four short ints.

        The first short int is the _Genre_ number (ascending order).<br>
        The second short int is an offset into the next table (_Genre_ _Album_ _Titles_).<br>
        The third short int is the number of _Albums_ in this _Genre_.<br>
        The last short int is always 0.
        """
        self.subIndex[sub_4_genre_albums].set_offset(self.db_file.tell())
        self.subIndex[sub_4_genre_albums].set_size(8)
        self.subIndex[sub_4_genre_albums].set_count(len(self.genreIndex) - 1)

        entry_offset = 0
        for giEntry in self.genreIndex[1:]:
            self.db_file.write(struct.pack("<HHHH", giEntry.number, entry_offset, giEntry.get_number_of_albums(), 0x0000))
            entry_offset += giEntry.get_number_of_albums()


    def write_sub_5(self):
        """
        Sub-indices _Genre_ _Album_ _Titles_ offsets and counts (5)

        This table seems to contain the number of _Titles_ per _Album_ per _Genre_.

        The first short int is the _Album_ number.<br>
        The second short int is an offset into the next table (_Genre_ _Titles_).<br>
        The third short int is the number of _Titles_ for that _Album_ that contain the _Genre_.<br>
        The last short int is always 0.
        """
        self.subIndex[sub_5_genre_album_titles].set_offset(self.db_file.tell())
        self.subIndex[sub_5_genre_album_titles].set_size(8)

        entry_offset = len(self.genreIndex[0].titles)
        count = 0
        for giEntry in self.genreIndex[1:]:
            for album in sorted(giEntry.get_albums()):
                print("Sub5 Album: {}".format(album))
                self.db_file.write(struct.pack("<HHHH", album, entry_offset, self.albumIndex[album].get_number_of_titles(), 0x0000))
                entry_offset += self.albumIndex[album].get_number_of_titles()
                count += 1

        self.subIndex[sub_5_genre_album_titles].set_count(count)

    def write_sub_6(self):
        """
        Sub-indices _Genre_ _Titles_ (6)

        Points to the _Genre_ _Title_ table.
        """
        self.subIndex[sub_6_genre_titles].set_offset(self.offsets[genre_title_offset])
        self.subIndex[sub_6_genre_titles].set_size(2)
        self.subIndex[sub_6_genre_titles].set_count(self.genre_title_table_length) # TODO: Could be len(mainIndex)


    def write_sub_7(self):
        '''
        Sub-indices _Performer_ _Albums_ offsets and counts (7)

        This table seems to contain the number of _Albums_ per _Performer_.

        The number of entries is the number of _Performers_ minus 1 (_Performer_ 0 is excluded). The format of each entry is four short ints.

        The first short int is the _Performer_ number (ascending order).<br>
        The second short int is an offset into the next table (_Performer_ _Album_ _Titles_).<br>
        The third short int is the number of _Albums_ for this _Performer_.<br>
        The last short int is always 0.
        '''
        self.subIndex[sub_7_performer_albums].set_offset(self.db_file.tell())
        self.subIndex[sub_7_performer_albums].set_size(8)
        self.subIndex[sub_7_performer_albums].set_count(len(self.performerIndex) - 1)

        entry_offset = 0
        for piEntry in self.performerIndex[1:]:
            self.db_file.write(struct.pack("<HHHH", piEntry.number, entry_offset, piEntry.get_number_of_albums(), 0x0000))
            entry_offset += piEntry.get_number_of_albums()

    def write_sub_8(self):
        '''
        Sub-indices _Performer_ _Album_ _Titles_ offsets and counts (8)

        This table seems to contain the number of _Titles_ per _Album_ per _Performer_.

        The first short int is the _Album_ number.<br>
        The second short int is an offset into the next table (_Performer_ _Titles_).<br>
        The third short int is the number of _Titles_ for the _Album_ for the _Performer_.<br>
        The last short int is always 0.
        '''
        self.subIndex[sub_8_performer_album_titles].set_offset(self.db_file.tell())
        self.subIndex[sub_8_performer_album_titles].set_size(8)

        entry_offset = len(self.performerIndex[0].titles)
        count = 0
        for piEntry in self.performerIndex[1:]:
            for album in sorted(piEntry.get_albums()):
                print("Sub8 Album: {}".format(album))
                self.db_file.write(struct.pack("<HHHH", album, entry_offset, self.albumIndex[album].get_number_of_titles(), 0x0000))
                entry_offset += self.albumIndex[album].get_number_of_titles()
                count += 1

        self.subIndex[sub_8_performer_album_titles].set_count(count)

    def write_sub_9(self):
        '''
        Sub-indices _Performer_ _Titles_ (9)

        Points to the _Performer_ _Title_ table.
        '''
        self.subIndex[sub_9_performer_titles].set_offset(self.offsets[performer_title_offset])
        self.subIndex[sub_9_performer_titles].set_size(2)
        self.subIndex[sub_9_performer_titles].set_count(self.performer_title_table_length)

    def write_sub_10(self):
        '''
        Sub-indices _Genre_ _Performers_ offsets and counts (10)

        This table seems to contain the number of _Performers_ per _Genre_. As such, it is the same as Sub-indices Table 0.

        The first short int is the _Genre_ number.<br>
        The second short int is an offset into the next table (_Genre_ _Performer_ _Titles_).<br>
        The third short int is the number of _Performers_ for this _Genre_.<br>
        The last short int is always 0.
        '''
        self.subIndex[sub_10_genre_performers].set_offset(self.db_file.tell())
        self.subIndex[sub_10_genre_performers].set_size(8)
        self.subIndex[sub_10_genre_performers].set_count(len(self.genreIndex) - 1)

        entry_offset = 0
        for giEntry in self.genreIndex[1:]:
            self.db_file.write(struct.pack("<HHHH", giEntry.number, entry_offset, giEntry.get_number_of_performers(), 0x0000))
            entry_offset += giEntry.get_number_of_performers()

    def write_sub_11(self):
        '''
        Sub-indices _Genre_ _Performer_ _Titles_ offsets and counts (11)

        The first short int is the _Performer_ number.<br>
        The second short int is an offset into the next table (Genre-Ordered-Titles).<br>
        The third short int is the number of _Titles_ for the _Performer_ for the _Genre_.<br>
        The last short int is always 0.
        '''
        self.subIndex[sub_11_genre_performer_titles].set_offset(self.db_file.tell())
        self.subIndex[sub_11_genre_performer_titles].set_size(8)

        entry_offset = 0
        count = 0
        for giEntry in self.genreIndex[1:]:
            for performer in sorted(giEntry.get_performers()):
                print("Sub11 Performer: {}".format(performer))
                self.db_file.write(
                    struct.pack(
                        "<HHHH",
                        performer,
                        entry_offset,
                        self.performerIndex[performer].get_number_of_titles(),
                        0x0000))
                entry_offset += self.performerIndex[performer].get_number_of_titles()
                count += 1

        self.subIndex[sub_11_genre_performer_titles].set_count(count)

        pass

    def write_sub_12(self):
        '''
        Sub-indices Genre-Ordered-Titles (12)

        Points to table Genre-Ordered-Title List
        '''
        self.subIndex[sub_12_genre_ordered_titles].set_offset(
            self.offsets[genre_title_order_offset])
        self.subIndex[sub_12_genre_ordered_titles].set_size(2)

        # TODO: Could be len(mainIndex)
        self.subIndex[sub_12_genre_ordered_titles].set_count(
            self.genre_title_order_table_length)

    def write_u29(self):
        """
        Table 29 has no contents - pass.
        """
        pass

    def write_u30(self):
        """
        Table 30 has no contents - pass.
        """
        pass

    def write_u31(self):
        """
        Table 31 has no contents - pass.
        """
        pass

    def write_u32(self):
        """
        Table 32 has no contents - pass.
        """
        pass

    def write_db(self, media_files):
        self.write_signature()

        self.number_of_entries = len(media_files)

        # Genres, Performers and Albums always have null string entries
        titles = []
        genres = {"": []}
        performers = {"": []}
        albums = {"": []}
        playlists = {}

        self.mainIndex = []
        for mf in media_files:

            titles.append((mf.get_title(), mf.get_index()))

            # log.debug("Genre:{}:".format(mf.genre))
            if mf.get_genre() in genres:
                genres[mf.get_genre()].append(mf)
            else:
                genres[mf.get_genre()] = [mf]

            if mf.get_performer() in performers:
                performers[mf.get_performer()].append(mf)
            else:
                performers[mf.get_performer()] = [mf]

            if mf.get_album() in albums:
                albums[mf.get_album()].append(mf)
            else:
                albums[mf.get_album()] = [mf]

            miEntry = MainIndexEntry(mf)
            self.mainIndex.append(miEntry)

        self.alpha_ordered_titles = [x[1] for x in sorted(
            titles, key=lambda e: e[0])]

        self.genreIndex = []
        self.number_of_genres = len(genres)
        genre_number = 0
        for key in sorted(genres):
            print ("Genre[{}] = {}".format(key, genres[key]))
            giEntry = GenreIndexEntry(key, genres[key], genre_number)
            self.genreIndex.append(giEntry)
            genre_number += 1

        self.performerIndex = []
        self.number_of_performers = len(performers)
        performer_number = 0
        for key in sorted(performers):
            print ("Performer[{}] = {}".format(key, performers[key]))
            piEntry = PerformerIndexEntry(
                key,
                performers[key],
                performer_number)
            self.performerIndex.append(piEntry)
            performer_number += 1

        self.albumIndex = []
        self.number_of_albums = len(albums)
        album_number = 0
        for key in sorted(albums):
            print ("Album[{}] = {}".format(key, albums[key]))
            aiEntry = AlbumIndexEntry(key, albums[key], album_number)
            self.albumIndex.append(aiEntry)
            album_number += 1

        self.playlistIndex = []
        self.number_of_playlists = len(playlists)
        # TODO: Playlists

        # Write the counts
        self.write_counts()

        if self.db_file.tell() != OFFSETS_OFFSET:
            log.warning("Not at correct offset for offsets table")
            self.db_file.seek(OFFSETS_OFFSET)

        # These will be empty at the moment
        self.write_offsets()

        # Get the file offset, and store it as the main index offset
        self.offsets[main_index_offset] = self.db_file.tell()
        self.write_main_index()

        self.offsets[title_offset] = self.db_file.tell()
        self.write_title_table()

        self.offsets[shortdir_offset] = self.db_file.tell()
        self.write_shortdir_table()

        self.offsets[shortfile_offset] = self.db_file.tell()
        self.write_shortfile_table()

        self.offsets[longdir_offset] = self.db_file.tell()
        self.write_longdir_table()

        self.offsets[longfile_offset] = self.db_file.tell()
        self.write_longfile_table()

        self.offsets[alpha_title_order_offset] = self.db_file.tell()
        self.write_alpha_ordered_title_table()

        for giEntry in self.genreIndex:
            giEntry.init_performers()
            giEntry.init_albums()
        for piEntry in self.performerIndex:
            piEntry.init_albums()

        # GENRE TABLES
        self.write_all_genre_tables()

        # PERFORMER TABLES
        self.write_all_performer_tables()

        # ALBUM TABLES
        self.write_all_album_tables()

        # Was table 8
        self.offsets[u20_offset] = 0
        self.write_u20()

        # PLAYLISTS
        self.write_all_playlist_tables()

        # Was table 9
        self.offsets[u24_offset] = self.db_file.tell()
        self.write_u24()

        # Was table 10
        self.offsets[u25_offset] = self.db_file.tell()
        self.write_u25()

        # Was table 11
        self.offsets[u26_offset] = self.db_file.tell()
        self.write_u26()

        # Was table 12
        self.offsets[u27_offset] = self.db_file.tell()
        self.write_u27()

        # UP TO HERE

        self.offsets[sub_index_offset] = self.db_file.tell()
        self.write_all_sub_indices()
        # self.write_sub_index()

        self.offsets[u29_offset] = 0
        self.write_u29()

        self.offsets[u30_offset] = 0
        self.write_u30()

        self.offsets[u31_offset] = 0
        self.write_u31()

        self.offsets[u32_offset] = 0
        self.write_u32()

        # Go back and write the offsets (now complete)
        self.db_file.seek(OFFSETS_OFFSET)
        self.write_offsets()

        # Go back and write the main index (now complete)
        self.db_file.seek(self.offsets[main_index_offset])
        self.write_main_index()

        # Go back and write the genre index (now complete)
        self.db_file.seek(self.offsets[genre_index_offset])
        self.write_genre_index()

        # Go back and write the genre index (now complete)
        self.db_file.seek(self.offsets[performer_index_offset])
        self.write_performer_index()

        # Go back and write the genre index (now complete)
        self.db_file.seek(self.offsets[album_index_offset])
        self.write_album_index()

    def finalise(self):
        """
        Close the database file.
        """
        log.debug("KenwoodDatabase finalised.")
        self.db_file.close()

# Holds the list of all media locations
MediaLocations = []


class MediaLocation(object):
    """
    An object to hold the media files within a given directory path.
    It instantiates a KenwoodDatabase and one MediaFile per file.
    """

    def __init__(self, path):
        """
        Store the path, create empty lists in which to store media files
        and playlists.
        """
        self.path = path

        log.debug("MediaLocation created at: {}".format(self.path))

        # Create the database file location
        self.db_path = os.path.join(self.path, "kenwood.dap")
        if os.path.exists(self.db_path):
            log.info("database directory exists")
        else:
            log.info("data directory does not exist - creating")
            os.mkdir(self.db_path)

        self.database = KenwoodDatabase(self.db_path)

        # The list of playlists
        self.playlists = []

        # The list of media files
        self.mediaFiles = []
        index = -1
        for root, dirs, files in os.walk(self.path):
            log.debug("Root: {}".format(root))
            for media_file in files:
                if media_file[-3:] in valid_media_files:
                    index += 1
                    log.debug("{}".format(os.path.join(root, media_file)))

                    title = ""
                    performer = ""
                    album = ""
                    genre = ""

                    # TODO: Determine what to do when there is
                    # no ID3 information
                    #
                    # Title <- filename without extension
                    # Album <- directory?
                    # Performer <- directory?
                    # Genre <- 0
                    metadata = auto.File(os.path.join(root, media_file))
                    title = metadata.title
                    if title == "":
                        title = media_file.split(".")[0]
                    performer = metadata.artist
                    if performer == "":
                        pass
                    album = metadata.album
                    if album == "":
                        pass
                    genre = metadata.genre
                    if genre == "":
                        pass

                    # try:
                    #    metadata = id3.ID3(os.path.join(root,media_file))
                    # except id3.ID3NoHeaderError:
                    #    log.warning("No ID3 Header: {}".format(media_file))
                    #    metadata = {}
                    #
                    # if 'TIT2' in metadata:
                    #    title = str(metadata['TIT2'])
                    #
                    # if 'TPE1' in metadata:
                    #    performer = str(metadata['TPE1'])
                    #
                    # if 'TALB' in metadata:
                    #    album = str(metadata['TALB'])
                    #
                    # if 'TCON' in metadata:
                    #    genre = str(metadata['TCON'])

                    longdir = "/" + os.path.relpath(root, self.path) + "/"
                    longfile = media_file

                    if mdir_parser is not None:
                        shortdir = mdir_parser.short_directory_name(longdir)
                        shortfile = mdir_parser.short_file_name(
                            longdir,
                            longfile)
                    else:
                        shortdir = ""
                        shortfile = ""

                    mf = MediaFile(
                        index,
                        shortdir,
                        shortfile,
                        longdir,
                        longfile,
                        title,
                        performer,
                        album,
                        genre)

                    self.mediaFiles.append(mf)

                    log.debug(mf)

        log.info("Number of media files: {}".format(len(self.mediaFiles)))

    def finalise(self):
        """
        Write and finalise the database.
        """
        log.debug("MediaLocation finalised")
        self.database.write_db(self.mediaFiles)
        self.database.finalise()

    def __str__(self):
        """
        Return a string formatted with the location path.
        """
        return "Location: {}".format(self.path)


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg

LGFMT = '%(asctime)-15s: %(levelname)s - %(filename)s:%(lineno)d - %(message)s'


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Chris Willoughby on %s.
  Copyright 2014 Chris Willoughby. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            "-v", "--verbose",
            dest="verbose",
            action="count",
            help="set verbosity level [default: %(default)s]")
        parser.add_argument(
            "-i", "--include",
            dest="include",
            help="only include media files matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]",
            metavar="RE")
        parser.add_argument(
            "-e", "--exclude",
            dest="exclude",
            help="exclude media files matching this regex pattern. [default: %(default)s]",
            metavar="RE")
        parser.add_argument(
            '-V', '--version',
            action='version',
            version=program_version_message)
        parser.add_argument(
            dest="paths",
            help="paths to folder(s) with media file(s) [default: %(default)s]",
            metavar="path",
            nargs='+')

        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        verbose = args.verbose
        inpat = args.include
        expat = args.exclude

        if verbose is not None:
            logging.basicConfig(
                format=LGFMT,
                level=logging.DEBUG)
            log.debug("Verbose mode on")
        else:
            logging.basicConfig(
                format=LGFMT,
                level=logging.INFO)

        if inpat and expat and inpat == expat:
            raise CLIError("include and exclude pattern are equal! Nothing will be processed.")

        for inpath in paths:
            log.debug("Path: ".format(inpath))

            # Create a MediaLocation and store it in the list
            ml = MediaLocation(inpath)
            MediaLocations.append(ml)
            ml.finalise()

        log.info("Number of media locations: {}".format(len(MediaLocations)))

        return 0

    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0

#     except Exception as e:
#         if DEBUG or TESTRUN:
#             raise(e)
#         indent = len(program_name) * " "
#         sys.stderr.write(program_name + ": " + repr(e) + "\n")
#         sys.stderr.write(indent + "  for help use --help")
#         return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")

    if TESTRUN:
        import doctest
        doctest.testmod()

    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'DapGen_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)

    sys.exit(main())
