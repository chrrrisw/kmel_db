#!/usr/bin/python3
# encoding: utf-8
'''
DapGen -- a Kenwood database generator.

DapGen is a media file scanner that scans a path for all media files, and
generates a database for Kenwood car stereos.

This module defines the following classes:
    MediaLocation

@author:     Chris Willoughby

@copyright:  2014,2015 Chris Willoughby. All rights reserved.

@license:    Apache License 2.0

@contact:    chrrrisw <at> gmail <dot> com
@deffield    updated: Updated
'''

import sys
import os
import logging
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from kmeldb.KenwoodDatabase import KenwoodDatabase
from kmeldb.mounts import get_fat_mounts

if sys.platform.startswith('linux'):
    from kmeldb.linux_dir_parser import DirWalker
elif sys.platform == 'darwin':
    from kmeldb.mac_dir_parser import DirWalker
elif sys.platform == 'win32':
    pass

log = logging.getLogger(__name__)

__all__ = []
__version__ = 0.2
__date__ = '2014-05-12'
__updated__ = '2016-04-16'

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

        log.info("MediaLocation created at: {}".format(self.topdir))

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
        self.media_files = []

        # Walk the directory tree
        self.dir_walker = DirWalker(self.topdir, self.playlists, self.media_files)
        self.dir_walker.walk()

        # # Check to guard against missing fwalk (Mac)
        # if hasattr(os, 'fwalk'):
        #     for root, dirs, files, rootfd in os.fwalk(self.topdir):
        #         self.get_directory_entries(self, root, rootfd, files)
        # else:
        #     for root, dirs, files in os.walk(self.topdir):
        #         rootfd = open(root, 'r')
        #         self.get_directory_entries(self, root, rootfd, files)
        #         rootfd.close()
        # print()

        log.info("Number of media files: {}".format(len(self.media_files)))
        log.info("Number of playlists: {}".format(len(self.playlists)))

        # Read the playlists we found.
        for pl in self.playlists:
            pl.read()

        # Iterate once through the media files and check if they're in any
        # of the playlists.
        for mf in self.media_files:
            for pl in self.playlists:
                if mf.fullname in pl.media_filenames:
                    pl.add_media_file(mf)

    def finalise(self):
        """
        Write and finalise the database.
        """
        log.debug("MediaLocation finalised")
        self.database.write_db(self.media_files, self.playlists)
        self.database.finalise()

    def __str__(self):
        """
        Return a string formatted with the location path.
        """
        return "Location: {}".format(self.topdir)


LGFMT = '%(levelname)-8s: %(filename)s:%(lineno)d - %(message)s'


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

    default_mounts = [m[0] for m in get_fat_mounts()]

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
        if verbose >= 2:
            log_level = logging.DEBUG
        elif verbose == 1:
            log_level = logging.INFO
        else:
            log_level = logging.WARNING

        logging.basicConfig(
            format=LGFMT,
            level=log_level)

        # Check for conflicting includes and excludes
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

            # Write it out
            ml.finalise()

        log.info("Number of media locations: {}".format(len(MediaLocations)))

        return 0

    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0


if __name__ == "__main__":
    sys.exit(main())
