import struct
from constants import STRING_ENCODING


class AlbumIndexEntry(object):
    def __init__(self, name, titles, number):
        self.number = number
        self.name = name + '\x00'
        self.name_length = len(self.name.encode(STRING_ENCODING))
        self.name_char_length = 2

        self.num_titles = len(titles)
        self.titles = titles
        self.title_numbers = []

        # Set the album number on each of the titles
        for title in self.titles:
            title.set_album_number(self.number)
            self.title_numbers.append(title.get_index())

        # To be set later
        self.name_offset = 0
        self.title_entry_offset = 0

        print('''
AlbumIndexEntry
    Name:{}: Length:{}: Num_Titles:{}:
'''.format(self.name, self.name_length, self.num_titles))

    def set_name_offset(self, name_offset):
        self.name_offset = name_offset

    def set_title_entry_offset(self, title_entry_offset):
        self.title_entry_offset = title_entry_offset

    def get_number_of_titles(self):
        return self.num_titles

    def get_title_numbers(self):
        return self.title_numbers

    def get_representation(self):
        return struct.pack(
            "<HHIHHHH",
            self.name_length,
            self.name_char_length,
            self.name_offset,
            0x0000,
            self.num_titles,
            self.title_entry_offset,
            0x0000)

