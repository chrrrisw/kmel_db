import logging
import struct
from .constants import STRING_ENCODING

log = logging.getLogger(__name__)


class MainIndexEntry(object):
    '''A class to read and write main index entries.'''

    FORMAT = "<HHH HIII HHI HHI HHI HHI HHI I"
    SIZE = struct.calcsize(FORMAT)
    TITLE_CHAR_LENGTH = 2
    SHORTDIR_CHAR_LENGTH = 1
    SHORTFILE_CHAR_LENGTH = 1
    LONGDIR_CHAR_LENGTH = 2
    LONGFILE_CHAR_LENGTH = 2

    def __init__(self):
        self._mediaFile = None

    def set_media_file(self, mediafile):
        '''Initialise the entry from a media file.'''
        self._mediaFile = mediafile

        self.title_length = len(self.encodedTitle)
        # To be set later
        self.title_offset = 0

        self.shortdir_length = len(self.encodedShortdir)
        # To be set later
        self.shortdir_offset = 0

        self.shortfile_length = len(self.encodedShortfile)
        # To be set later
        self.shortfile_offset = 0

        self.longdir_length = len(self.encodedLongdir)
        # To be set later
        self.longdir_offset = 0

        self.longfile_length = len(self.encodedLongfile)
        # To be set later
        self.longfile_offset = 0

    @property
    def mediaFile(self):
        '''Get the corresponding media file.'''
        return self._mediaFile

    def get_index(self):
        '''Get the index from the media file.'''
        return self._mediaFile.index

    @property
    def encodedTitle(self):
        '''Get the title from the media file and encode it for writing.'''
        return self._mediaFile.title.encode(STRING_ENCODING)

    @property
    def title(self):
        '''Get the title from the media file.'''
        return self._mediaFile.title

    @property
    def encodedShortdir(self):
        '''
        Get the 8.3 directory name for the media file and encode it
        for writing.
        '''
        return self._mediaFile.shortdir.encode("ascii")

    @property
    def shortdir(self):
        '''Get the 8.3 directory name for the media file.'''
        return self._mediaFile.shortdir

    @property
    def encodedShortfile(self):
        ''''''
        # The 8.3 filename for the media file
        return self._mediaFile.shortfile.encode("ascii")

    @property
    def shortfile(self):
        ''''''
        return self._mediaFile.shortfile

    @property
    def encodedLongdir(self):
        ''''''
        # The long directory name for the media file
        return self._mediaFile.longdir.encode(STRING_ENCODING)

    @property
    def longdir(self):
        ''''''
        return self._mediaFile.longdir

    @property
    def encodedLongfile(self):
        ''''''
        # The long filename for the media file
        return self._mediaFile.longfile.encode(STRING_ENCODING)

    @property
    def longfile(self):
        ''''''
        return self._mediaFile.longfile

    @property
    def genre_number(self):
        ''''''
        return self._mediaFile.genre_number

    @property
    def performer_number(self):
        ''''''
        return self._mediaFile.performer_number

    @property
    def album_number(self):
        ''''''
        return self._mediaFile.album_number

    # Offsets to be set once known

    def set_title_offset(self, title_offset):
        ''''''
        self.title_offset = title_offset

    def set_shortdir_offset(self, shortdir_offset):
        ''''''
        self.shortdir_offset = shortdir_offset

    def set_shortfile_offset(self, shortfile_offset):
        ''''''
        self.shortfile_offset = shortfile_offset

    def set_longdir_offset(self, longdir_offset):
        ''''''
        self.longdir_offset = longdir_offset

    def set_longfile_offset(self, longfile_offset):
        ''''''
        self.longfile_offset = longfile_offset

    def get_representation(self):
        '''Return the on-disk representation for this entry.'''
        return struct.pack(
            self.FORMAT,
            self._mediaFile.genre_number,
            self._mediaFile.performer_number,
            self._mediaFile.album_number,
            0x0000,
            0xffffffff,
            0x80000000,
            0x80000000,
            self.title_length,
            self.TITLE_CHAR_LENGTH,
            self.title_offset,
            self.shortdir_length,
            self.SHORTDIR_CHAR_LENGTH,
            self.shortdir_offset,
            self.shortfile_length,
            self.SHORTFILE_CHAR_LENGTH,
            self.shortfile_offset,
            self.longdir_length,
            self.LONGDIR_CHAR_LENGTH,
            self.longdir_offset,
            self.longfile_length,
            self.LONGFILE_CHAR_LENGTH,
            self.longfile_offset,
            0x00000000)

    def read_from_buffer(self, bfr, offset):
        '''Read an entry from a buffer.'''

        (
            genre_number,  # 0
            performer_number,  # 1
            album_number,  # 2
            self.u1,  # 3
            self.u2,  # 4
            self.u3,  # 5
            self.u4,  # 6
            self.title_length,  # 7
            title_char_length,  # 8
            self.title_offset,  # 9
            self.shortdir_length,  # 10
            shortdir_char_length,  # 11
            self.shortdir_offset,  # 12
            self.shortfile_length,  # 13
            shortfile_char_length,  # 14
            self.shortfile_offset,  # 15
            self.longdir_length,  # 16
            longdir_char_length,  # 17
            self.longdir_offset,  # 18
            self.longfile_length,  # 19
            longfile_char_length,  # 20
            self.longfile_offset,  # 21
            self.u5) = struct.unpack_from(self.FORMAT, bfr, offset)

        if self.u1 != 0x0000:
            log.warning("Unexpected main index u1 value")

        if self.u2 != 0xffffffff:
            log.warning("Unexpected main index u2 value")

        if self.u3 != 0x80000000:
            log.warning("Unexpected main index u3 value")

        if self.u4 != 0x80000000:
            log.warning("Unexpected main index u4 value")

        if title_char_length != self.TITLE_CHAR_LENGTH:
            log.warning("Unexpected title char length value")

        # log.debug("Title length:{} offset:{}".format(
        #     self.title_length, self.title_offset))

        if shortdir_char_length != self.SHORTDIR_CHAR_LENGTH:
            log.warning("Unexpected shortdir char length value")

        if shortfile_char_length != self.SHORTFILE_CHAR_LENGTH:
            log.warning("Unexpected shortfile char length value")

        if longdir_char_length != self.LONGDIR_CHAR_LENGTH:
            log.warning("Unexpected longdir char length value")

        if longfile_char_length != self.LONGFILE_CHAR_LENGTH:
            log.warning("Unexpected longfile char length value")

        if self.u5 != 0x00000000:
            log.warning("Unexpected main index u5 value")

        if self._mediaFile is None:
            pass
        else:
            self._mediaFile.genre_number = genre_number
            self._mediaFile.performer_number = performer_number
            self._mediaFile.album_number = album_number

    # STUFF FROM READER
    # def set_genre(self, genre):
    #     self.genre = genre
    #     log.debug(self.genre)

    # def set_performer(self, performer):
    #     self.performer = performer
    #     log.debug(self.performer)

    # def set_album(self, album):
    #     self.album = album
    #     log.debug(self.album)

    # def set_title(self, title):
    #     self.title = title
    #     log.debug("Title:{}".format(self.title))

    # def set_shortdir(self, shortdir):
    #     self.shortdir = shortdir
    #     log.debug("\tShortdir:{}".format(self.shortdir))

    # def set_shortfile(self, shortfile):
    #     self.shortfile = shortfile
    #     log.debug("\tShortfile:{}".format(self.shortfile))

    # def set_longdir(self, longdir):
    #     self.longdir = longdir
    #     log.debug("\tLongdir:{}".format(self.longdir))

    # def set_longfile(self, longfile):
    #     self.longfile = longfile
    #     log.debug("\tLongfile:{}".format(self.longfile))

    # def __str__(self):
    #     return "Title- '{}'; genre {:04x}; performer {:04x}; album {:04x}".format(
    #         self.title, self.genre, self.performer, self.album)
