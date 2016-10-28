#!/usr/bin/env /usr/bin/python3
import unittest
from kmeldb import mounts
# import argparse
# import os
import sys

if sys.platform.startswith('linux'):
    from kmeldb.linux_dir_parser import DirWalker
elif sys.platform == 'darwin':
    from kmeldb.mac_dir_parser import DirWalker
elif sys.platform == 'win32':
    pass


# def main():
#     parser = argparse.ArgumentParser(description="List a FAT directory")
#     parser.add_argument(
#         dest="inputdir",
#         action="store",
#         default=None, help="specify input directory")

#     args = parser.parse_args()

#     playlists = []
#     media_files = []

#     if os.path.isdir(args.inputdir):
#         dir_walker = DirWalker(args.inputdir, playlists, media_files)
#         dir_walker.walk()
#     else:
#         print('Please enter a directory name on a FAT partition')


# if __name__ == '__main__':
#     main()

class TestDirWalker(unittest.TestCase):

    def test_dir_walker(self):
        fat_mounts = mounts.get_fat_mounts()

        if mounts:
            playlists = []
            media_files = []
            dir_walker = DirWalker(fat_mounts[0][0], playlists, media_files)
            dir_walker.walk()
