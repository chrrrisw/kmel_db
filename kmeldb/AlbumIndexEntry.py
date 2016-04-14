from .BaseIndexEntry import BaseIndexEntry


class AlbumIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(AlbumIndexEntry, self).__init__(name, titles, number)

        self._title_numbers = []
        self._discs_and_tracks = {}

        for title in self._titles:
            # Set the album number on each of the titles
            title.album_number = self._number

            # Append the title index to the list
            self._title_numbers.append(title.index)

            # Store titles according to disc and track number
            if title.discnumber not in self._discs_and_tracks:
                self._discs_and_tracks[title.discnumber] = {}
            if title.tracknumber in self._discs_and_tracks[title.discnumber]:
                print ("Duplicate track number", title.tracknumber, title.title)
            self._discs_and_tracks[title.discnumber][title.tracknumber] = title

        self._freeze()

    # Getters

    @property
    def title_numbers(self):
        return self._title_numbers

    @property
    def tracks(self):
        '''Return titles in album disc and track order'''
        return [self._discs_and_tracks[d][t] for d in sorted(self._discs_and_tracks) for t in sorted(self._discs_and_tracks[d])]
