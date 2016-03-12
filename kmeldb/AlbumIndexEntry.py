from .BaseIndexEntry import BaseIndexEntry


class AlbumIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(AlbumIndexEntry, self).__init__(name, titles, number)

        self._title_numbers = []
        self._tracks = {}

        # Set the album number on each of the titles
        for title in self._titles:
            title.album_number = self._number
            self._title_numbers.append(title.index)
            if title.track in self._tracks:
                print ("Duplicate track number", title.track, title.title)
            self._tracks[title.track] = title

        self._freeze()

    # Getters

    @property
    def title_numbers(self):
        return self._title_numbers

    @property
    def tracks(self):
        '''Return titles in album track order'''
        return [self._tracks[t] for t in sorted(self._tracks)]
