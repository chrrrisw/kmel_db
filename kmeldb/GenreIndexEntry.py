from .BaseIndexEntry import BaseIndexEntry


class GenreIndexEntry(BaseIndexEntry):
    '''
    Genres have titles, performers and albums.
    '''

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
        self._album_numbers = []
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

    def init_performers(self, performers):
        for title in self._titles:
            if title.performer_number not in self._performer_numbers:
                self._performer_numbers.append(title.performer_number)
                self._performers.append(performers[title.performer_number])
        self._performers_initialised = True

    @property
    def performer_numbers(self):
        '''Return list of performer numbers, sorted numerically (therefore alphabetically).'''
        if self._performers_initialised:
            return sorted(self._performer_numbers)
        else:
            raise Exception("Performers not initialised.")

    @property
    def number_of_performers(self):
        if self._performers_initialised:
            return len(self._performer_numbers)
        else:
            raise Exception("Performers not initialised.")

    def init_albums(self, albums):
        for title in self._titles:
            if title.album_number not in self._album_numbers:
                self._album_numbers.append(title.album_number)
                self._albums.append(albums[title.album_number])
        self._albums_initialised = True

    @property
    def album_numbers(self):
        '''Return list of album numbers, sorted numerically (therefore alphabetically).'''
        if self._albums_initialised:
            return sorted(self._album_numbers)
        else:
            raise Exception("Albums not initialised.")

    @property
    def number_of_albums(self):
        if self._albums_initialised:
            return len(self._album_numbers)
        else:
            raise Exception("Albums not initialised.")

    def performer(self, performer_number):
        for p in self._performers:
            if p.number == performer_number:
                return p
        return None

    def number_of_albums_for_performer(self, performer_number):
        count = set()
        for title in self._titles:
            if title.performer_number == performer_number:
                count.add(title.album_number)
        return len(count)

    def number_of_titles_for_performer(self, performer_number):
        count = set()
        for title in self._titles:
            if title.performer_number == performer_number:
                count.add(title.index)
        return len(count)

    def number_of_titles_for_album(self, album_number):
        count = set()
        for title in self._titles:
            if title.album_number == album_number:
                count.add(title.index)
        return len(count)

    def number_of_titles_for_album_for_performer(
            self, performer_number, album_number):

        count = set()
        for title in self._titles:
            if ((title.performer_number == performer_number) and
                    (title.album_number == album_number)):
                count.add(title.index)
        return len(count)

    def read_from_buffer(self, buffer, offset):

        (
            self.name_length,
            self.name_char,
            self.name_offset,
            self.u1,
            self.titles_count,
            self.titles_offset,
            self.u2) = struct.unpack_from(self.FORMAT, buffer, offset)

        if self.name_char != 0x02:
            log.warning("Unexpected genre name character length")

        if self.u1 != 0x00:
            log.warning("Unexpected genre u1 value")

        if self.u2 != 0x00:
            log.warning("Unexpected genre u2 value")
