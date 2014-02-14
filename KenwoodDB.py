#!/usr/bin/env /usr/bin/python3

import argparse
import logging
import struct

log = logging.getLogger(__name__)
FORMAT = '##### %(message)s'
logging.basicConfig(format=FORMAT)
log.setLevel(logging.INFO)

(
    signature,
    u1,
    
    title_count,
    title_entry_size,
    
    genre_count,
    genre_entry_size,
    
    performer_count,
    performer_entry_size,
    
    album_count,
    album_entry_size,
    
    playlist_count,
    playlist_entry_size,
    
    u2,
    u3,
    
    main_index_offset,
    title_offset,
    shortdir_offset,
    shortfile_offset,
    longdir_offset,
    longfile_offset,
    
    u4,
    
    genre_index_offset,
    genre_name_offset,
    genre_title_offset,
    
    u5,
    
    performer_index_offset,
    performer_name_offset,
    performer_title_offset,
    
    u6,
    
    album_index_offset,
    album_name_offset,
    album_title_offset,
    
    u7,
    u8,
    
    playlist_index_offset,
    playlist_name_offset,
    playlist_title_offset,
    
    u9,
    u10,
    u11,
    u12,
    u13,
    end
) = list(range(43))

# file_offsets is a dictionary of tuples containing the file offset, format and name of the DB file header
file_offsets = {
    signature:              (0x00, "<4s", "signature"),
    u1:                     (0x04, "<HH", "u1"),
    title_count:            (0x08, "<H", "title_count"),
    title_entry_size:       (0x0a, "<H", "title_entry_size"),
    genre_count:            (0x0c, "<H", "genre_count"),
    genre_entry_size:       (0x0e, "<H", "genre_entry_size"),
    performer_count:        (0x10, "<H", "performer_count"),
    performer_entry_size:   (0x12, "<H", "performer_entry_size"),
    album_count:            (0x14, "<H", "album_count"),
    album_entry_size:       (0x16, "<H", "album_entry_size"),
    playlist_count:         (0x18, "<H", "playlist_count"),
    playlist_entry_size:    (0x1a, "<H", "playlist_entry_size"),
    u2:                     (0x1c, "<H", "u2"),
    u3:                     (0x1e, "<H", "u3"),
    main_index_offset:      (0x40, "<I", "main_index_offset"),
    title_offset:           (0x44, "<I", "title_offset"),
    shortdir_offset:        (0x48, "<I", "shortdir_offset"),
    shortfile_offset:       (0x4c, "<I", "shortfile_offset"),
    longdir_offset:         (0x50, "<I", "longdir_offset"),
    longfile_offset:        (0x54, "<I", "longfile_offset"),
    u4:                     (0x58, "<I", "u4"),
    genre_index_offset:     (0x5c, "<I", "genre_index_offset"),
    genre_name_offset:      (0x60, "<I", "genre_name_offset"),
    genre_title_offset:     (0x64, "<I", "genre_title_offset"),
    u5:                     (0x68, "<I", "u5"),
    performer_index_offset: (0x6c, "<I", "performer_index_offset"),
    performer_name_offset:  (0x70, "<I", "performer_name_offset"),
    performer_title_offset: (0x74, "<I", "performer_title_offset"),
    u6:                     (0x78, "<I", "u6"),
    album_index_offset:     (0x7c, "<I", "album_index_offset"),
    album_name_offset:      (0x80, "<I", "album_name_offset"),
    album_title_offset:     (0x84, "<I", "album_title_offset"),
    u7:                     (0x88, "<I", "u7"),
    u8:                     (0x8c, "<I", "u8"),
    playlist_index_offset:  (0x90, "<I", "playlist_index_offset"),
    playlist_name_offset:   (0x94, "<I", "playlist_name_offset"),
    playlist_title_offset:  (0x98, "<I", "playlist_title_offset"),
    u9:                     (0x9c, "<I", "u9"),
    u10:                    (0xa0, "<I", "u10"),
    u11:                    (0xa4, "<I", "u11"),
    u12:                    (0xa8, "<I", "u12"),
    u13:                    (0xac, "<I", "u13")
}

INDEX_FORMAT = "<HHHHIIIHHIHHIHHIHHIHHII"
GENRE_INDEX_FORMAT = "<HHIHHHH"
PERFORMER_INDEX_FORMAT = "<HHIHHHH"
ALBUM_INDEX_FORMAT = "<HHIHHHH"
PLAYLIST_INDEX_FORMAT = "<HHIHHHH"

class MainIndexEntry(object):
    def __init__(self, values):
        self.genre = values[0]
        self.performer = values[1]
        self.album = values[2]

        self.u1 = values[3]
        if self.u1 != 0x0000:
            log.warning ("Unexpected main index u1 value")

        self.u2 = values[4]
        if self.u2 != 0xffffffff:
            log.warning ("Unexpected main index u2 value")

        self.u3 = values[5]
        if self.u3 != 0x80000000:
            log.warning ("Unexpected main index u3 value")

        self.u4 = values[6]
        if self.u4 != 0x80000000:
            log.warning ("Unexpected main index u4 value")

        self.title_length = values[7]
        self.title_char = values[8]
        self.title_offset = values[9]
        if self.title_char != 0x02:
            log.warning ("Unexpected title char value")

        self.shortdir_length = values[10]
        self.shortdir_char = values[11]
        self.shortdir_offset = values[12]
        if self.shortdir_char != 0x01:
            log.warning ("Unexpected shortdir char value")

        self.shortfile_length = values[13]
        self.shortfile_char = values[14]
        self.shortfile_offset = values[15]
        if self.shortfile_char != 0x01:
            log.warning ("Unexpected shortfile char value")

        self.longdir_length = values[16]
        self.longdir_char = values[17]
        self.longdir_offset = values[18]
        if self.longdir_char != 0x02:
            log.warning ("Unexpected longdir char value")

        self.longfile_length = values[19]
        self.longfile_char = values[20]
        self.longfile_offset = values[21]
        if self.longfile_char != 0x02:
            log.warning ("Unexpected longfile char value")

        self.u5 = values[22]
        if self.u5 != 0x00000000:
            log.warning ("Unexpected main index u5 value")

    def set_genre(self, genre):
        self.genre = genre
        log.debug (self.genre)

    def set_performer(self, performer):
        self.performer = performer
        log.debug (self.performer)

    def set_album(self, album):
        self.album = album
        log.debug (self.album)

    def set_title(self, title):
        self.title = title
        log.debug (self.title)

    def set_shortdir(self, shortdir):
        self.shortdir = shortdir
        log.debug ("\t{}".format(self.shortdir))

    def set_shortfile(self, shortfile):
        self.shortfile = shortfile
        log.debug ("\t{}".format(self.shortfile))

    def set_longdir(self, longdir):
        self.longdir = longdir
        log.debug ("\t{}".format(self.longdir))

    def set_longfile(self, longfile):
        self.longfile = longfile
        log.debug ("\t{}".format(self.longfile))

class BaseIndexEntry(object):
    def __init__(self, values):
        self.identifier = "Base"

    def set_dir_count(self, dir_count):
        self.dir_count = dir_count

    def set_title_count(self, title_count):
        self.title_count = title_count

    def set_genre_count(self, genre_count):
        self.genre_count = genre_count

    def set_performer_count(self, performer_count):
        self.performer_count = performer_count

    def set_album_count(self, album_count):
        self.album_count = album_count

    def set_playlist_count(self, playlist_count):
        self.playlist_count = playlist_count

    def set_name(self, name):
        self.name = name
        log.debug ("{} name: {}".format(self.identifier, self.name))

    def set_titles(self, titles, entries):
        self.titles = titles
        self.set_title_count(len(self.titles))

        log.debug ("\t{} titles: {}".format(self.identifier, self.titles))

        # Count things
        dirlist = []
        genlist = []
        perflist = []
        alblist = []
        for title in self.titles:
            if entries[title].longdir not in dirlist:
                dirlist.append(entries[title].longdir)
            if entries[title].genre not in genlist:
                genlist.append(entries[title].genre)
            if entries[title].performer not in perflist:
                perflist.append(entries[title].performer)
            if entries[title].album not in alblist:
                alblist.append(entries[title].album)
        self.set_dir_count(len(dirlist))
        self.set_genre_count(len(genlist))
        self.set_performer_count(len(perflist))
        self.set_album_count(len(alblist))

    def __str__(self):
        contents = "{}: {}, titles: {}".format(self.identifier, self.name, str(self.titles))
        return contents


class GenreIndexEntry(BaseIndexEntry):
    def __init__(self, values):
        self.identifier = "Genre"
        self.name_length = values[0]
        self.name_char = values[1]
        if self.name_char != 0x02:
            log.warning ("Unexpected genre name character length")
        self.name_offset = values[2]
        self.u1 = values[3]
        if self.u1 != 0x00:
            log.warning ("Unexpected genre u1 value")
        self.titles_count = values[4]
        self.titles_offset = values[5]
        self.u2 = values[6]
        if self.u2 != 0x00:
            log.warning ("Unexpected genre u2 value")

class PerformerIndexEntry(BaseIndexEntry):
    def __init__(self, values):
        self.identifier = "Performer"
        self.name_length = values[0]
        self.name_char = values[1]
        if self.name_char != 0x02:
            log.warning ("Unexpected performer name character length")
        self.name_offset = values[2]
        self.u1 = values[3]
        if self.u1 != 0x00:
            log.warning ("Unexpected performer u1 value")
        self.titles_count = values[4]
        self.titles_offset = values[5]
        self.u2 = values[6]
        if self.u2 != 0x00:
            log.warning ("Unexpected performer u2 value")

class AlbumIndexEntry(BaseIndexEntry):
    def __init__(self, values):
        self.identifier = "Album"
        self.name_length = values[0]
        self.name_char = values[1]
        if self.name_char != 0x02:
            log.warning ("Unexpected album name character length")
        self.name_offset = values[2]
        self.u1 = values[3]
        if self.u1 != 0x00:
            log.warning ("Unexpected album u1 value")
        self.titles_count = values[4]
        self.titles_offset = values[5]
        self.u2 = values[6]
        if self.u2 != 0x00:
            log.warning ("Unexpected album u2 value")

class PlaylistIndexEntry(BaseIndexEntry):
    def __init__(self, values):
        self.identifier = "Playlist"
        self.name_length = values[0]
        self.name_char = values[1]
        if self.name_char != 0x02:
            log.warning ("Unexpected playlist name character length")
        self.name_offset = values[2]
        self.u1 = values[3]
        if self.u1 != 0x00:
            log.warning ("Unexpected playlist u1 value")
        self.titles_count = values[4]
        self.titles_offset = values[5]
        self.u2 = values[6]
        if self.u2 != 0x00:
            log.warning ("Unexpected playlist u2 value")

class U13IndexEntry(object):
    def __init__(self, values):
        self.offset = values[0]
        self.size = values[1]
        self.count = values[2]

class DBfile(object):
    def __init__(self, filename):
        f = open(filename, 'rb')
        self.db = f.read()
        f.close()

        self.details = []
        for index in range(end):
            self.details.append(struct.unpack_from(file_offsets[index][1], self.db, file_offsets[index][0]))

        self.parse_u2()
        self.parse_u3()
        self.parse_main_index()
        self.parse_u4()
        self.parse_genres()
        self.parse_u5()
        self.parse_performers()
        self.parse_u6()
        self.parse_albums()
        self.parse_u7()
        self.parse_u8()
        self.parse_playlists()
        self.parse_u9()
        self.parse_u10()
        self.parse_u11()
        self.parse_u12()
        self.parse_u13()

    def parse_u2(self):
        log.debug("Parsing u2")
        if self.details[u2][0] != 0x0001:
            log.warning("Unexpected u2 value")

    def parse_u3(self):
        log.debug("Parsing u3")
        if self.details[u3][0] != 0x0014:
            log.warning("Unexpected u3 value")

    def parse_main_index(self):
        log.debug("Parsing main index")
        self.entries = []
        if self.details[title_entry_size][0] != struct.calcsize(INDEX_FORMAT):
            log.warning ("Unexpected index size")
        current = self.details[main_index_offset][0]
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from(INDEX_FORMAT, self.db, current)
            main_index_entry = MainIndexEntry(value)

            title = self.db[
                self.details[title_offset][0] + main_index_entry.title_offset:
                self.details[title_offset][0] + main_index_entry.title_offset + main_index_entry.title_length - main_index_entry.title_char].decode('utf-16')
            main_index_entry.set_title(title)

            shortdir = self.db[
                self.details[shortdir_offset][0] + main_index_entry.shortdir_offset:
                self.details[shortdir_offset][0] + main_index_entry.shortdir_offset + main_index_entry.shortdir_length - main_index_entry.shortdir_char].decode('ascii')
            main_index_entry.set_shortdir(shortdir)

            shortfile = self.db[
                self.details[shortfile_offset][0] + main_index_entry.shortfile_offset:
                self.details[shortfile_offset][0] + main_index_entry.shortfile_offset + main_index_entry.shortfile_length - main_index_entry.shortfile_char].decode('ascii')
            main_index_entry.set_shortfile(shortfile)

            longdir = self.db[
                self.details[longdir_offset][0] + main_index_entry.longdir_offset:
                self.details[longdir_offset][0] + main_index_entry.longdir_offset + main_index_entry.longdir_length - main_index_entry.longdir_char].decode('utf-16')
            main_index_entry.set_longdir(longdir)

            longfile = self.db[
                self.details[longfile_offset][0] + main_index_entry.longfile_offset:
                self.details[longfile_offset][0] + main_index_entry.longfile_offset + main_index_entry.longfile_length - main_index_entry.longfile_char].decode('utf-16')
            main_index_entry.set_longfile(longfile)

            self.entries.append(main_index_entry)
            current += self.details[title_entry_size][0]

    def parse_u4(self):
        """The u4 table is currently unknown, but seems to consist of an array (length title_count) of short ints.
        """
        log.debug("Parsing u4")
        print ("u4 offset: {:08x}".format(self.details[u4][0]))
        current = self.details[u4][0]
        increment = struct.calcsize("<H")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            # Is this a list of titles?
            print ("\t{}".format(self.entries[value[0]].title))
            current += increment
        if current != self.details[genre_index_offset][0]:
            log.warning("Unexpected u4 end offset")

    def parse_genres(self):
        log.debug("Parsing genres")
        self.genres = []
        if self.details[genre_entry_size][0] != struct.calcsize(GENRE_INDEX_FORMAT):
            log.warning ("Unexpected genre index size")
        current = self.details[genre_index_offset][0]
        for index in range(self.details[genre_count][0]):
            value = struct.unpack_from(GENRE_INDEX_FORMAT, self.db, current)
            genre_index_entry = GenreIndexEntry(value)

            name = self.db[
                self.details[genre_name_offset][0] + genre_index_entry.name_offset:
                self.details[genre_name_offset][0] + genre_index_entry.name_offset + genre_index_entry.name_length - genre_index_entry.name_char].decode('utf-16')
            genre_index_entry.set_name(name)

            titles = []
            titles_current = self.details[genre_title_offset][0] + genre_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(genre_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            genre_index_entry.set_titles(titles, self.entries)

            self.genres.append(genre_index_entry)
            current += self.details[genre_entry_size][0]

    def parse_u5(self):
        log.debug("Parsing u5")
        print ("u5 offset: {:08x}".format(self.details[u5][0]))
        current = self.details[u5][0]
        increment = struct.calcsize("<H")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            print ("\t{}".format(self.entries[value[0]].title))
            current += increment
        if current != self.details[performer_index_offset][0]:
            log.warning("Unexpected u5 end offset")

        # Compare it to the previous table - not the same
#        current = self.details[u5][0]
#        prev_current = self.details[genre_title_offset][0]
#        for index in range(self.details[title_count][0]):
#            value1 = struct.unpack_from("<H", self.db, current)
#            value2 = struct.unpack_from("<H", self.db, prev_current)
#            if value1 != value2:
#                log.warning("u5 is not the same as genre title")
#            current += increment
#            prev_current += increment

    def parse_performers(self):
        log.debug("Parsing performers")
        self.performers = []
        if self.details[performer_entry_size][0] != struct.calcsize(PERFORMER_INDEX_FORMAT):
            log.warning ("Unexpected performer index size")
        current = self.details[performer_index_offset][0]
        for index in range(self.details[performer_count][0]):
            value = struct.unpack_from(PERFORMER_INDEX_FORMAT, self.db, current)
            performer_index_entry = PerformerIndexEntry(value)

            name = self.db[
                self.details[performer_name_offset][0] + performer_index_entry.name_offset:
                self.details[performer_name_offset][0] + performer_index_entry.name_offset + performer_index_entry.name_length - performer_index_entry.name_char].decode('utf-16')
            performer_index_entry.set_name(name)

            titles = []
            titles_current = self.details[performer_title_offset][0] + performer_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(performer_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            performer_index_entry.set_titles(titles, self.entries)

            self.performers.append(performer_index_entry)
            current += self.details[performer_entry_size][0]

    def parse_u6(self):
        log.debug("Parsing u6")
        print ("u6 offset: {:08x}".format(self.details[u6][0]))
        current = self.details[u6][0]
        increment = struct.calcsize("<H")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            print ("\t{}".format(self.entries[value[0]].title))
            current += increment
        if current != self.details[album_index_offset][0]:
            log.warning("Unexpected u6 end offset")

        # Compare it to the previous table - not the same
#        current = self.details[u6][0]
#        prev_current = self.details[performer_title_offset][0]
#        for index in range(self.details[title_count][0]):
#            value1 = struct.unpack_from("<H", self.db, current)
#            value2 = struct.unpack_from("<H", self.db, prev_current)
#            if value1 != value2:
#                log.warning("u6 is not the same as genre title")
#            current += increment
#            prev_current += increment

    def parse_albums(self):
        log.debug("Parsing albums")
        self.albums = []
        if self.details[album_entry_size][0] != struct.calcsize(ALBUM_INDEX_FORMAT):
            log.warning ("Unexpected album index size")
        current = self.details[album_index_offset][0]
        for index in range(self.details[album_count][0]):
            value = struct.unpack_from(ALBUM_INDEX_FORMAT, self.db, current)
            album_index_entry = AlbumIndexEntry(value)

            name = self.db[
                self.details[album_name_offset][0] + album_index_entry.name_offset:
                self.details[album_name_offset][0] + album_index_entry.name_offset + album_index_entry.name_length - album_index_entry.name_char].decode('utf-16')
            album_index_entry.set_name(name)

            titles = []
            titles_current = self.details[album_title_offset][0] + album_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(album_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            album_index_entry.set_titles(titles, self.entries)

            self.albums.append(album_index_entry)
            current += self.details[album_entry_size][0]

    def parse_u7(self):
        log.debug("Parsing u7")
        print ("u7 offset: {:08x}".format(self.details[u7][0]))
        current = self.details[u7][0]
        increment = struct.calcsize("<H")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            print ("\t{}".format(self.entries[value[0]].title))
            current += increment
        if current != self.details[playlist_index_offset][0]:
            log.warning("Unexpected u7 end offset")


    def parse_u8(self):
        log.debug("Parsing u8")
        print ("u8 offset: {:08x}".format(self.details[u8][0]))
        if self.details[u8][0] != 0x00000000:
            log.warning("Unexpected value for u8 offset")

    def parse_playlists(self):
        log.debug("Parsing playlists")
        self.playlists = []
        if self.details[playlist_entry_size][0] != struct.calcsize(PLAYLIST_INDEX_FORMAT):
            log.warning ("Unexpected playlist index size")
        current = self.details[playlist_index_offset][0]
        for index in range(self.details[playlist_count][0]):
            value = struct.unpack_from(PLAYLIST_INDEX_FORMAT, self.db, current)
            playlist_index_entry = PlaylistIndexEntry(value)

            name = self.db[
                self.details[playlist_name_offset][0] + playlist_index_entry.name_offset:
                self.details[playlist_name_offset][0] + playlist_index_entry.name_offset + playlist_index_entry.name_length - playlist_index_entry.name_char].decode('utf-16')
            playlist_index_entry.set_name(name)

            titles = []
            titles_current = self.details[playlist_title_offset][0] + playlist_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(playlist_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            playlist_index_entry.set_titles(titles, self.entries)

            self.playlists.append(playlist_index_entry)
            current += self.details[playlist_entry_size][0]

    def parse_u9(self):
        log.debug("Parsing u9")
        print ("u9 offset: {:08x}".format(self.details[u9][0]))
        current = self.details[u9][0]
        increment = struct.calcsize("<HHHHHHHHHH")
        value = struct.unpack_from("<HHHHHHHHHH", self.db, current)
        if value != (65535, 65535, 0, 0, 2, 2, 0, 0, 0, 0):
            log.warning("Unexpected u9 values")
        current += increment
        if current != self.details[u10][0]:
            log.warning("Unexpected u9 end offset")
        

    def parse_u10(self):
        log.debug("Parsing u10")
        print ("u10 offset: {:08x}".format(self.details[u10][0]))
        current = self.details[u10][0]
        increment = struct.calcsize("<H")
        value = struct.unpack_from("<H", self.db, current)
        if value != (0,):
            log.warning("Unexpected u10 value")
        current += increment
        if current != self.details[u11][0]:
            log.warning("Unexpected u10 end offset")
        
    def parse_u11(self):
        log.debug("Parsing u11")
        print ("u11 offset: {:08x}".format(self.details[u11][0]))
        current = self.details[u11][0]
        increment = struct.calcsize("<I")
        for index in range(self.details[album_count][0]):
            value = struct.unpack_from("<I", self.db, current)
            if value[0] != 0x00:
                log.warning ("Unexpected u11 value {}".format(value[0]))
            current += increment
        if current != self.details[u12][0]:
            log.warning("Unexpected u11 end offset")

    def parse_u12(self):
        log.debug("Parsing u12")
        print ("u12 offset: {:08x}".format(self.details[u12][0]))
        current = self.details[u12][0]
        increment = struct.calcsize("<I")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<I", self.db, current)
            if value[0] != 0x00:
                log.warning ("Unexpected u12 value {}".format(value[0]))
            current += increment
        if current != self.details[u13][0]:
            log.warning("Unexpected u12 end offset")

    def parse_u13(self):
        log.debug("Parsing u13")
        print ("u13 offset: {:08x}".format(self.details[u13][0]))
        current = self.details[u13][0]
        
        # this seems to be the offset of some data
        data_start_offset = struct.unpack_from("<I", self.db, current)
        if data_start_offset[0] != 0x6c:
            log.warning("Unexpected u13 data_start_offset")
        data_start = current + data_start_offset[0]
        current += struct.calcsize("<I")
        increment = struct.calcsize("<IHH")
        num = 0
        
        self.u13s = []

        # read the index up to the beginning of the data
        while current < data_start:

            # seems to be an offset, size, count
            u13_index_element = U13IndexEntry(struct.unpack_from("<IHH", self.db, current))
            self.u13s.append(u13_index_element)

            # TODO: size and count may be row and column?
            u13offset, u13size, u13count = struct.unpack_from("<IHH", self.db, current)
            print ("UNK13 Index 0x%x @ 0x%x: Offset 0x%x, Size 0x%x, Count 0x%x" % (num, current, u13offset, u13size, u13count))
            
            known = False

            if num in [0, 1, 4, 5, 6, 7, 9, 10]:
                known = True

            if u13size == 2:
                u13fmt = "<H"
            elif u13size == 8:
                u13fmt = "<HHHH"
            else:
                log.warning("Unexpected u13size")
                u13fmt = "<H"
                
            if not known:
                increment1 = struct.calcsize(u13fmt)
                for index1 in range(u13count):
                    value = struct.unpack_from(u13fmt, self.db, u13offset)
                    if u13size == 2:
                        print ("\t{:04x}".format(value[0]))
                    else:
                        print ("\t{:04x} {:04x} {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
                    u13offset += increment1

            # check that we read to the end of the file
            if num == 11:
                if u13offset != len(self.db):
                    log.warning("Unexpected end of u13 table 11")

            current += increment
            num += 1

        self.parse_u13_t0()
        self.parse_u13_t1()
        self.parse_u13_t2()
        self.parse_u13_t3()
        self.parse_u13_t4()
        self.parse_u13_t5()
        self.parse_u13_t6()
        self.parse_u13_t7()
        self.parse_u13_t8()
        self.parse_u13_t9()
        self.parse_u13_t10()
        self.parse_u13_t11()
        self.parse_u13_t12()

    def parse_u13_t0(self):
        print("foo0 - genre performer counts")

        if self.u13s[0].count != self.details[genre_count][0] - 1:
            log.warning("Unexpected u13 count 0")

        current = self.u13s[0].offset
        increment = struct.calcsize("<HHHH")
        total_performers = 0
        for index in range(self.u13s[0].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            print ("\tgenre number: {:04x}, performer total: {:04x}, number of performers: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total_performers:
                log.warning("Unexpected u13t0 value 1")
            if value[2] != self.genres[value[0]].performer_count:
                log.warning("Unexpected u13t0 value 2")
            if value[3] != 0x00:
                log.warning("Unexpected u13t0 value 3")
            total_performers += value[2]
            current += increment

    def parse_u13_t1(self):
        print("foo1 - genre performer album counts")
        # running total in value[1]
        current = self.u13s[1].offset
        increment = struct.calcsize("<HHHH")
        total = 0
        for index in range(self.u13s[1].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            print ("\tperformer: {:04x}, total: {:04x}, num albums: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning("Unexpected u13t1 value 1")
            if value[3] != 0x00:
                log.warning("Unexpected u13t1 value 3")
            total += value[2]
            current += increment

    def parse_u13_t2(self):
        print("foo2 - unknown")
        # running total in value[1]
        current = self.u13s[2].offset
        increment = struct.calcsize("<HHHH")
        total = self.genres[0].title_count
        for index in range(self.u13s[2].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            print ("\t?: {:04x}, total: {:04x}, ?: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning("Unexpected u13t2 value 1")
            if value[3] != 0x00:
                log.warning("Unexpected u13t2 value 3")
            total += value[2]
            current += increment

    def parse_u13_t3(self):
        print("foo3 - unknown u5")
        if self.u13s[3].offset != self.details[u5][0]:
            log.warning("Unexpected u13 offset 3")
        if self.u13s[3].count != self.details[title_count][0]:
            log.warning("Unexpected u13 count 3")

    def parse_u13_t4(self):
        print("foo4 - genre album counts")

        if self.u13s[4].count != self.details[genre_count][0] - 1:
            log.warning("Unexpected u13 count 4")

        current = self.u13s[4].offset
        increment = struct.calcsize("<HHHH")
        total_albums = 0
        for index in range(self.u13s[4].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            print ("\tgenre number: {:04x}, album total: {:04x}, number of albums: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total_albums:
                log.warning("Unexpected u13t4 value 1")
            if value[2] != self.genres[value[0]].album_count:
                log.warning("Unexpected u13t4 value 2, expected {} got {}".format(self.genres[value[0]].album_count, value[2]))
            if value[3] != 0x00:
                log.warning("Unexpected u13t4 value 3")
            total_albums += value[2]
            current += increment

    def parse_u13_t5(self):
        print("foo5 - genre album title counts")

        if self.u13s[5].count != self.details[album_count][0] - 1:
            log.warning("Unexpected u13 count 5")

        # running total in value[1]
        current = self.u13s[5].offset
        increment = struct.calcsize("<HHHH")
        total = self.genres[0].title_count
        for index in range(self.u13s[5].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            print ("\talbum number: {:04x}, title total: {:04x}, number of titles: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning("Unexpected u13t5 value 1")
            if value[3] != 0x00:
                log.warning("Unexpected u13t5 value 3")
            total += value[2]
            current += increment

    def parse_u13_t6(self):
        print("foo6 - genre titles")
        if self.u13s[6].offset != self.details[genre_title_offset][0]:
            log.warning("Unexpected u13 offset 6")
        if self.u13s[6].count != self.details[title_count][0]:
            log.warning("Unexpected u13 count 6")


    def parse_u13_t7(self):
        print("foo7 - performer album counts")

        if self.u13s[7].count != self.details[performer_count][0] - 1:
            log.warning("Unexpected u13 count 7")

        current = self.u13s[7].offset
        increment = struct.calcsize("<HHHH")
        total_albums = 0
        for index in range(self.u13s[7].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            print ("\tperformer number: {:04x}, album total: {:04x}, number of albums: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total_albums:
                log.warning("Unexpected u13t7 value 1")
            if value[2] != self.performers[value[0]].album_count:
                log.warning("Unexpected u13t7 value 2, expected {} got {}".format(self.performers[value[0]].album_count, value[2]))
            if value[3] != 0x00:
                log.warning("Unexpected u13t7 value 3")
            total_albums += value[2]
            current += increment

    def parse_u13_t8(self):
        print("foo8 - unknown")

    def parse_u13_t9(self):
        print("foo9 - performer titles")
        if self.u13s[9].offset != self.details[performer_title_offset][0]:
            log.warning("Unexpected u13 offset 9") 
        if self.u13s[9].count != self.details[title_count][0]:
            log.warning("Unexpected u13 count 9")

    def parse_u13_t10(self):
        print("foo10 - genre performer counts")
        if self.u13s[10].count != self.details[genre_count][0] - 1:
            log.warning("Unexpected u13 count 10")
        current = self.u13s[10].offset
        increment = struct.calcsize("<HHHH")
        total_performers = 0
        for index in range(self.u13s[10].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            print ("\tgenre number: {:04x}, performer total: {:04x}, number of performers: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total_performers:
                log.warning("Unexpected u13t10 value 1")
            if value[2] != self.genres[value[0]].performer_count:
                log.warning("Unexpected u13t10 value 2")
            if value[3] != 0x00:
                log.warning("Unexpected u13t10 value 3")
            total_performers += value[2]
            current += increment

    def parse_u13_t11(self):
        print("foo11 - unknown")
        # running total in value[1]
        current = self.u13s[11].offset
        increment = struct.calcsize("<HHHH")
        total = self.genres[0].title_count
        for index in range(self.u13s[11].count):
            value = struct.unpack_from("<HHHH", self.db, current)
            print ("\t?: {:04x}, total: {:04x}, ?: {:04x} {:04x}".format(value[0], value[1], value[2], value[3]))
            if value[1] != total:
                log.warning("Unexpected u13t11 value 1")
            if value[3] != 0x00:
                log.warning("Unexpected u13t11 value 3")
            total += value[2]
            current += increment

    def parse_u13_t12(self):
        print("foo12 - u5")
        if self.u13s[12].offset != self.details[u5][0]:
            log.warning("Unexpected u13 offset 12") 
        if self.u13s[12].count != self.details[title_count][0]:
            log.warning("Unexpected u13 count 12")

    def show_titles(self):
        print ("Titles:")
        for index in range(self.details[title_count][0]):
            print("\tTitle- 0x{:04x}: {}; genre {:04x}; performer {:04x}; album {:04x}".format(index, self.entries[index].title, self.entries[index].genre, self.entries[index].performer, self.entries[index].album))

    def show_genres(self):
        print ("Genres:")
        for index in range(self.details[genre_count][0]):
            print("\tGenre- 0x{:04x}: '{}'".format(index, self.genres[index].name))
            print("\tgen:titles_offset {:04x} dir_count {:04x}".format(self.genres[index].titles_offset, self.genres[index].dir_count))
            print("\tgen:performer_count {:04x}".format(self.genres[index].performer_count))
            print("\tgen:album_count {:04x}".format(self.genres[index].album_count))
            for title_index in range(self.genres[index].titles_count):
                print("\t\t0x{:04x}: {}".format(index, self.entries[self.genres[index].titles[title_index]].title))

    def show_performers(self):
        print ("Performers:")
        for index in range(self.details[performer_count][0]):
            print("\tPerformer- 0x{:04x}: {}".format(index, self.performers[index].name))
            print("\tper:titles_offset {:04x} dir_count {:04x}".format(self.performers[index].titles_offset, self.performers[index].dir_count))
            print("\tper:genre_count {:04x}".format(self.performers[index].genre_count))
            print("\tper:album_count {:04x}".format(self.performers[index].album_count))
            for title_index in range(self.performers[index].titles_count):
                print("\t\t0x{:04x}: {}".format(index, self.entries[self.performers[index].titles[title_index]].title))

    def show_albums(self):
        print ("Albums:")
        for index in range(self.details[album_count][0]):
            print("\tAlbum- 0x{:04x}: {}".format(index, self.albums[index].name))
            for title_index in range(self.albums[index].titles_count):
                print("\t\t0x{:04x}: {}".format(index, self.entries[self.albums[index].titles[title_index]].title))

    def show_playlists(self):
        print ("Playlists:")
        for index in range(self.details[playlist_count][0]):
            print("\tPlaylist- 0x{:04x}: {}".format(index, self.playlists[index].name))
            for title_index in range(self.playlists[index].titles_count):
                print("\t\t0x{:04x}: {}".format(index, self.entries[self.playlists[index].titles[title_index]].title))

    def __str__(self):
        contents = ""
        for index in range(title_count, end):
            contents += "{}: 0x{:08x}\n".format(file_offsets[index][2], self.details[index][0])
        return contents

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Read a kenwood database")
    parser.add_argument("-i", "--input", dest="inputfile", action="store", default="kenwood.dap", help="specify input file")

    args = parser.parse_args()

    print (args.inputfile)

    db = DBfile(args.inputfile)
    db.show_titles()
    db.show_genres()
    db.show_performers()
    db.show_albums()
    db.show_playlists()
    print (db)
