import re
import os
import logging
import struct
from . import constants
from .MainIndexEntry import MainIndexEntry
from .GenreIndexEntry import GenreIndexEntry
from .PerformerIndexEntry import PerformerIndexEntry
from .AlbumIndexEntry import AlbumIndexEntry
from .SubIndexEntry import SubIndexEntry

log = logging.getLogger(__name__)


class KenwoodDatabase(object):
    """
    The class responsible for writing the Kendwood database file.
    """

    def __init__(self, path):
        """
        Stores the path to the database and opens the file for writing.
        """

        log.info("KenwoodDatabase created at: {}".format(path))

        self.db_path = path
        # Open a file for writing
        self.db_file = open(
            os.path.join(self.db_path, "kenwood.dap"), mode='wb')

        # Create the empty list of offsets
        self.offsets = []
        for offset in range(constants.end_offsets):
            self.offsets.append(0)

        self.subIndex = []
        for sub in range(constants.end_subindex_offsets):
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

        self.db_file.write(
            struct.pack("<HH", self.number_of_entries, 0x0040))
        self.db_file.write(
            struct.pack("<HH", self.number_of_genres, 0x0010))
        self.db_file.write(
            struct.pack("<HH", self.number_of_performers, 0x0010))
        self.db_file.write(
            struct.pack("<HH", self.number_of_albums, 0x0010))
        self.db_file.write(
            struct.pack("<HH", self.number_of_playlists, 0x0010))
        self.db_file.write(
            struct.pack("<HH", 0x0001, 0x0014))

        self.db_file.write(
            b"\x01\x00\x02\x00\x00\x00\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00")
        self.db_file.write(
            b"\x00\x00\x06\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

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
            self.db_file.write(miEntry.encodedTitle)

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
            if miEntry.shortdir not in self.shortdirs:
                self.shortdirs[miEntry.shortdir] = \
                    self.db_file.tell() - start_of_shortdirs
                self.db_file.write(miEntry.encodedShortdir)
            miEntry.set_shortdir_offset(self.shortdirs[miEntry.shortdir])

    def write_shortfile_table(self):
        """
        For each of the entries in the main index, write its short filename
        to file and store its offset in the main index entry.
        """

        # KMEL actually removes duplicate short filenames from this
        # table.

        start_of_shortfiles = self.db_file.tell()

        shortfiles = {}
        for miEntry in self.mainIndex:
            short_filename = miEntry.encodedShortfile
            if short_filename in shortfiles:
                miEntry.set_shortfile_offset(
                    shortfiles[short_filename])
            else:
                shortfiles[short_filename] = \
                    self.db_file.tell() - start_of_shortfiles

                miEntry.set_shortfile_offset(
                    shortfiles[short_filename])
                self.db_file.write(short_filename)

    def write_longdir_table(self):
        """
        For each of the entries in the main index, if the long directory
        name is not already written then store the offset of its entry
        and write its name to file. If it is already written, just store
        the offset.
        """

        start_of_longdirs = self.db_file.tell()
        self.longdirs = {}
        for miEntry in self.mainIndex:
            if miEntry.longdir not in self.longdirs:
                self.longdirs[miEntry.longdir] = \
                    self.db_file.tell() - start_of_longdirs
                self.db_file.write(miEntry.encodedLongdir)
            miEntry.set_longdir_offset(self.longdirs[miEntry.longdir])

    def write_longfile_table(self):
        """
        For each of the entries in the main index, write its long filename
        to file and store its offset in the main index entry.
        """

        # KMEL actually removes duplicates long filenames from this
        # table.

        start_of_longfiles = self.db_file.tell()

        longfiles = {}
        for miEntry in self.mainIndex:

            long_filename = miEntry.encodedLongfile

            if long_filename in longfiles:

                miEntry.set_longfile_offset(
                    longfiles[long_filename])

            else:

                longfiles[long_filename] = \
                    self.db_file.tell() - start_of_longfiles

                miEntry.set_longfile_offset(
                    longfiles[long_filename])
                self.db_file.write(long_filename)

    def write_alpha_ordered_title_table(self):
        """
        """

        # print("\nAlpha Ordered Title Table")
        for title in self.alpha_ordered_titles:
            # print(title, self.mainIndex[title].title)
            self.db_file.write(struct.pack("<H", title))

    # GENRE

    def write_all_genre_tables(self):
        """
        """

        self.offsets[constants.genre_index_offset] = self.db_file.tell()
        self.write_genre_index()

        self.offsets[constants.genre_name_offset] = self.db_file.tell()
        self.write_genre_name_table()

        self.offsets[constants.genre_title_offset] = self.db_file.tell()
        self.write_genre_title_table()

        self.offsets[constants.genre_title_order_offset] = self.db_file.tell()
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
            giEntry.name_offset = (
                self.db_file.tell() - start_of_names)
            self.db_file.write(giEntry.encodedName)

    def write_genre_title_table(self):
        """
        For each entry in the Genre Index, write the indices of all media files in the Genre
        and store the offset to the start of the indices.

        Sort by genre, then album, then title
        """
        start_of_titles = self.db_file.tell()
        self.genre_title_table_length = 0
        for giEntry in self.genreIndex:
            giEntry.title_entry_offset = (
                self.db_file.tell() - start_of_titles)

            for album in sorted(giEntry.album_numbers):
                for title in sorted(
                        self.albumIndex[album].title_numbers):
                    if ((self.mainIndex[title].genre_number ==
                            giEntry.number) and
                            (self.mainIndex[title].album_number == album)):

                        self.db_file.write(
                            struct.pack(
                                "<H",
                                self.mainIndex[title].get_index()))
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
            for performer in sorted(giEntry.performer_numbers):
                for album in sorted(self.performerIndex[performer].album_numbers):
                    for title in sorted(self.albumIndex[album].title_numbers):
                        if self.mainIndex[title].genre_number == giEntry.number and \
                                self.mainIndex[title].performer_number == performer and \
                                self.mainIndex[title].album_number == album:
                            self.db_file.write(struct.pack("<H", self.mainIndex[title].get_index()))
                            self.genre_title_order_table_length += 1

        # TODO:
        if self.genre_title_order_table_length != len(self.mainIndex):
            print("2#############################################")

    # PERFORMER

    def write_all_performer_tables(self):
        self.offsets[constants.performer_index_offset] = self.db_file.tell()
        self.write_performer_index()

        self.offsets[constants.performer_name_offset] = self.db_file.tell()
        self.write_performer_name_table()

        self.offsets[constants.performer_title_offset] = self.db_file.tell()
        self.write_performer_title_table()

        self.offsets[constants.performer_title_order_offset] = \
            self.db_file.tell()
        self.write_performer_title_order_table()

    def write_performer_index(self):
        for piEntry in self.performerIndex:
            # Write to file
            self.db_file.write(piEntry.get_representation())

    def write_performer_name_table(self):
        start_of_names = self.db_file.tell()
        for piEntry in self.performerIndex:
            piEntry.name_offset = (
                self.db_file.tell() - start_of_names)
            self.db_file.write(piEntry.encodedName)

    def write_performer_title_table(self):
        start_of_titles = self.db_file.tell()
        self.performer_title_table_length = 0
        for piEntry in self.performerIndex:
            piEntry.title_entry_offset = (
                self.db_file.tell() - start_of_titles)

            for album in sorted(piEntry.album_numbers):
                for title in sorted(self.albumIndex[album].title_numbers):
                    if self.mainIndex[title].performer_number == piEntry.number and \
                            self.mainIndex[title].album_number == album:
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
            for album in sorted(piEntry.album_numbers):
                for title in sorted(self.albumIndex[album].title_numbers):
                    if self.mainIndex[title].performer_number == piEntry.number and \
                            self.mainIndex[title].album_number == album:
                        self.db_file.write(struct.pack("<H", self.mainIndex[title].get_index()))
            #for mf in piEntry.titles:
            #    self.db_file.write(struct.pack("<H", mf.get_index()))

    # ALBUM

    def write_all_album_tables(self):
        self.offsets[constants.album_index_offset] = self.db_file.tell()
        self.write_album_index()

        self.offsets[constants.album_name_offset] = self.db_file.tell()
        self.write_album_name_table()

        self.offsets[constants.album_title_offset] = self.db_file.tell()
        self.write_album_title_table()

        self.offsets[constants.album_title_order_offset] = self.db_file.tell()
        self.write_album_title_order_table()

    def write_album_index(self):
        for aiEntry in self.albumIndex:
            self.db_file.write(aiEntry.get_representation())

    def write_album_name_table(self):
        start_of_names = self.db_file.tell()
        for aiEntry in self.albumIndex:
            aiEntry.name_offset = (
                self.db_file.tell() - start_of_names)
            self.db_file.write(aiEntry.encodedName)

    def write_album_title_table(self):
        start_of_titles = self.db_file.tell()
        for aiEntry in self.albumIndex:
            aiEntry.title_entry_offset = (
                self.db_file.tell() - start_of_titles)
            for mf in aiEntry.titles:
                self.db_file.write(struct.pack("<H", mf.index))

        # TODO: KMEL seems to write this twice, but with some
        # differences (sometimes). I suspect a bug in the code.
        for aiEntry in self.albumIndex:
            for mf in aiEntry.titles:
                self.db_file.write(struct.pack("<H", mf.index))

    def write_album_title_order_table(self):
        for aiEntry in self.albumIndex:
            for mf in aiEntry.titles:
                self.db_file.write(struct.pack("<H", mf.index))

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
        self.offsets[constants.playlist_index_offset] = self.db_file.tell()
        self.write_playlist_index()

        self.offsets[constants.playlist_name_offset] = self.db_file.tell()
        self.write_playlist_name_table()

        self.offsets[constants.playlist_title_offset] = self.db_file.tell()
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
        Sub-indices starts with a relative offset (int) to the start
        of more tables.
        """

        # remember where we are.
        temp_offset_1 = self.db_file.tell()

        # Write a filler for the relative offset to the first table
        self.db_file.write(struct.pack("<I", 0x00000000))

        # Write the sub index entries (blank at this stage)
        self.write_sub_index()

        # self.subIndex[constants.sub_0_genre_performers].offset = \
        #     self.db_file.tell()
        self.write_sub_0()

        # self.subIndex[constants.sub_1_genre_performer_albums].offset = \
        #     self.db_file.tell()
        self.write_sub_1()

        # self.subIndex[constants.sub_2_genre_performer_album_titles].offset = \
        #     self.db_file.tell()
        self.write_sub_2()

        # self.subIndex[constants.sub_3_genre_ordered_titles].offset = \
        #     self.db_file.tell()
        self.write_sub_3()

        # self.subIndex[constants.sub_4_genre_albums].offset = \
        #     self.db_file.tell()
        self.write_sub_4()

        # self.subIndex[constants.sub_5_genre_album_titles].offset = \
        #     self.db_file.tell()
        self.write_sub_5()

        # self.subIndex[constants.sub_6_genre_titles].offset = \
        #     self.db_file.tell()
        self.write_sub_6()

        # self.subIndex[constants.sub_7_performer_albums].offset = \
        #     self.db_file.tell()
        self.write_sub_7()

        # self.subIndex[constants.sub_8_performer_album_titles].offset = \
        #     self.db_file.tell()
        self.write_sub_8()

        # self.subIndex[constants.sub_9_performer_titles].offset = \
        #     self.db_file.tell()
        self.write_sub_9()

        # self.subIndex[constants.sub_10_genre_performers].offset = \
        #     self.db_file.tell()
        self.write_sub_10()

        # self.subIndex[constants.sub_11_genre_performer_titles].offset = \
        #     self.db_file.tell()
        self.write_sub_11()

        # self.subIndex[constants.sub_12_genre_ordered_titles].offset = \
        #     self.db_file.tell()
        self.write_sub_12()

        # Remeber where we are
        temp_offset_2 = self.db_file.tell()

        # Go back to the start
        self.db_file.seek(temp_offset_1)

        # Write the offset to the first table
        self.db_file.write(
            struct.pack(
                "<I",
                self.subIndex[constants.sub_0_genre_performers].offset -
                temp_offset_1))

        # Write the real data now
        self.write_sub_index()

        # Go to the end
        self.db_file.seek(temp_offset_2)

    def write_sub_index(self):
        """
        This is then followed by a number (always 13) of entries that seem
        to consist of an absolute offset (int), a size (short int) and a
        count (short int).

        The absolute offset points to another table that either
        contains "count" short ints (if "size" is 2), or "count" arrays of
        4 short ints (if "size" is 8).
        """
        for sie in self.subIndex:
            self.db_file.write(sie.get_representation())

    def write_sub_0(self):
        '''
        Sub-indices Genre Performers offsets and counts (0)

        This table contains the number of Performers per Genre.

        The number of entries is the number of Genres minus 1
            (Genre 0 is excluded). The format of each entry is
            four short ints.

        The first short int is the Genre number (ascending order).
        The second short int is an offset into the next table
            (Genre Performer Albums).
        The third short int is the number of Performers in this Genre.
        The last short int is always 0.
        '''

        self.subIndex[constants.sub_0_genre_performers].offset = (
            self.db_file.tell())
        self.subIndex[constants.sub_0_genre_performers].size = 8
        self.subIndex[constants.sub_0_genre_performers].count = (
            len(self.genreIndex) - 1)

        entry_offset = 0
        for giEntry in self.genreIndex[1:]:
            # print('Sub0 {}'.format(giEntry))
            self.db_file.write(
                struct.pack(
                    "<HHHH",
                    giEntry.number,
                    entry_offset,
                    giEntry.number_of_performers,
                    0x0000))
            entry_offset += giEntry.number_of_performers

    def write_sub_1(self):
        '''
        Sub-indices Genre Performer Albums offsets and counts (1)

        This table contains the number of Albums per Performer per Genre.

        The first short int is the Performer number. Ascending order
            within Genre.
        The second short int is an offset into the next table
            (Genre Performer Album Titles).
        The third short int is the number of Albums for that Performer
            that contain the Genre.
        The last short int is always 0.
        '''
        self.subIndex[constants.sub_1_genre_performer_albums].offset = (
            self.db_file.tell())
        self.subIndex[constants.sub_1_genre_performer_albums].size = 8

        entry_offset = 0
        count = 0
        for giEntry in self.genreIndex[1:]:

            # print('Sub1 {}'.format(giEntry))

            for performer in sorted(giEntry.performer_numbers):

                # piEntry = self.performerIndex[performer]
                # number_of_albums_for_genre = 0
                # for album in sorted(piEntry.album_numbers):
                #     aiEntry = self.albumIndex[album]
                #     found = False
                #     for title in aiEntry.titles:
                #         if title.get_genre_number() == giEntry.number:
                #             found = True
                #     if found:
                #         number_of_albums_for_genre += 1

                # print("\tSub1 Performer: {}".format(
                #     giEntry.performer(performer)))

                self.db_file.write(
                    struct.pack(
                        "<HHHH",
                        performer,
                        entry_offset,
                        giEntry.number_of_albums_for_performer(performer),
                        0x0000))

                entry_offset += giEntry.number_of_albums_for_performer(
                    performer)
                count += 1

        self.subIndex[constants.sub_1_genre_performer_albums].count = count

    def write_sub_2(self):
        '''
        Sub-indices Genre Performer Album Titles offsets and counts (2)

        This table seems to contain the number of Titles per Album per
            Performer per Genre.

        The first short int is the Album number.
        The second short int is an offset into the next table
            (Genre-Ordered-Titles).
        The third short int is the number of Titles.
        The last short int is always zero.
        '''
        self.subIndex[constants.sub_2_genre_performer_album_titles].offset = (
            self.db_file.tell())
        self.subIndex[constants.sub_2_genre_performer_album_titles].size = 8

        # The first entry starts at genre 1
        # (genre 0 is for those files without a genre)
        entry_offset = len(self.genreIndex[0].titles)
        count = 0
        for giEntry in self.genreIndex[1:]:
            for performer in sorted(giEntry.performer_numbers):
                for album in sorted(self.performerIndex[performer].album_numbers):
                    # print("Sub2 Album: {}".format(album))
                    number_of_titles = \
                        giEntry.number_of_titles_for_album_for_performer(
                            performer, album)
                    if number_of_titles > 0:
                        self.db_file.write(
                            struct.pack(
                                "<HHHH",
                                album,
                                entry_offset,
                                number_of_titles,
                                0x0000))
                        entry_offset += number_of_titles
                        count += 1

        self.subIndex[constants.sub_2_genre_performer_album_titles].count = (
            count)

    def write_sub_3(self):
        """
        Sub-indices Genre-Ordered-Title List (3)

        Points to table Genre-Ordered-Title List
        """
        self.subIndex[constants.sub_3_genre_ordered_titles].offset = (
            self.offsets[constants.genre_title_order_offset])
        self.subIndex[constants.sub_3_genre_ordered_titles].size = 2
        # TODO: Could be len(mainIndex)
        self.subIndex[constants.sub_3_genre_ordered_titles].count = (
            self.genre_title_order_table_length)

    def write_sub_4(self):
        """
        Sub-indices Genre Albums offsets and counts (4)

        This table seems to contain the number of Albums per Genre.

        The number of entries is the number of Genres minus 1
            (_Genre_ 0 is excluded). The format of each entry is four
            short ints.

        The first short int is the Genre number (ascending order).
        The second short int is an offset into the next table
            (Genre Album Titles).
        The third short int is the number of Albums in this Genre.
        The last short int is always 0.
        """
        self.subIndex[constants.sub_4_genre_albums].offset = (
            self.db_file.tell())
        self.subIndex[constants.sub_4_genre_albums].size = 8
        self.subIndex[constants.sub_4_genre_albums].count = (
            len(self.genreIndex) - 1)

        entry_offset = 0
        for giEntry in self.genreIndex[1:]:
            self.db_file.write(
                struct.pack(
                    "<HHHH",
                    giEntry.number,
                    entry_offset,
                    giEntry.number_of_albums,
                    0x0000))
            entry_offset += giEntry.number_of_albums

    def write_sub_5(self):
        """
        Sub-indices Genre Album Titles offsets and counts (5)

        This table seems to contain the number of Titles per Album
            per Genre.

        The first short int is the Album number.
        The second short int is an offset into the next table
            (_Genre_ _Titles_).
        The third short int is the number of _Titles_ for that _Album_
            that contain the _Genre_.
        The last short int is always 0.
        """
        self.subIndex[constants.sub_5_genre_album_titles].offset = (
            self.db_file.tell())
        self.subIndex[constants.sub_5_genre_album_titles].size = 8

        entry_offset = len(self.genreIndex[0].titles)
        count = 0
        for giEntry in self.genreIndex[1:]:
            for album in sorted(giEntry.album_numbers):
                # print("Sub5 Album: {}".format(album))
                number_of_titles = giEntry.number_of_titles_for_album(album)
                if number_of_titles > 0:
                    self.db_file.write(
                        struct.pack(
                            "<HHHH",
                            album,
                            entry_offset,
                            number_of_titles,
                            0x0000))
                    entry_offset += number_of_titles
                    count += 1

        self.subIndex[constants.sub_5_genre_album_titles].count = (count)

    def write_sub_6(self):
        """
        Sub-indices _Genre_ _Titles_ (6)

        Points to the _Genre_ _Title_ table.
        """
        self.subIndex[constants.sub_6_genre_titles].offset = (
            self.offsets[constants.genre_title_offset])
        self.subIndex[constants.sub_6_genre_titles].size = (2)
        self.subIndex[constants.sub_6_genre_titles].count = (
            self.genre_title_table_length)  # TODO: Could be len(mainIndex)

    def write_sub_7(self):
        '''
        Sub-indices Performer Albums offsets and counts (7)

        This table seems to contain the number of Albums per Performer.

        The number of entries is the number of Performers minus 1
            (Performer 0 is excluded).
            The format of each entry is four short ints.

        The first short int is the Performer number
            (ascending order).
        The second short int is an offset into the next table
            (Performer Album Titles).
        The third short int is the number of Albums for this Performer.
        The last short int is always 0.
        '''
        self.subIndex[constants.sub_7_performer_albums].offset = (
            self.db_file.tell())
        self.subIndex[constants.sub_7_performer_albums].size = (8)
        self.subIndex[constants.sub_7_performer_albums].count = (
            len(self.performerIndex) - 1)

        entry_offset = 0
        for piEntry in self.performerIndex[1:]:
            self.db_file.write(
                struct.pack(
                    "<HHHH",
                    piEntry.number,
                    entry_offset,
                    piEntry.number_of_albums,
                    0x0000))
            entry_offset += piEntry.number_of_albums

    def write_sub_8(self):
        '''
        Sub-indices _Performer_ _Album_ _Titles_ offsets and counts (8)

        This table seems to contain the number of Titles per Album per Performer.

        The first short int is the Album number.<br>
        The second short int is an offset into the next table (Performer Titles).<br>
        The third short int is the number of Titles for the Album for the Performer.<br>
        The last short int is always 0.
        '''
        self.subIndex[constants.sub_8_performer_album_titles].offset = (
            self.db_file.tell())
        self.subIndex[constants.sub_8_performer_album_titles].size = (8)

        entry_offset = len(self.performerIndex[0].titles)
        count = 0
        for piEntry in self.performerIndex[1:]:
            for album in sorted(piEntry.album_numbers):
                # print("Sub8 Album: {}".format(album))
                number_of_titles = piEntry.number_of_titles_for_album(album)
                if number_of_titles > 0:
                    self.db_file.write(
                        struct.pack(
                            "<HHHH",
                            album,
                            entry_offset,
                            number_of_titles,
                            0x0000))
                    entry_offset += number_of_titles
                    count += 1

        self.subIndex[constants.sub_8_performer_album_titles].count = (count)

    def write_sub_9(self):
        '''
        Sub-indices Performer Titles (9)

        Points to the Performer Title table.
        '''
        self.subIndex[constants.sub_9_performer_titles].offset = (
            self.offsets[constants.performer_title_offset])
        self.subIndex[constants.sub_9_performer_titles].size = 2
        self.subIndex[constants.sub_9_performer_titles].count = (
            self.performer_title_table_length)

    def write_sub_10(self):
        '''
        Sub-indices Genre Performers offsets and counts (10)

        Points to sub-index 0.
        '''
        self.subIndex[constants.sub_10_genre_performers].offset = \
            self.subIndex[constants.sub_0_genre_performers].offset
        self.subIndex[constants.sub_10_genre_performers].size = \
            self.subIndex[constants.sub_0_genre_performers].size
        self.subIndex[constants.sub_10_genre_performers].count = \
            self.subIndex[constants.sub_0_genre_performers].count

    def write_sub_11(self):
        '''
        Sub-indices Genre Performer Titles offsets and counts (11)

        The first short int is the Performer number.
        The second short int is an offset into the next table
            (Genre-Ordered-Titles).
        The third short int is the number of _Titles_ for the _Performer_
            for the _Genre_.
        The last short int is always 0.
        '''
        self.subIndex[constants.sub_11_genre_performer_titles].offset = (
            self.db_file.tell())
        self.subIndex[constants.sub_11_genre_performer_titles].size = (8)

        entry_offset = len(self.genreIndex[0].titles)
        count = 0
        for giEntry in self.genreIndex[1:]:

            for performer in sorted(giEntry.performer_numbers):
                number_of_titles = giEntry.number_of_titles_for_performer(
                    performer)

                # print("Sub11 Performer: {} {}".format(
                #     performer, number_of_titles))

                if number_of_titles > 0:
                    self.db_file.write(
                        struct.pack(
                            "<HHHH",
                            performer,
                            entry_offset,
                            number_of_titles,
                            0x0000))
                    entry_offset += number_of_titles
                    count += 1

        self.subIndex[constants.sub_11_genre_performer_titles].count = (count)

    def write_sub_12(self):
        '''
        Sub-indices Genre-Ordered-Titles (12)

        Points to table Genre-Ordered-Title List
        '''
        self.subIndex[constants.sub_12_genre_ordered_titles].offset = (
            self.offsets[constants.genre_title_order_offset])
        self.subIndex[constants.sub_12_genre_ordered_titles].size = 2

        # TODO: Could be len(mainIndex)
        self.subIndex[constants.sub_12_genre_ordered_titles].count = (
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
        '''Constructs database from given media file list.'''

        self.write_signature()

        self.number_of_entries = len(media_files)

        # Initialise structures
        # Genres, Performers and Albums always have null string entries
        titles = []
        genres = {"": []}
        performers = {"": []}
        albums = {"": []}
        playlists = {}

        # Collect all titles, genres, performers and albums
        self.mainIndex = []
        for mf in media_files:

            titles.append((mf.title, mf.index))

            # log.debug("Genre:{}:".format(mf.genre))
            if mf.genre in genres:
                genres[mf.genre].append(mf)
            else:
                genres[mf.genre] = [mf]

            if mf.performer in performers:
                performers[mf.performer].append(mf)
            else:
                performers[mf.performer] = [mf]

            if mf.album in albums:
                albums[mf.album].append(mf)
            else:
                albums[mf.album] = [mf]

            miEntry = MainIndexEntry()
            miEntry.set_media_file(mf)
            self.mainIndex.append(miEntry)

        # TODO: International characters not sorted properly.
        # self.alpha_ordered_titles = [x[1] for x in sorted(
        #     titles, key=lambda e: e[0])]
        self.alpha_ordered_titles = [x[1] for x in sorted(
            titles, key=lambda e: re.sub("'", "", e[0].lower()))]

        # Create the Genre Index, alphabetically sorted on name
        self.genreIndex = []
        self.number_of_genres = len(genres)
        genre_number = 0
        for key in sorted(genres):
            # print ("Genre[{}] = {}".format(key, genres[key]))
            giEntry = GenreIndexEntry(
                name=key,
                titles=genres[key],
                number=genre_number)
            self.genreIndex.append(giEntry)
            genre_number += 1

        # Create the Performer Index, alphabetically sorted on name
        self.performerIndex = []
        self.number_of_performers = len(performers)
        performer_number = 0
        for key in sorted(performers):
            # print ("Performer[{}] = {}".format(key, performers[key]))
            piEntry = PerformerIndexEntry(
                name=key,
                titles=performers[key],
                number=performer_number)
            self.performerIndex.append(piEntry)
            performer_number += 1

        # Create the Album Index, alphabetically sorted on name
        self.albumIndex = []
        self.number_of_albums = len(albums)
        album_number = 0
        for key in sorted(albums):
            # print ("Album[{}] = {}".format(key, albums[key]))
            aiEntry = AlbumIndexEntry(key, albums[key], album_number)
            self.albumIndex.append(aiEntry)
            album_number += 1

        # Create the Playlist Index
        self.playlistIndex = []
        self.number_of_playlists = len(playlists)
        # TODO: Playlists

        # Write the counts
        self.write_counts()

        if self.db_file.tell() != constants.OFFSETS_OFFSET:
            log.warning("Not at correct offset for offsets table")
            self.db_file.seek(constants.OFFSETS_OFFSET)

        # These will be empty at the moment
        self.write_offsets()

        # Get the file offset, and store it as the main index offset
        self.offsets[constants.main_index_offset] = self.db_file.tell()
        self.write_main_index()

        self.offsets[constants.title_offset] = self.db_file.tell()
        self.write_title_table()

        self.offsets[constants.shortdir_offset] = self.db_file.tell()
        self.write_shortdir_table()

        self.offsets[constants.shortfile_offset] = self.db_file.tell()
        self.write_shortfile_table()

        self.offsets[constants.longdir_offset] = self.db_file.tell()
        self.write_longdir_table()

        self.offsets[constants.longfile_offset] = self.db_file.tell()
        self.write_longfile_table()

        self.offsets[constants.alpha_title_order_offset] = self.db_file.tell()
        self.write_alpha_ordered_title_table()

        for giEntry in self.genreIndex:
            giEntry.init_performers(self.performerIndex)
            giEntry.init_albums(self.albumIndex)

        for piEntry in self.performerIndex:
            piEntry.init_albums(self.albumIndex)

        # GENRE TABLES
        self.write_all_genre_tables()

        # PERFORMER TABLES
        self.write_all_performer_tables()

        # ALBUM TABLES
        self.write_all_album_tables()

        # Was table 8
        self.offsets[constants.u20_offset] = 0
        self.write_u20()

        # PLAYLISTS
        self.write_all_playlist_tables()

        # Was table 9
        self.offsets[constants.u24_offset] = self.db_file.tell()
        self.write_u24()

        # Was table 10
        self.offsets[constants.u25_offset] = self.db_file.tell()
        self.write_u25()

        # Was table 11
        self.offsets[constants.u26_offset] = self.db_file.tell()
        self.write_u26()

        # Was table 12
        self.offsets[constants.u27_offset] = self.db_file.tell()
        self.write_u27()

        # UP TO HERE

        self.offsets[constants.sub_index_offset] = self.db_file.tell()
        self.write_all_sub_indices()
        # self.write_sub_index()

        self.offsets[constants.u29_offset] = 0
        self.write_u29()

        self.offsets[constants.u30_offset] = 0
        self.write_u30()

        self.offsets[constants.u31_offset] = 0
        self.write_u31()

        self.offsets[constants.u32_offset] = 0
        self.write_u32()

        # Go back and write the offsets (now complete)
        self.db_file.seek(constants.OFFSETS_OFFSET)
        self.write_offsets()

        # Go back and write the main index (now complete)
        self.db_file.seek(self.offsets[constants.main_index_offset])
        self.write_main_index()

        # Go back and write the genre index (now complete)
        self.db_file.seek(self.offsets[constants.genre_index_offset])
        self.write_genre_index()

        # Go back and write the genre index (now complete)
        self.db_file.seek(self.offsets[constants.performer_index_offset])
        self.write_performer_index()

        # Go back and write the genre index (now complete)
        self.db_file.seek(self.offsets[constants.album_index_offset])
        self.write_album_index()

    def finalise(self):
        """
        Close the database file.
        """
        log.info("KenwoodDatabase finalised.")
        self.db_file.close()
