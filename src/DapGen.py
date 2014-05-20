#!/usr/bin/python3
# encoding: utf-8
'''
DapGen -- a Kenwood database generator.

DapGen is a media file scanner that scans a path for all media files, and generates a database for Kenwood car stereos.

It defines the following classes:
    MediaLocation
    MediaFile
    Playlist
    KenwoodDatabase

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
#import mutagen.id3 as id3
##from mutagen.id3 import ID3
from hsaudiotag import auto

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

log = logging.getLogger(__name__)

__all__ = []
__version__ = 0.1
__date__ = '2014-05-12'
__updated__ = '2014-05-12'

DEBUG = 0
TESTRUN = 1
PROFILE = 0

STRING_ENCODING = "utf_16_le"

valid_media_files = ['mp3', 'wma'];
valid_media_playlists = [];

OFFSETS_OFFSET = 0x40

# The following is the list of offsets in the offset table - DO NOT CHANGE TO INCLUDE ANYTHING ELSE
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

class Playlist(object):
    """
    An object to hold a playlist. Reads a previously created playlist for inclusion in the database.
    """
    
    def __init__(self):
        """
        Not yet implemented.
        """
        
        log.debug("Playlist created")
        
class MainIndexEntry(object):
    def __init__(self, mediafile):
        self.mediaFile = mediafile
        
        # TODO: Set later
        self.genre = 0 
        # TODO: Set later
        self.performer = 0
        # TODO: Set later
        self.album = 0
        
        self.title_length = len(self.mediaFile.title.encode(STRING_ENCODING))
        self.title_char_length = 2
        # TODO: Set later
        self.title_offset = 0 
        
        self.shortdir_length = len(self.mediaFile.shortdir.encode("ascii"))
        self.shortdir_char_length = 1
        # TODO: Set later
        self.shortdir_offset = 0 
        
        self.shortfile_length = len(self.mediaFile.shortfile.encode("ascii"))
        self.shortfile_char_length = 1
        # TODO: Set later
        self.shortfile_offset = 0 
        
        self.longdir_length = len(self.mediaFile.longdir.encode(STRING_ENCODING))
        self.longdir_char_length = 2
        # TODO: Set later
        self.longdir_offset = 0 
        
        self.longfile_length = len(self.mediaFile.longfile.encode(STRING_ENCODING))
        self.longfile_char_length = 2
        # TODO: Set later
        self.longfile_offset = 0 
        
    
    def set_genre(self, genre):
        self.genre = genre
    
    def set_performer(self, performer):
        self.performer = performer
    
    def set_album(self, album):
        self.album = album
        
    def set_title_offset(self, title_offset):
        self.title_offset = title_offset
        
    def set_shortdir_offset(self, shortdir_offset):
        self.shortdir_offset = shortdir_offset
        
    def set_shortfile_offset(self, shortfile_offset):
        self.shortfile_offset = shortfile_offset
        
    def set_longdir_offset(self, longdir_offset):
        self.longdir_offset = longdir_offset
        
    def set_longfile_offset(self, longfile_offset):
        self.longfile_offset = longfile_offset
        
    def get_representation(self):
        return struct.pack("<HHH HIII HHI HHI HHI HHI HHI I",
                           self.genre, self.performer, self.album,
                           0x0000, 0xffffffff, 0x80000000, 0x80000000,
                           self.title_length, self.title_char_length, self.title_offset,
                           self.shortdir_length, self.shortdir_char_length, self.shortdir_offset,
                           self.shortfile_length, self.shortfile_char_length, self.shortfile_offset,
                           self.longdir_length, self.longdir_char_length, self.longdir_offset,
                           self.longfile_length, self.longfile_char_length, self.longfile_offset,
                           0x00000000
                           )
    
class GenreIndexEntry(object):
    def __init__(self, name, titles):
        self.name = name + '\x00'
        self.name_length = len(self.name.encode(STRING_ENCODING))
        self.name_char_length = 2
        
        # TODO: Set later
        self.name_offset = 0
        
        self.num_titles = len(titles)
        self.titles = titles

        # TODO: Set later
        self.title_entry_offset = 0 
        
        print("\tName:{}: Length:{}: Num_Titles:{}:".format(self.name, self.name_length, self.num_titles))

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
    
class PerformerIndexEntry(object):
    def __init__(self, name, titles):
        self.name = name + '\x00'
        self.name_length = len(self.name.encode(STRING_ENCODING))
        self.name_char_length = 2
        
        # TODO: Set later
        self.name_offset = 0
        
        self.num_titles = len(titles)
        self.titles = titles

        # TODO: Set later
        self.title_entry_offset = 0 
        
        print("\tName:{}: Length:{}: Num_Titles:{}:".format(self.name, self.name_length, self.num_titles))

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
    
    
class AlbumIndexEntry(object):
    def __init__(self, name, titles):
        self.name = name + '\x00'
        self.name_length = len(self.name.encode(STRING_ENCODING))
        self.name_char_length = 2
        
        # TODO: Set later
        self.name_offset = 0
        
        self.num_titles = len(titles)
        self.titles = titles

        # TODO: Set later
        self.title_entry_offset = 0 
        
        print("\tName:{}: Length:{}: Num_Titles:{}:".format(self.name, self.name_length, self.num_titles))

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
    
class PlaylistIndexEntry(object):
    def __init__(self):
        pass
    
    def get_representation(self):
        return struct.pack("<HHIHHHH", )
    
class SubIndexEntry(object):
    def __init__(self):
        self.offset = 0
        self.size = 0
        self.count = 0

    def get_representation(self):
        return struct.pack("<IHH", self.offset, self.size, self.count)
    
class MediaFile(object):
    """
    An object to hold all the information about a given media file.
    """
    
    def __init__(self, index, shortdir, shortfile, longdir, longfile, title, performer, album, genre):
        """
        Store the given information.
        """
        self.index = index
        self.shortdir = shortdir + "\x00"
        self.shortfile = shortfile + "\x00"
        self.longdir = longdir + "\x00"
        self.longfile = longfile + "\x00"
        self.title = title + "\x00"
        self.performer = performer
        self.album = album
        self.genre = genre
    
    def __repr__(self):
        return "MediaFile({})".format(self.title)
    
    def __str__(self):
        """
        Return a string formatted with the media file information.
        """
        return "\n\tLongDir: {}\n\tLongFile: {}\n\tTitle: {}\n\tPerfomer: {}\n\tAlbum: {}\n\tGenre: {}".format(self.longdir,
                                                                                                               self.longfile,
                                                                                                               self.title,
                                                                                                               self.performer,
                                                                                                               self.album,
                                                                                                               self.genre)

class KenwoodDatabase(object):
    def __init__(self, path):
        log.debug("KenwoodDatabase created at: {}.".format(path))
        self.db_path = path
        # Open a file for writing
        self.db_file = open(os.path.join(self.db_path, "kenwood.dap"), mode='wb')
        
        # Create the empty list of offsets
        self.offsets = []
        for offset in range(end_offsets):
            self.offsets.append(0)
        
    def write_signature(self):
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
        
        self.db_file.write(struct.pack("<HH", self.number_of_entries,    0x0040))
        self.db_file.write(struct.pack("<HH", self.number_of_genres,     0x0010))
        self.db_file.write(struct.pack("<HH", self.number_of_performers, 0x0010))
        self.db_file.write(struct.pack("<HH", self.number_of_albums,     0x0010))
        self.db_file.write(struct.pack("<HH", self.number_of_playlists,  0x0010))
        self.db_file.write(struct.pack("<HH", 0x0001,  0x0014))
        
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
        for mie in self.mainIndex:
            self.db_file.write(mie.get_representation())
    
    def write_title_table(self):
        start_of_titles = self.db_file.tell()
        for mie in self.mainIndex:
            mie.set_title_offset(self.db_file.tell() - start_of_titles)
            self.db_file.write(mie.mediaFile.title.encode(STRING_ENCODING))
            
    def write_shortdir_table(self):
        start_of_shortdirs = self.db_file.tell()
        self.shortdirs = []
        for mie in self.mainIndex:
            if mie.mediaFile.shortdir not in self.shortdirs:
                self.shortdirs.append(mie.mediaFile.shortdir)
                mie.set_shortdir_offset(self.db_file.tell() - start_of_shortdirs)
                self.db_file.write(mie.mediaFile.shortdir.encode("ascii"))
    
    def write_shortfile_table(self):
        start_of_shortfiles = self.db_file.tell()
        for mie in self.mainIndex:
            mie.set_shortfile_offset(self.db_file.tell() - start_of_shortfiles)
            self.db_file.write(mie.mediaFile.shortfile.encode("ascii"))
    
    def write_longdir_table(self):
        start_of_longdirs = self.db_file.tell()
        self.longdirs = []
        for mie in self.mainIndex:
            if mie.mediaFile.longdir not in self.longdirs:
                self.longdirs.append(mie.mediaFile.longdir)
                mie.set_longdir_offset(self.db_file.tell() - start_of_longdirs)
                self.db_file.write(mie.mediaFile.longdir.encode(STRING_ENCODING))
    
    def write_longfile_table(self):
        start_of_longfiles = self.db_file.tell()
        for mie in self.mainIndex:
            mie.set_longfile_offset(self.db_file.tell() - start_of_longfiles)
            self.db_file.write(mie.mediaFile.longfile.encode(STRING_ENCODING))
    
    def write_alpha_ordered_title_table(self):
        for title in self.alpha_ordered_titles:
            print(title, self.mainIndex[title].mediaFile.title)
            self.db_file.write(struct.pack("<H", title))
    
    # GENRE
    
    def write_all_genre_tables(self):
        self.offsets[genre_index_offset] = self.db_file.tell()
        self.write_genre_index()

        self.offsets[genre_name_offset] = self.db_file.tell()
        self.write_genre_name_table()
        
        self.offsets[genre_title_offset] = self.db_file.tell()
        self.write_genre_title_table()
        
        self.offsets[genre_title_order_offset] = self.db_file.tell()
        self.write_genre_title_order_table()
    
    def write_genre_index(self):
        for gi in self.genreIndex:
            self.db_file.write(gi.get_representation())
            
    def write_genre_name_table(self):
        start_of_names = self.db_file.tell()
        for gi in self.genreIndex:
            gi.set_name_offset(self.db_file.tell() - start_of_names)
            self.db_file.write(gi.name.encode(STRING_ENCODING))
    
    def write_genre_title_table(self):
        start_of_titles = self.db_file.tell()
        for gi in self.genreIndex:
            gi.set_title_entry_offset(self.db_file.tell() - start_of_titles)
            for mf in gi.titles:
                self.db_file.write(struct.pack("<H", mf.index))
    
    def write_genre_title_order_table(self):
        for gie in self.genreIndex:
            for mf in gie.titles:
                self.db_file.write(struct.pack("<H", mf.index))
    
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
        for pie in self.performerIndex:
            self.db_file.write(pie.get_representation())
    
    def write_performer_name_table(self):
        start_of_names = self.db_file.tell()
        for pie in self.performerIndex:
            pie.set_name_offset(self.db_file.tell() - start_of_names)
            self.db_file.write(pie.name.encode(STRING_ENCODING))
    
    def write_performer_title_table(self):
        start_of_titles = self.db_file.tell()
        for pie in self.performerIndex:
            pie.set_title_entry_offset(self.db_file.tell() - start_of_titles)
            for mf in pie.titles:
                self.db_file.write(struct.pack("<H", mf.index))
    
    def write_performer_title_order_table(self):
        for pie in self.performerIndex:
            for mf in pie.titles:
                self.db_file.write(struct.pack("<H", mf.index))
    
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
        for aie in self.albumIndex:
            self.db_file.write(aie.get_representation())
    
    def write_album_name_table(self):
        start_of_names = self.db_file.tell()
        for aie in self.albumIndex:
            aie.set_name_offset(self.db_file.tell() - start_of_names)
            self.db_file.write(aie.name.encode(STRING_ENCODING))
    
    def write_album_title_table(self):
        start_of_titles = self.db_file.tell()
        for aie in self.albumIndex:
            aie.set_title_entry_offset(self.db_file.tell() - start_of_titles)
            for mf in aie.titles:
                self.db_file.write(struct.pack("<H", mf.index))
    
    def write_album_title_order_table(self):
        for aie in self.albumIndex:
            for mf in aie.titles:
                self.db_file.write(struct.pack("<H", mf.index))
    
    # Was table 8
    def write_u20(self):
        """
        Table 20 has no contents - pass.
        """
        pass
    
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
        for pi in self.playlistIndex:
            self.db_file.write(pi.get_representation())
    
    def write_playlist_name_table(self):
        """
        TODO: Not yet implemented
        """
        pass
    
    def write_playlist_title_table(self):
        """
        TODO: Not yet implemented
        """
        pass
    
    # Was table 9
    def write_u24(self):
        self.db_file.write(b"\xFF\xFF\xFF\xFF\x00\x00\x00\x00\x02\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    
    # Was table 10
    def write_u25(self):
        self.db_file.write(b"\x00\x00")
    
    # Was table 11
    def write_u26(self):
        for ai in range(len(self.albumIndex)):
            self.db_file.write(b"\x00\x00\x00\x00")
    
    # Was table 12
    def write_u27(self):
        for mi in range(len(self.mainIndex)):
            self.db_file.write(b"\x00\x00\x00\x00")
    
    def write_sub_index(self):
        """
        TODO: Not yet implemented
        """
        
        # Write relative offset to the tables
        
        # Write all thirteen tables
        pass
    
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
            
            titles.append((mf.title, mf.index))
            
            #log.debug("Genre:{}:".format(mf.genre))
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
            
            mie = MainIndexEntry(mf)
            self.mainIndex.append(mie)
        
        self.alpha_ordered_titles = [x[1] for x in sorted(titles, key=lambda e: e[0])]
        
        self.genreIndex = []
        self.number_of_genres = len(genres)
        for key in sorted(genres):
            print ("Genre[{}] = {}".format(key, genres[key]))
            gie = GenreIndexEntry(key, genres[key])
            self.genreIndex.append(gie)
            
        self.performerIndex = []
        self.number_of_performers = len(performers)
        for key in sorted(performers):
            print ("Performer[{}] = {}".format(key, performers[key]))
            pie = PerformerIndexEntry(key, performers[key])
            self.performerIndex.append(pie)
            
        self.albumIndex = []
        self.number_of_albums = len(albums)
        for key in sorted(albums):
            print ("Album[{}] = {}".format(key, albums[key]))
            aie = AlbumIndexEntry(key, albums[key])
            self.albumIndex.append(aie)
            
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
        self.write_sub_index()
        
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
        log.debug("KenwoodDatabase finalised.")
        self.db_file.close()
        
# Holds the list of all media locations        
MediaLocations = []

class MediaLocation(object):
    """
    An object to hold the media files within a given directory path.
    """
    
    def __init__(self, path):
        """
        Store the path, create empty lists in which to store media files and playlists.
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
                    log.debug("{}".format(os.path.join(root,media_file)))

                    title = ""
                    performer = ""
                    album = ""
                    genre = ""
                        
                    # TODO: Determine what to do when there is no ID3 information
                    # Title <- filename
                    # Album <- directory?
                    # Performer <- directory?
                    # Genre <- 0
                    metadata = auto.File(os.path.join(root,media_file))
                    title = metadata.title
                    performer = metadata.artist
                    album = metadata.album
                    genre = metadata.genre

                    #try:
                    #    metadata = id3.ID3(os.path.join(root,media_file))
                    #except id3.ID3NoHeaderError:
                    #    log.warning("No ID3 Header: {}".format(media_file))
                    #    metadata = {}
                    #    
                    #if 'TIT2' in metadata:
                    #    title = str(metadata['TIT2'])
                    #        
                    #if 'TPE1' in metadata:
                    #    performer = str(metadata['TPE1'])
                    #        
                    #if 'TALB' in metadata:
                    #    album = str(metadata['TALB'])
                    #        
                    #if 'TCON' in metadata:
                    #    genre = str(metadata['TCON'])
                    
                    shortdir = ""
                    shortfile = ""
                    longdir = os.path.relpath(root, self.path)
                    longfile = media_file
                    
                    mf = MediaFile(index, shortdir, shortfile, longdir, longfile, title, performer, album, genre)
                        
                    self.mediaFiles.append(mf)
                        
                    log.debug(mf)
                
        log.info("Number of media files: {}".format(len(self.mediaFiles)))
        
    def finalise(self):
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

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
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
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-i", "--include", dest="include", help="only include media files matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
        parser.add_argument("-e", "--exclude", dest="exclude", help="exclude media files matching this regex pattern. [default: %(default)s]", metavar="RE" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="paths", help="paths to folder(s) with media file(s) [default: %(default)s]", metavar="path", nargs='+')
        
        # Process arguments
        args = parser.parse_args()
        
        paths = args.paths
        verbose = args.verbose
        inpat = args.include
        expat = args.exclude
        
        if verbose != None:
            logging.basicConfig(format='%(asctime)-15s: %(levelname)s - %(filename)s:%(lineno)d - %(message)s', level=logging.DEBUG)
            log.debug("Verbose mode on")
        else:
            logging.basicConfig(format='%(asctime)-15s: %(levelname)s - %(filename)s:%(lineno)d - %(message)s', level=logging.INFO)
        
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
        ### handle keyboard interrupt ###
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
