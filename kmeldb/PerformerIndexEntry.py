from .BaseIndexEntry import BaseIndexEntry


class PerformerIndexEntry(BaseIndexEntry):
    '''A class to hold index data for performers.

    Performers have titles and albums.
    '''

    def __init__(self, name, titles, number):
        super(PerformerIndexEntry, self).__init__(name, titles, number)

        # Set the performer number on each of the titles
        for title in self._titles:
            title.performer_number = self._number

        # To be set later
        self._albums = []
        self._album_numbers = []
        self._albums_initialised = False

        self._freeze()

    def __str__(self):
        return '{}: {} {}, albums: {} {}, titles: {}'.format(
            self.__class__.__name__,
            self._number,
            self._name,
            self.number_of_albums, self._album_numbers,
            self.number_of_titles)

    def init_albums(self, albums):
        for title in self._titles:
            if title.album_number not in self._album_numbers:
                self._album_numbers.append(title.album_number)
                self._albums.append(albums[title.album_number])
        self._albums_initialised = True

    @property
    def album_numbers(self):
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

    def album(self, album_number):
        for a in self._albums:
            if a.number == album_number:
                return a
        return None

    def number_of_titles_for_album(self, album_number):
        count = set()
        for title in self._titles:
            if title.album_number == album_number:
                count.add(title.index)
        return len(count)
