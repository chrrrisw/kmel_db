#!/usr/bin/python3
# encoding: utf-8
'''
DapGen -- a Kenwood database generator.

DapGen is a media file scanner that scans a path for all media files, and
generates a database for Kenwood car stereos.

It defines the following classes:
    Playlist
    MainIndexEntry
    GenreIndexEntry
    PerformerIndexEntry
    AlbumIndexEntry
    PlaylistIndexEntry
    SubIndexEntry
    MediaFile
    KenwoodDatabase
    MediaLocation

@author:     Chris Willoughby

@copyright:  2014 Chris Willoughby. All rights reserved.

@license:    Apache License 2.0

@contact:    chrrrisw <at> gmail <dot> com
@deffield    updated: Updated
'''

import sys
import os
import logging
import struct
import fcntl
from hsaudiotag import auto

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from KenwoodDatabase import KenwoodDatabase
from MediaFile import MediaFile
from mounts import get_fat_mounts
import vfat_ioctl

log = logging.getLogger(__name__)

__all__ = []
__version__ = 0.1
__date__ = '2014-05-12'
__updated__ = '2014-05-12'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

valid_media_files = ['mp3', 'wma']
valid_media_playlists = []


class Playlist(object):
    """
    An object to hold a playlist. Reads a previously created playlist for
    inclusion in the database.
    """

    def __init__(self):
        """
        Not yet implemented.
        """

        log.debug("Playlist created")


# Holds the list of all media locations
MediaLocations = []


class MediaLocation(object):
    """
    An object to hold the media files within a given directory path.
    It instantiates a KenwoodDatabase and one MediaFile per file.
    """

    def __init__(self, path):
        """
        Store the path, create empty lists in which to store media files
        and playlists.
        """
        self.topdir = path

        log.debug("MediaLocation created at: {}".format(self.topdir))

        # Create the database file location
        self.db_path = os.path.join(self.topdir, "kenwood.dap")
        if os.path.exists(self.db_path):
            log.info("Database directory exists")
        else:
            log.info("Data directory does not exist - creating")
            os.mkdir(self.db_path)

        # Create the database instance
        self.database = KenwoodDatabase(self.db_path)

        # The list of playlists
        self.playlists = []

        # The list of media files
        self.mediaFiles = []

        # Walk the directory tree
        self._file_index = -1
        self._paths = {}
        self._buffer = bytearray(vfat_ioctl.BUFFER_SIZE)
        for root, dirs, files, rootfd in os.fwalk(self.topdir):
            self.get_directory_entries(root, rootfd, files)

        log.info("Number of media files: {}".format(len(self.mediaFiles)))

    def get_directory_entries(self, root, rootfd, files):

        # Get the path relative to the top level directory
        relative_path = os.path.relpath(root, self.topdir)

        # If we don't have it, it's the top level directory so we
        # seed the _paths dictionary.
        if relative_path not in self._paths:
            self._paths[relative_path] = {'shortname': '/'}

        # Get the shortname for the directory (collected one level up).
        current_path_shortname = self._paths[relative_path]['shortname']

        while True:

            # Get both names for the next directory entry using a ioctl call.
            result = fcntl.ioctl(
                rootfd,
                vfat_ioctl.VFAT_IOCTL_READDIR_BOTH,
                self._buffer)

            # Have we finished?
            if result < 1:
                break

            # Interpret the resultant bytearray
            # sl = length of shortname
            # sn = shortname
            # ll = length of longname
            # ln = longname
            sl, sn, ll, ln = struct.unpack(
                vfat_ioctl.BUFFER_FORMAT,
                self._buffer)

            # Decode the bytearrays into strings
            # If longname has zero length, use shortname
            shortname = sn[:sl].decode()
            if ll > 0:
                filename = ln[:ll].decode()
            else:
                filename = shortname

            # Don't process . or ..
            if (filename != '.') and (filename != '..'):
                fullname = os.path.join(root, filename)
                # Check whether it's a directory
                if os.path.isdir(fullname):
                    # Create the _paths entry, add following os.sep
                    self._paths[os.path.relpath(fullname, self.topdir)] = {
                        'shortname': os.path.join(
                            current_path_shortname, shortname, '')}
                else:
                    if filename[-3:] in valid_media_files:
                        self._file_index += 1

                        title = ""
                        performer = ""
                        album = ""
                        genre = ""

                        # TODO: Determine what to do when there is
                        # no ID3 information
                        #
                        # Title <- filename without extension
                        # Album <- directory?
                        # Performer <- directory?
                        # Genre <- 0
                        metadata = auto.File(fullname)
                        title = metadata.title
                        if title == "":
                            title = filename.split(".")[0]
                        performer = metadata.artist
                        if performer == "":
                            pass
                        album = metadata.album
                        if album == "":
                            pass
                        genre = metadata.genre
                        if genre == "":
                            pass

                        mf = MediaFile(
                            index=self._file_index,
                            shortdir=self._paths[relative_path]['shortname'],
                            shortfile=shortname,
                            longdir='{}{}{}'.format(os.sep, relative_path, os.sep),
                            longfile=filename,
                            title=title,
                            performer=performer,
                            album=album,
                            genre=genre)

                        self.mediaFiles.append(mf)

                        log.debug(mf)

                    # self._paths[relative_path]['files'].append({
                    #     'shortname': shortname,
                    #     'fullname': fullname,
                    #     'filename': filename})

    def deprecated_get_directory_entries(self, root, rootfd, files):
        log.debug("Root: {}".format(root))
        for media_file in files:
            if media_file[-3:] in valid_media_files:
                self._file_index += 1
                log.debug("{}".format(os.path.join(root, media_file)))

                title = ""
                performer = ""
                album = ""
                genre = ""

                # TODO: Determine what to do when there is
                # no ID3 information
                #
                # Title <- filename without extension
                # Album <- directory?
                # Performer <- directory?
                # Genre <- 0
                metadata = auto.File(os.path.join(root, media_file))
                title = metadata.title
                if title == "":
                    title = media_file.split(".")[0]
                performer = metadata.artist
                if performer == "":
                    pass
                album = metadata.album
                if album == "":
                    pass
                genre = metadata.genre
                if genre == "":
                    pass

                # try:
                #    metadata = id3.ID3(os.path.join(root,media_file))
                # except id3.ID3NoHeaderError:
                #    log.warning("No ID3 Header: {}".format(media_file))
                #    metadata = {}
                #
                # if 'TIT2' in metadata:
                #    title = str(metadata['TIT2'])
                #
                # if 'TPE1' in metadata:
                #    performer = str(metadata['TPE1'])
                #
                # if 'TALB' in metadata:
                #    album = str(metadata['TALB'])
                #
                # if 'TCON' in metadata:
                #    genre = str(metadata['TCON'])

                longdir = "/" + os.path.relpath(root, self.topdir) + "/"
                longfile = media_file

                if mdir_parser is not None:
                    shortdir = mdir_parser.short_directory_name(longdir)
                    shortfile = mdir_parser.short_file_name(
                        longdir,
                        longfile)
                else:
                    shortdir = ""
                    shortfile = ""

                mf = MediaFile(
                    self._file_index,
                    shortdir,
                    shortfile,
                    longdir,
                    longfile,
                    title,
                    performer,
                    album,
                    genre)

                self.mediaFiles.append(mf)

                log.debug(mf)

    def finalise(self):
        """
        Write and finalise the database.
        """
        log.debug("MediaLocation finalised")
        self.database.write_db(self.mediaFiles)
        self.database.finalise()

    def __str__(self):
        """
        Return a string formatted with the location path.
        """
        return "Location: {}".format(self.topdir)

LGFMT = '%(asctime)-15s: %(levelname)s - %(filename)s:%(lineno)d - %(message)s'


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Chris Willoughby on %s.
  Copyright 2014 Chris Willoughby. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    mounts = get_fat_mounts()
    default_mounts = []
    for m in mounts:
        default_mounts.append(m[0])

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter)

        parser.add_argument(
            "-v", "--verbose",
            dest="verbose",
            action="count",
            help='''Set logging verbosity level (repeat to increase)
                [default: %(default)s]''',
            default=0)

        parser.add_argument(
            "-i", "--include",
            dest="include",
            help='''Only include media files matching this regex pattern.
                Note: exclude is given preference over include.
                [default: %(default)s]''',
            metavar="RE")

        parser.add_argument(
            "-e", "--exclude",
            dest="exclude",
            help='''Exclude media files matching this regex pattern.
                [default: %(default)s]''',
            metavar="RE")

        parser.add_argument(
            '-V', '--version',
            action='version',
            version=program_version_message)

        parser.add_argument(
            dest="paths",
            help='''Paths to folder(s) with media file(s).
                Default is all FAT partitions: %(default)s''',
            metavar="path",
            nargs='*',
            default=default_mounts)

        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        verbose = args.verbose
        inpat = args.include
        expat = args.exclude

        # Set logging level
        if verbose == 2:
            log_level = logging.DEBUG
            log.debug("DEBUG logging enabled")

        elif verbose == 1:
            log_level = logging.INFO
            log.debug("WARNING logging enabled")

        else:
            log_level = logging.WARNING

        logging.basicConfig(
            format=LGFMT,
            level=log_level)

        if inpat and expat and inpat == expat:
            print(
                'Include and Exclude pattern are equal! ' +
                'Nothing will be processed.')
            return -1

        for inpath in paths:
            log.debug("Processing path: {}".format(inpath))

            # Create a MediaLocation and store it in the list
            ml = MediaLocation(inpath)
            MediaLocations.append(ml)
            ml.finalise()

        log.info("Number of media locations: {}".format(len(MediaLocations)))

        return 0

    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0

#     except Exception as e:
#         if DEBUG or TESTRUN:
#             raise(e)
#         indent = len(program_name) * " "
#         sys.stderr.write(program_name + ": " + repr(e) + "\n")
#         sys.stderr.write(indent + "  for help use --help")
#         return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")

    if TESTRUN:
        import doctest
        doctest.testmod()

    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'DapGen_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)

    sys.exit(main())
