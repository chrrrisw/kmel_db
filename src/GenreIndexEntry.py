from BaseIndexEntry import BaseIndexEntry


class GenreIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(GenreIndexEntry, self).__init__(name, titles, number)

        # Set the genre number on each of the titles
        for title in self._titles:
            title.genre_number = self._number

        # To be set later
        self._performers = []
        self._performer_numbers = []
        self._performers_initialised = False
        self._albums = []
        self._albums_initialised = False

        self._freeze()

    def __str__(self):
        return '{}: {} {}, performers: {} {}, albums: {}, titles: {}'.format(
            self.__class__.__name__,
            self._number,
            self._name,
            self.number_of_performers, self._performer_numbers,
            self.number_of_albums,
            self.number_of_titles)

    # Initialise the performers list for this genre

    def init_performers(self):
        for title in self._titles:
            if title.performer_number not in self._performer_numbers:
                self._performer_numbers.append(title.performer_number)
                self._performers.append(title.performer)
        self._performers_initialised = True

    @property
    def performer_numbers(self):
        if self._performers_initialised:
            return self._performer_numbers
        else:
            raise Exception("Performers not initialised.")

    @property
    def number_of_performers(self):
        return len(self._performer_numbers)

    def init_albums(self):
        for title in self._titles:
            if title.album_number not in self._albums:
                self._albums.append(title.album_number)
        self._albums_initialised = True

    @property
    def albums(self):
        if self._albums_initialised:
            return self._albums
        else:
            raise Exception("Albums not initialised.")

    @property
    def number_of_albums(self):
        if self._albums_initialised:
            return len(self._albums)
        else:
            raise Exception("Albums not initialised.")

    def number_of_albums_for_performer(self, performer_number):
        count = set()
        for title in self._titles:
            if title.performer_number == performer_number:
                count.add(title.album_number)
        return len(count)
