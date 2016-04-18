from .BaseIndexEntry import BaseIndexEntry


class AlbumIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(AlbumIndexEntry, self).__init__(name, titles, number)

        self._discs_and_tracks = {}

        for title in self._titles:
            # Set the album number on each of the titles
            title.album_number = self._number

            # Store titles according to disc and track number
            # TODO: Cope with more than two discs
            discnumber = title.discnumber
            if discnumber not in self._discs_and_tracks:
                self._discs_and_tracks[discnumber] = {}
            if title.tracknumber in self._discs_and_tracks[discnumber]:
                print ("Duplicate track numbers:")
                print ("\tFirst", title.tracknumber, self._discs_and_tracks[discnumber][title.tracknumber].title)
                print ("\tSecond", title.tracknumber, title.title)
                discnumber = title.discnumber + 1
                if discnumber not in self._discs_and_tracks:
                    self._discs_and_tracks[discnumber] = {}
                print ("\tSetting disc number to: {} - you may want to edit the file and set disc number yourself.".format(discnumber))
            self._discs_and_tracks[discnumber][title.tracknumber] = title

        self._freeze()

    # Getters

    @property
    def title_numbers(self):
        return [self._discs_and_tracks[d][t].index for d in sorted(self._discs_and_tracks) for t in sorted(self._discs_and_tracks[d])]

    @property
    def tracks(self):
        '''Return titles in album disc and track order'''
        return [self._discs_and_tracks[d][t] for d in sorted(self._discs_and_tracks) for t in sorted(self._discs_and_tracks[d])]
