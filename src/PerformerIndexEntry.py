from BaseIndexEntry import BaseIndexEntry


class PerformerIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(PerformerIndexEntry, self).__init__(name, titles, number)

        # Set the performer number on each of the titles
        for title in self._titles:
            title.performer_number = self._number

        # To be set later
        self._albums = []
        self._albums_initialised = False

        self._freeze()

    def __str__(self):
        return '{}: {} {}, albums: {} {}, titles: {}'.format(
            self.__class__.__name__,
            self._number,
            self._name,
            self.number_of_albums, self._albums,
            self.number_of_titles)

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
        return len(self._albums)
