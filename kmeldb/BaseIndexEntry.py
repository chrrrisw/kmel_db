''''''
import struct
import logging
from .constants import STRING_ENCODING

LOG = logging.getLogger(__name__)


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
        ''''''
        return self._name.encode(STRING_ENCODING)

    @property
    def number(self):
        ''''''
        return self._number

    @property
    def titles(self):
        ''''''
        return self._titles

    @property
    def number_of_titles(self):
        ''''''
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
