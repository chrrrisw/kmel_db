import struct
from constants import STRING_ENCODING


class PerformerIndexEntry(object):

    FORMAT = "<HHIHHHH"
    SIZE = struct.calcsize(FORMAT)
    NAME_CHAR_LENGTH = 2

    def __init__(self, name, titles, number):
        self._number = number
        self._name = name + '\x00'
        self._name_length = len(self._name.encode(STRING_ENCODING))

        self._num_titles = len(titles)
        self._titles = titles

        # Set the performer number on each of the titles
        for title in self._titles:
            title.set_performer_number(self._number)

        # To be set later
        self._name_offset = 0
        self._title_entry_offset = 0
        self._albums = []
        self._albums_initialised = False

        print('''
PerformerIndexEntry
    Name:{}: Length:{}: Num_Titles:{}:
'''.format(self._name, self._name_length, self._num_titles))

    # Offsets to be set when known

    @property
    def name_offset(self):
        return self._name_offset

    @name_offset.setter
    def name_offset(self, name_offset):
        self._name_offset = name_offset

    @property
    def title_entry_offset(self):
        return self._title_entry_offset

    @title_entry_offset.setter
    def title_entry_offset(self, title_entry_offset):
        self._title_entry_offset = title_entry_offset

    # Getters

    @property
    def encodedName(self):
        return self._name.encode(STRING_ENCODING)

    @property
    def number(self):
        return self._number

    @property
    def titles(self):
        return self._titles

    def init_albums(self):
        for title in self._titles:
            if title.get_album_number() not in self._albums:
                self._albums.append(title.get_album_number())
        self._albums_initialised = True

    def get_albums(self):
        if self._albums_initialised:
            return self._albums
        else:
            raise

    def get_number_of_albums(self):
        return len(self._albums)

    def get_number_of_titles(self):
        return self._num_titles

    def get_representation(self):
        return struct.pack(
            self.FORMAT,
            self._name_length,
            self.NAME_CHAR_LENGTH,
            self._name_offset,
            0x0000,
            self._num_titles,
            self._title_entry_offset,
            0x0000)


