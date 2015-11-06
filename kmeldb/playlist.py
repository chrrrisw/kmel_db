#!/usr/bin/python3
# encoding: utf-8
'''
DapGen -- a Kenwood database generator.

DapGen is a media file scanner that scans a path for all media files, and
generates a database for Kenwood car stereos.

This module defines the following classes:
    PlaylistFile
    PLSPlaylistFile
    PlaylistIndexEntry

@author:     Chris Willoughby

@copyright:  2014,2015 Chris Willoughby. All rights reserved.

@license:    Apache License 2.0

@contact:    chrrrisw <at> gmail <dot> com
@deffield    updated: Updated
'''

import os
import logging
import configparser
import urllib.parse
from .BaseIndexEntry import BaseIndexEntry

log = logging.getLogger(__name__)


class PlaylistFile(object):
    """
    An object to hold a playlist. Reads a previously created playlist for
    inclusion in the database.
    """

    def __init__(self, fullname):
        """
        Store the filename.
        """
        log.info("PlaylistFile created")
        self.fullname = fullname
        self.path, self.filename = os.path.split(self.fullname)
        self.title = ''

        # The filenames in the order in which they are read in.
        self._media_filenames = []

        self._media_files = {}

    @property
    def media_filenames(self):
        return self._media_filenames

    @property
    def media_files(self):
        return [self._media_files[i] for i in sorted(self._media_files)]

    def add_media_file(self, media_file):
        '''Add the media file, preserving order.'''
        index = self._media_filenames.index(media_file.fullname)
        self._media_files[index] = media_file

    def read(self):
        raise NotImplementedError


PLS_SECTION = 'playlist'


class PLSPlaylistFile(PlaylistFile):

    def read(self):
        cfg_parser = configparser.ConfigParser(interpolation=None)

        f = open(self.fullname, 'r')

        try:
            cfg_parser.read_file(f)
        except configparser.MissingSectionHeaderError:
            f.close()
            return
        f.close()

        for section in cfg_parser.sections():
            # Some media players (amarok, I'm looking at you) capitalise
            # the section
            if section.lower() == PLS_SECTION:

                self.title = cfg_parser.get(
                    section,
                    'X-GNOME-Title',
                    fallback='')
                if self.title == '':
                    self.title = os.path.splitext(self.filename)[0]

                num_entries = cfg_parser.getint(section, "NumberOfEntries")

                for index in range(1, num_entries + 1):

                    # Handle URIs
                    parsed = urllib.parse.urlparse(cfg_parser.get(
                        section,
                        "File{}".format(index)))
                    media_file = urllib.parse.unquote(parsed.path)

                    # Check for relative paths
                    if media_file.startswith(os.pardir):
                        media_file = os.path.realpath(
                            os.path.join(self.path, media_file))

                    # media_title = cfg_parser.get(
                    #     PLS_SECTION,
                    #     "Title{}".format(index),
                    #     fallback='')

                    # media_length = cfg_parser.get(
                    #     PLS_SECTION,
                    #     "Length{}".format(index),
                    #     fallback=0)

                    if os.path.exists(media_file):
                        self._media_filenames.append(media_file)

                    log.info('PlaylistFile "{}": {}'.format(
                        self.title, media_file))


class PlaylistIndexEntry(BaseIndexEntry):

    def __init__(self, name, titles, number):
        super(PlaylistIndexEntry, self).__init__(name, titles, number)

        # print('Creating playlist index entry: {}'.format(name))

        self._title_numbers = [t.index for t in titles]

        # print('\t with titles: {}'.format(self._title_numbers))

        # Set the playlist number on each of the titles
        # TODO: May be in more than one playlist
        # for title in self._titles:
        #     title.playlist_number = self._number
        #     self._title_numbers.append(title.index)

        self._freeze()

    # Getters

    @property
    def title_numbers(self):
        return self._title_numbers


valid_media_playlists = ('pls')
playlist_classes = {
    'pls': PLSPlaylistFile
}


def playlist(fullname):
    extension = os.path.splitext(fullname)[1][1:]
    return playlist_classes[extension](fullname)
