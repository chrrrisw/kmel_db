#!/usr/bin/env /usr/bin/python3

import logging
import struct

log = logging.getLogger(__name__)
FORMAT = '%(message)s'
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

class GenreIndexEntry(object):
    def __init__(self, values):
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

    def set_name(self, name):
        self.name = name
        log.debug ("Genre name: {}".format(self.name))

    def set_titles(self, titles):
        self.titles = titles
        log.debug ("\tGenre titles: {}".format(self.titles))

    def __str__(self):
        contents = "Genre: {}, titles: {}".format(self.name, str(self.titles))
        return contents

class PerformerIndexEntry(object):
    def __init__(self, values):
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

    def set_name(self, name):
        self.name = name
        log.debug ("Performer name: {}".format(self.name))

    def set_titles(self, titles):
        self.titles = titles
        log.debug ("\tPerformer titles: {}".format(self.titles))

class AlbumIndexEntry(object):
    def __init__(self, values):
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

    def set_name(self, name):
        self.name = name
        log.debug ("Album name: {}".format(self.name))

    def set_titles(self, titles):
        self.titles = titles
        log.debug ("\tAlbum titles: {}".format(self.titles))

class PlaylistIndexEntry(object):
    def __init__(self, values):
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

    def set_name(self, name):
        self.name = name
        log.debug ("Playlist name: {}".format(self.name))

    def set_titles(self, titles):
        self.titles = titles
        log.debug ("\tPlaylist titles: {}".format(self.titles))

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
        pass

    def parse_u3(self):
        pass

    def parse_main_index(self):
        self.entries = []
        if self.details[title_entry_size][0] != struct.calcsize(INDEX_FORMAT):
            log.warning ("Unexpected index size")
        current = self.details[main_index_offset][0]
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from(INDEX_FORMAT, self.db, current)
            main_index_entry = MainIndexEntry(value)

            title = self.db[
                self.details[title_offset][0] + main_index_entry.title_offset:
                self.details[title_offset][0] + main_index_entry.title_offset + main_index_entry.title_length].decode('utf-16')
            main_index_entry.set_title(title)

            shortdir = self.db[
                self.details[shortdir_offset][0] + main_index_entry.shortdir_offset:
                self.details[shortdir_offset][0] + main_index_entry.shortdir_offset + main_index_entry.shortdir_length].decode('ascii')
            main_index_entry.set_shortdir(shortdir)

            shortfile = self.db[
                self.details[shortfile_offset][0] + main_index_entry.shortfile_offset:
                self.details[shortfile_offset][0] + main_index_entry.shortfile_offset + main_index_entry.shortfile_length].decode('ascii')
            main_index_entry.set_shortfile(shortfile)

            longdir = self.db[
                self.details[longdir_offset][0] + main_index_entry.longdir_offset:
                self.details[longdir_offset][0] + main_index_entry.longdir_offset + main_index_entry.longdir_length].decode('utf-16')
            main_index_entry.set_longdir(longdir)

            longfile = self.db[
                self.details[longfile_offset][0] + main_index_entry.longfile_offset:
                self.details[longfile_offset][0] + main_index_entry.longfile_offset + main_index_entry.longfile_length].decode('utf-16')
            main_index_entry.set_longfile(longfile)

            self.entries.append(main_index_entry)
            current += self.details[title_entry_size][0]

    def parse_u4(self):
        print ("u4 offset: {:08x}".format(self.details[u4][0]))
        current = self.details[u4][0]
        increment = struct.calcsize("<H")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            print ("\t{}".format(self.entries[value[0]].title))
            current += increment
        if current != self.details[genre_index_offset][0]:
            log.warning("Unexpected u4 end offset")

    def parse_genres(self):
        self.genres = []
        if self.details[genre_entry_size][0] != struct.calcsize(GENRE_INDEX_FORMAT):
            log.warning ("Unexpected genre index size")
        current = self.details[genre_index_offset][0]
        for index in range(self.details[genre_count][0]):
            value = struct.unpack_from(GENRE_INDEX_FORMAT, self.db, current)
            genre_index_entry = GenreIndexEntry(value)

            name = self.db[
                self.details[genre_name_offset][0] + genre_index_entry.name_offset:
                self.details[genre_name_offset][0] + genre_index_entry.name_offset + genre_index_entry.name_length].decode('utf-16')
            genre_index_entry.set_name(name)

            titles = []
            titles_current = self.details[genre_title_offset][0] + genre_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(genre_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            genre_index_entry.set_titles(titles)

            self.genres.append(genre_index_entry)
            current += self.details[genre_entry_size][0]

    def parse_u5(self):
        print ("u5 offset: {:08x}".format(self.details[u5][0]))
        current = self.details[u5][0]
        increment = struct.calcsize("<H")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            print ("\t{}".format(self.entries[value[0]].title))
            current += increment
        if current != self.details[performer_index_offset][0]:
            log.warning("Unexpected u5 end offset")

    def parse_performers(self):
        self.performers = []
        if self.details[performer_entry_size][0] != struct.calcsize(PERFORMER_INDEX_FORMAT):
            log.warning ("Unexpected performer index size")
        current = self.details[performer_index_offset][0]
        for index in range(self.details[performer_count][0]):
            value = struct.unpack_from(PERFORMER_INDEX_FORMAT, self.db, current)
            performer_index_entry = PerformerIndexEntry(value)

            name = self.db[
                self.details[performer_name_offset][0] + performer_index_entry.name_offset:
                self.details[performer_name_offset][0] + performer_index_entry.name_offset + performer_index_entry.name_length].decode('utf-16')
            performer_index_entry.set_name(name)

            titles = []
            titles_current = self.details[performer_title_offset][0] + performer_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(performer_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            performer_index_entry.set_titles(titles)

            self.performers.append(performer_index_entry)
            current += self.details[performer_entry_size][0]

    def parse_u6(self):
        print ("u6 offset: {:08x}".format(self.details[u6][0]))
        current = self.details[u6][0]
        increment = struct.calcsize("<H")
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from("<H", self.db, current)
            print ("\t{}".format(self.entries[value[0]].title))
            current += increment
        if current != self.details[album_index_offset][0]:
            log.warning("Unexpected u6 end offset")

    def parse_albums(self):
        self.albums = []
        if self.details[album_entry_size][0] != struct.calcsize(ALBUM_INDEX_FORMAT):
            log.warning ("Unexpected album index size")
        current = self.details[album_index_offset][0]
        for index in range(self.details[album_count][0]):
            value = struct.unpack_from(ALBUM_INDEX_FORMAT, self.db, current)
            album_index_entry = AlbumIndexEntry(value)

            name = self.db[
                self.details[album_name_offset][0] + album_index_entry.name_offset:
                self.details[album_name_offset][0] + album_index_entry.name_offset + album_index_entry.name_length].decode('utf-16')
            album_index_entry.set_name(name)

            titles = []
            titles_current = self.details[album_title_offset][0] + album_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(album_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            album_index_entry.set_titles(titles)

            self.albums.append(album_index_entry)
            current += self.details[album_entry_size][0]

    def parse_u7(self):
        pass

    def parse_u8(self):
        pass

    def parse_playlists(self):
        self.playlists = []
        if self.details[playlist_entry_size][0] != struct.calcsize(PLAYLIST_INDEX_FORMAT):
            log.warning ("Unexpected playlist index size")
        current = self.details[playlist_index_offset][0]
        for index in range(self.details[playlist_count][0]):
            value = struct.unpack_from(PLAYLIST_INDEX_FORMAT, self.db, current)
            playlist_index_entry = PlaylistIndexEntry(value)

            name = self.db[
                self.details[playlist_name_offset][0] + playlist_index_entry.name_offset:
                self.details[playlist_name_offset][0] + playlist_index_entry.name_offset + playlist_index_entry.name_length].decode('utf-16')
            playlist_index_entry.set_name(name)

            titles = []
            titles_current = self.details[playlist_title_offset][0] + playlist_index_entry.titles_offset
            titles_increment = struct.calcsize("<H")
            for titles_index in range(playlist_index_entry.titles_count):
                titles.append(struct.unpack_from("<H", self.db, titles_current)[0])
                titles_current += titles_increment
            playlist_index_entry.set_titles(titles)

            self.playlists.append(playlist_index_entry)
            current += self.details[playlist_entry_size][0]

    def parse_u9(self):
        pass

    def parse_u10(self):
        pass

    def parse_u11(self):
        pass

    def parse_u12(self):
        pass

    def parse_u13(self):
        pass

    def show_titles(self):
        print ("Titles:")
        for index in range(self.details[title_count][0]):
            print("\t0x{:04x}: {}".format(index, self.entries[index].title))

    def show_genres(self):
        print ("Genres:")
        for index in range(self.details[genre_count][0]):
            print("\t0x{:04x}: {}".format(index, self.genres[index].name))
            for title_index in range(self.genres[index].titles_count):
                print("\t\t0x{:04x}: {}".format(index, self.entries[self.genres[index].titles[title_index]].title))

    def show_performers(self):
        print ("Performers:")
        for index in range(self.details[performer_count][0]):
            print("\t0x{:04x}: {}".format(index, self.performers[index].name))
            for title_index in range(self.performers[index].titles_count):
                print("\t\t0x{:04x}: {}".format(index, self.entries[self.performers[index].titles[title_index]].title))

    def show_albums(self):
        print ("Albums:")
        for index in range(self.details[album_count][0]):
            print("\t0x{:04x}: {}".format(index, self.albums[index].name))
            for title_index in range(self.albums[index].titles_count):
                print("\t\t0x{:04x}: {}".format(index, self.entries[self.albums[index].titles[title_index]].title))

    def show_playlists(self):
        print ("Playlists:")
        for index in range(self.details[playlist_count][0]):
            print("\t0x{:04x}: {}".format(index, self.playlists[index].name))
            for title_index in range(self.playlists[index].titles_count):
                print("\t\t0x{:04x}: {}".format(index, self.entries[self.playlists[index].titles[title_index]].title))

    def __str__(self):
        contents = ""
        for index in range(end):
            contents += "{}: {}\n".format(file_offsets[index][2], self.details[index])
        return contents

if __name__ == "__main__":
    
    db = DBfile("kenwood.dap")
    db.show_titles()
    db.show_genres()
    db.show_performers()
    db.show_albums()
    db.show_playlists()
