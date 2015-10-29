import struct
from BaseIndexEntry import BaseIndexEntry


class AlbumIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(AlbumIndexEntry, self).__init__(name, titles, number)

        self._title_numbers = []

        # Set the album number on each of the titles
        for title in self._titles:
            title.set_album_number(self._number)
            self._title_numbers.append(title.get_index())

        self._freeze()

    # Getters

    @property
    def title_numbers(self):
        return self._title_numbers
