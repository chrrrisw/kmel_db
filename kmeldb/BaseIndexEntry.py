import struct
from .constants import STRING_ENCODING

import logging
log = logging.getLogger(__name__)


class BaseIndexEntry(object):
    '''
    BaseIndexEntry is the super class for AlbumIndexEntry, GenreIndexEntry,
    PerformerIndexEntry and PlaylistIndexEntry.

    It defines attributes to hold a name, a list of media files, and an
    index number.
    '''

    FORMAT = "<HHIHHHH"
    SIZE = struct.calcsize(FORMAT)
    NAME_CHAR_LENGTH = 2
    __isfrozen = False

    def __init__(self, name, titles, number):
        '''Initialise the class.

        Args:
            name (str): The name for this instance.
            titles (List[MediaFile]): The media files associated with this
                instance.
            number (int): The index number for this instance.
        '''
        self._number = number
        self._name = name + '\x00'
        self._name_length = len(self.encodedName)

        self._num_titles = len(titles)
        self._titles = titles

        # To be set later
        self._name_offset = 0
        self._title_entry_offset = 0

    def __setattr__(self, key, value):
        '''Only allow new attributes if not frozen.'''
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("%r is a frozen class" % self)
        object.__setattr__(self, key, value)

    def _freeze(self):
        '''Freeze the class such that new attributes cannot be added.'''
        self.__isfrozen = True

    def __str__(self):
        return '{}: {} {}'.format(
            self.__class__.__name__,
            self._number,
            self._name)

    # Offsets to be set when known

    @property
    def name_offset(self):
        '''int: the offset to the name'''
        return self._name_offset

    @name_offset.setter
    def name_offset(self, name_offset):
        self._name_offset = name_offset

    @property
    def title_entry_offset(self):
        '''short int: the offset to the title entry'''
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

    def get_representation(self):
        '''Return the data encoded ready for writing to file.'''
        return struct.pack(
            self.FORMAT,
            self._name_length,
            self.NAME_CHAR_LENGTH,
            self._name_offset,
            0x0000,
            self._num_titles,
            self._title_entry_offset,
            0x0000)






class OldBaseIndexEntry(object):
    identifier = "Base"

    def __init__(self, values):
        pass

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
        log.debug("{} name: '{}'".format(self.__class__.identifier, self.name))

    def set_titles(self, titles, entries):
        self.titles = titles
        self.set_title_count(len(self.titles))

        log.debug("\t{} titles: {}".format(
            self.__class__.identifier, self.titles))

        # Count things

        self.counts = []
        dirlist = []
        genlist = []
        self.performer_albums = {}
        self.performer_titles = {}
        self.album_titles = {}
        for title in self.titles:
            self.counts.append(
                (entries[title].genre,
                    entries[title].performer,
                    entries[title].album))

            if entries[title].longdir not in dirlist:
                dirlist.append(entries[title].longdir)
            if entries[title].genre not in genlist:
                genlist.append(entries[title].genre)

            if entries[title].performer not in self.performer_albums.keys():
                self.performer_albums[entries[title].performer] = [entries[title].album]
                self.performer_titles[entries[title].performer] = [title]
            else:
                if entries[title].album not in self.performer_albums[entries[title].performer]:
                    self.performer_albums[entries[title].performer].append(entries[title].album)
                if title not in self.performer_titles[entries[title].performer]:
                    self.performer_titles[entries[title].performer].append(title)

            if entries[title].album not in self.album_titles.keys():
                self.album_titles[entries[title].album] = [title]
            else:
                if title not in self.album_titles[entries[title].album]:
                    self.album_titles[entries[title].album].append(title)

        self.set_dir_count(len(dirlist))
        self.set_genre_count(len(genlist))
        self.set_performer_count(len(self.performer_albums))
        self.set_album_count(len(self.album_titles))

        log.debug("\t{} performer albums {}".format(
            self.__class__.identifier, self.performer_albums))
        log.debug("\t{} performer titles {}".format(
            self.__class__.identifier, self.performer_titles))
        log.debug("\t{} album titles {}".format(
            self.__class__.identifier, self.album_titles))

    def __str__(self):
        contents = "{}: '{}', titles: {}".format(
            self.__class__.identifier, self.name, str(self.titles))
        return contents
