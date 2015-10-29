import struct
from BaseIndexEntry import BaseIndexEntry


class PerformerIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(PerformerIndexEntry, self).__init__(name, titles, number)

        # Set the performer number on each of the titles
        for title in self._titles:
            title.set_performer_number(self._number)

        # To be set later
        self._albums = []
        self._albums_initialised = False

        self._freeze()

    def init_albums(self):
        for title in self._titles:
            if title.get_album_number() not in self._albums:
                self._albums.append(title.get_album_number())
        self._albums_initialised = True

    def get_albums(self):
        if self._albums_initialised:
            return self._albums
        else:
            raise

    def get_number_of_albums(self):
        return len(self._albums)
