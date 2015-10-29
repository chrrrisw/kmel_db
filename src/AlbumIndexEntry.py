import struct
from constants import STRING_ENCODING


class AlbumIndexEntry(object):

    FORMAT = "<HHIHHHH"
    SIZE = struct.calcsize(FORMAT)
    NAME_CHAR_LENGTH = 2

    def __init__(self, name, titles, number):
        self._number = number
        self._name = name + '\x00'
        self._name_length = len(self.encodedName)

        self._num_titles = len(titles)
        self._titles = titles
        self._title_numbers = []

        # Set the album number on each of the titles
        for title in self._titles:
            title.set_album_number(self._number)
            self._title_numbers.append(title.get_index())

        # To be set later
        self._name_offset = 0
        self._title_entry_offset = 0

#         print('''
# AlbumIndexEntry
#     Name:{}: Length:{}: Num_Titles:{}:
# '''.format(self._name, self._name_length, self._num_titles))

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

    @property
    def number_of_titles(self):
        return self._num_titles

    @property
    def title_numbers(self):
        return self._title_numbers

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
