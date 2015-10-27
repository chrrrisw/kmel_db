import struct
from constants import STRING_ENCODING


class GenreIndexEntry(object):
    def __init__(self, name, titles, number):
        self.number = number
        self.name = name + '\x00'
        self.name_length = len(self.name.encode(STRING_ENCODING))
        self.name_char_length = 2

        self.num_titles = len(titles)
        self.titles = titles

        # Set the genre number on each of the titles
        for title in self.titles:
            title.set_genre_number(self.number)

        # To be set later
        self.name_offset = 0
        self.title_entry_offset = 0
        self.performers = []
        self.performers_initialised = False
        self.albums = []
        self.albums_initialised = False

        print('''
GenreIndexEntry
    Name:{}: Length:{}: Num_Titles:{}:
'''.format(self.name, self.name_length, self.num_titles))

    # Offsets to be set when known

    def set_name_offset(self, name_offset):
        self.name_offset = name_offset

    def set_title_entry_offset(self, title_entry_offset):
        self.title_entry_offset = title_entry_offset

    # Initialise the performers list for this genre

    def init_performers(self):
        for title in self.titles:
            if title.get_performer_number() not in self.performers:
                self.performers.append(title.get_performer_number())
        self.performers_initialised = True

    def get_performers(self):
        if self.performers_initialised:
            return self.performers
        else:
            raise

    def get_number_of_performers(self):
        return len(self.performers)

    def init_albums(self):
        for title in self.titles:
            if title.get_album_number() not in self.albums:
                self.albums.append(title.get_album_number())
        self.albums_initialised = True

    def get_albums(self):
        if self.albums_initialised:
            return self.albums
        else:
            raise

    def get_number_of_albums(self):
        return len(self.albums)

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
