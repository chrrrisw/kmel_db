#!/usr/bin/env /usr/bin/python3

import struct

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
    end
) = list(range(21))

file_offsets = {
    signature:            (0x00, "<4s", "signature"),
    u1:                   (0x04, "<HH", "u1"),
    title_count:          (0x08, "<H", "title_count"),
    title_entry_size:     (0x0a, "<H", "title_entry_size"),
    genre_count:          (0x0c, "<H", "genre_count"),
    genre_entry_size:     (0x0e, "<H", "genre_entry_size"),
    performer_count:      (0x10, "<H", "performer_count"),
    performer_entry_size: (0x12, "<H", "performer_entry_size"),
    album_count:          (0x14, "<H", "album_count"),
    album_entry_size:     (0x16, "<H", "album_entry_size"),
    playlist_count:       (0x18, "<H", "playlist_count"),
    playlist_entry_size:  (0x1a, "<H", "playlist_entry_size"),
    u2:                   (0x1c, "<H", "u2"),
    u3:                   (0x1e, "<H", "u3"),
    main_index_offset:         (0x40, "<I", "main_index_offset"),
    title_offset:         (0x44, "<I", "title_offset"),
    shortdir_offset:      (0x48, "<I", "shortdir_offset"),
    shortfile_offset:     (0x4c, "<I", "shortfile_offset"),
    longdir_offset:       (0x50, "<I", "longdir_offset"),
    longfile_offset:      (0x54, "<I", "longfile_offset")
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
            print ("Unexpected value")

        self.u2 = values[4]
        if self.u2 != 0xffffffff:
            print ("Unexpected value")

        self.u3 = values[5]
        if self.u3 != 0x80000000:
            print ("Unexpected value")

        self.u4 = values[6]
        if self.u4 != 0x80000000:
            print ("Unexpected value")

        self.title_length = values[7]
        self.title_char = values[8]
        self.title_offset = values[9]
        if self.title_char != 0x02:
            print ("Unexpected value")

        self.shortdir_length = values[10]
        self.shortdir_char = values[11]
        self.shortdir_offset = values[12]
        if self.shortdir_char != 0x01:
            print ("Unexpected value")

        self.shortfile_length = values[13]
        self.shortfile_char = values[14]
        self.shortfile_offset = values[15]
        if self.shortfile_char != 0x01:
            print ("Unexpected value")

        self.longdir_length = values[16]
        self.longdir_char = values[17]
        self.longdir_offset = values[18]
        if self.longdir_char != 0x02:
            print ("Unexpected value")

        self.longfile_length = values[19]
        self.longfile_char = values[20]
        self.longfile_offset = values[21]
        if self.longfile_char != 0x02:
            print ("Unexpected value")

        self.u5 = values[22]
        if self.u5 != 0x00000000:
            print ("Unexpected value")

class DBfile(object):
    def __init__(self, filename):
        f = open(filename, 'rb')
        self.db = f.read()
        f.close()

        self.details = []
        for index in range(end):
            self.details.append(struct.unpack_from(file_offsets[index][1], self.db, file_offsets[index][0]))

        self.parse_index()

    def parse_index(self):
        self.entries = []
        if self.details[title_entry_size][0] != struct.calcsize(INDEX_FORMAT):
            print ("Unexpected index size")
        current = self.details[main_index_offset][0]
        for index in range(self.details[title_count][0]):
            value = struct.unpack_from(INDEX_FORMAT, self.db, current)
            self.entries.append(MainIndexEntry(value))
            current += self.details[title_entry_size][0]

    def show_titles(self):
        for index in range(self.details[title_count][0]):
            pass

    def __str__(self):
        contents = ""
        for index in range(end):
            contents += "{}: {}\n".format(file_offsets[index][2], self.details[index])
        return contents

if __name__ == "__main__":
    db = DBfile("kenwood.dap")
    print (db)
