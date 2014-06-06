class MediaFile(object):
    """
    An object to hold all the information about a given media file.
    """
    
    def __init__(self, index, shortdir, shortfile, longdir, longfile, title, performer, album, genre):
        """
        Store the given information.
        """
        self._index = index
        
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

        # These will be set later
        self._performer_number = 0
        self._album_number = 0
        self._genre_number = 0

    def get_index(self):
        return self._index

    def get_title(self):
        return self._title

    def get_shortdir(self):
        return self._shortdir

    def get_shortfile(self):
        return self._shortfile

    def get_longdir(self):
        return self._longdir

    def get_longfile(self):
        return self._longfile

    def get_performer(self):
        return self._performer

    def get_performer_number(self):
        return self._performer_number
    
    def set_performer_number(self, performer_number):
        self._performer_number = performer_number
    
    def get_album(self):
        return self._album

    def get_album_number(self):
        return self._album_number
    
    def set_album_number(self, album_number):
        self._album_number = album_number
    
    def get_genre(self):
        return self._genre

    def get_genre_number(self):
        return self._genre_number
    
    def set_genre_number(self, genre_number):
        self._genre_number = genre_number
    
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

