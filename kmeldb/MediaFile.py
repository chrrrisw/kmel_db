valid_media_files = ('mp3', 'wma')


class MediaFile(object):
    """
    An object to hold all the information about a given media file.
    """

    def __init__(
            self,
            index,
            fullname,
            shortdir,
            shortfile,
            longdir,
            longfile,
            title,
            performer,
            album,
            genre,
            tracknumber,
            discnumber):
        """Store the given information.

        Args:
            index (int): The unique identifier for this file
            fullname (str): The absolute path name to the file
            shortdir (str): The 8.3 directory in which the file resides
            shortfile (str): The 8.3 filename
            longdir (str): The directory in which the file resides
            longfile (str): The filename
            title (str): The title for the work
            performer (str): The performer of the work
            album (str): The album on which the work appears
            genre (str): The genre for the work
        """
        self._index = index
        self._fullname = fullname

        # Need to add terminating 00 here
        self._shortdir = shortdir + "\x00"
        self._shortfile = shortfile + "\x00"
        self._longdir = longdir + "\x00"
        self._longfile = longfile + "\x00"
        self._title = title + "\x00"

        # The terminating 00 is added by each of the corresponding classes
        self._performer = performer
        self._album = album
        self._genre = genre
        self._tracknumber = tracknumber
        self._discnumber = discnumber

        # These will be set later
        self._performer_number = 0
        self._album_number = 0
        self._genre_number = 0

    @property
    def index(self):
        '''An integer representing the unique identifier for this file.'''
        return self._index

    @index.setter
    def index(self, index):
        '''An integer representing the unique identifier for this file.'''
        self._index = index

    @property
    def fullname(self):
        '''A string representing the full path and file name for this file.'''
        return self._fullname

    @property
    def title(self):
        '''A string representing the title of the media file.'''
        return self._title

    @property
    def shortdir(self):
        '''A string representing the FAT 8.3 directory for the file.
        Contains leading and trailing path separators.
        '''
        return self._shortdir

    @property
    def shortfile(self):
        '''A string representing the FAT 8.3 file name.'''
        return self._shortfile

    @property
    def longdir(self):
        '''A string representing the directory path for this file.
        Contains leading and trailing path separators.
        '''
        return self._longdir

    @property
    def longfile(self):
        '''A string representing the FAT 8.3 file name.'''
        return self._longfile

    @property
    def performer(self):
        return self._performer

    @property
    def performer_number(self):
        return self._performer_number

    @performer_number.setter
    def performer_number(self, performer_number):
        self._performer_number = performer_number

    @property
    def album(self):
        return self._album

    @property
    def album_number(self):
        return self._album_number

    @album_number.setter
    def album_number(self, album_number):
        self._album_number = album_number

    @property
    def genre(self):
        return self._genre

    @property
    def genre_number(self):
        return self._genre_number

    @genre_number.setter
    def genre_number(self, genre_number):
        self._genre_number = genre_number

    @property
    def tracknumber(self):
        return self._tracknumber

    @property
    def discnumber(self):
        return self._discnumber

    def __repr__(self):
        return "\nMediaFile({},\n\t{},\n\t{},\n\t{},\n\t{},\n\t{},\n\t{},\n\t{},\n\t{})\n".format(
            self._index,
            self._shortdir,
            self._shortfile,
            self._longdir,
            self._longfile,
            self._title,
            self._performer,
            self._album,
            self._genre)

    def __str__(self):
        """
        Return a string formatted with the media file information.
        """
        return "\n\tLongDir: {}\n\tShortDir: {}\n\tLongFile: {}\n\tShortFile: {}\n\tTitle: {}\n\tPerfomer: {}\n\tAlbum: {}\n\tGenre: {}".format(
            self._longdir,
            self._shortdir,
            self._longfile,
            self._shortfile,
            self._title,
            self._performer,
            self._album,
            self._genre)
