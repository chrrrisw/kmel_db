from BaseIndexEntry import BaseIndexEntry


class GenreIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(GenreIndexEntry, self).__init__(name, titles, number)

        # Set the genre number on each of the titles
        for title in self._titles:
            title.set_genre_number(self._number)

        # To be set later
        self._performers = []
        self._performers_initialised = False
        self._albums = []
        self._albums_initialised = False

        self._freeze()

    # Initialise the performers list for this genre

    def init_performers(self):
        for title in self._titles:
            if title.get_performer_number() not in self._performers:
                self._performers.append(title.get_performer_number())
        self._performers_initialised = True

    @property
    def performers(self):
        if self._performers_initialised:
            return self._performers
        else:
            raise Exception("Performers not initialised.")

    @property
    def number_of_performers(self):
        return len(self._performers)

    def init_albums(self):
        for title in self._titles:
            if title.get_album_number() not in self._albums:
                self._albums.append(title.get_album_number())
        self._albums_initialised = True

    @property
    def albums(self):
        if self._albums_initialised:
            return self._albums
        else:
            raise Exception("Albums not initialised.")

    @property
    def number_of_albums(self):
        return len(self._albums)
