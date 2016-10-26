'''Defines a subclass of BaseIndexEntry to handle Albums.'''
from .BaseIndexEntry import BaseIndexEntry


class AlbumIndexEntry(BaseIndexEntry):
    '''A class to hold album information.
    '''

    def __init__(self, name, titles, number):
        super(AlbumIndexEntry, self).__init__(name, titles, number)

        self._discs_and_tracks = {}

        for title in self._titles:
            # Set the album number on each of the titles
            title.album_number = self._number

            # Store titles according to disc and track number
            discnumber = title.discnumber
            modified = False
            new_location = False
            while not new_location:
                if discnumber not in self._discs_and_tracks:
                    self._discs_and_tracks[discnumber] = {}
                    new_location = True
                    break
                if title.tracknumber in self._discs_and_tracks[discnumber]:
                    discnumber += 1
                    modified = True
                else:
                    new_location = True

            if modified:
                print("Modified disc number for track {} '{}' to {}".format(
                    title.tracknumber,
                    title.title,
                    discnumber))

            self._discs_and_tracks[discnumber][title.tracknumber] = title

        self._freeze()

    # Getters

    @property
    def title_numbers(self):
        '''Return a list of title indices in album disc and track order.'''
        return [self._discs_and_tracks[d][t].index
                for d in sorted(self._discs_and_tracks)
                for t in sorted(self._discs_and_tracks[d])]

    @property
    def tracks(self):
        '''Return a list of titles in album disc and track order'''
        return [self._discs_and_tracks[d][t]
                for d in sorted(self._discs_and_tracks)
                for t in sorted(self._discs_and_tracks[d])]
