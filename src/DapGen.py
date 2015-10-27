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
from hsaudiotag import auto

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from KenwoodDatabase import KenwoodDatabase
from MediaFile import MediaFile

log = logging.getLogger(__name__)

__all__ = []
__version__ = 0.1
__date__ = '2014-05-12'
__updated__ = '2014-05-12'

DEBUG = 0
TESTRUN = 1
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
        self.path = path

        log.debug("MediaLocation created at: {}".format(self.path))

        # Create the database file location
        self.db_path = os.path.join(self.path, "kenwood.dap")
        if os.path.exists(self.db_path):
            log.info("database directory exists")
        else:
            log.info("data directory does not exist - creating")
            os.mkdir(self.db_path)

        self.database = KenwoodDatabase(self.db_path)

        # The list of playlists
        self.playlists = []

        # The list of media files
        self.mediaFiles = []
        index = -1
        for root, dirs, files in os.walk(self.path):
            log.debug("Root: {}".format(root))
            for media_file in files:
                if media_file[-3:] in valid_media_files:
                    index += 1
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

                    longdir = "/" + os.path.relpath(root, self.path) + "/"
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
                        index,
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

        log.info("Number of media files: {}".format(len(self.mediaFiles)))

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
        return "Location: {}".format(self.path)


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg

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

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license,
            formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(
            "-v", "--verbose",
            dest="verbose",
            action="count",
            help="set verbosity level [default: %(default)s]")
        parser.add_argument(
            "-i", "--include",
            dest="include",
            help="only include media files matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]",
            metavar="RE")
        parser.add_argument(
            "-e", "--exclude",
            dest="exclude",
            help="exclude media files matching this regex pattern. [default: %(default)s]",
            metavar="RE")
        parser.add_argument(
            '-V', '--version',
            action='version',
            version=program_version_message)
        parser.add_argument(
            dest="paths",
            help="paths to folder(s) with media file(s) [default: %(default)s]",
            metavar="path",
            nargs='+')

        # Process arguments
        args = parser.parse_args()

        paths = args.paths
        verbose = args.verbose
        inpat = args.include
        expat = args.exclude

        if verbose is not None:
            logging.basicConfig(
                format=LGFMT,
                level=logging.DEBUG)
            log.debug("Verbose mode on")
        else:
            logging.basicConfig(
                format=LGFMT,
                level=logging.INFO)

        if inpat and expat and inpat == expat:
            raise CLIError("include and exclude pattern are equal! Nothing will be processed.")

        for inpath in paths:
            log.debug("Path: ".format(inpath))

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
        sys.argv.append("-r")

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
