import struct
from constants import STRING_ENCODING


class GenreIndexEntry(object):

    FORMAT = "<HHIHHHH"
    SIZE = struct.calcsize(FORMAT)
    NAME_CHAR_LENGTH = 2

    def __init__(self, name, titles, number):
        self._number = number
        self._name = name + '\x00'
        self._name_length = len(self.encodedName)

        self._num_titles = len(titles)
        self._titles = titles

        # Set the genre number on each of the titles
        for title in self._titles:
            title.set_genre_number(self._number)

        # To be set later
        self._name_offset = 0
        self._title_entry_offset = 0
        self._performers = []
        self._performers_initialised = False
        self._albums = []
        self._albums_initialised = False

        print('''
GenreIndexEntry
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

    # Initialise the performers list for this genre

    def init_performers(self):
        for title in self._titles:
            if title.get_performer_number() not in self._performers:
                self._performers.append(title.get_performer_number())
        self._performers_initialised = True

    def get_performers(self):
        if self._performers_initialised:
            return self._performers
        else:
            raise

    def get_number_of_performers(self):
        return len(self._performers)

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
