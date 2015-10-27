#!/usr/bin/env /usr/bin/python3
import argparse
import os
import fcntl
import struct
import vfat_ioctl


class FATParser(object):
    def __init__(self, topdir):
        self.topdir = topdir
        self.paths = {}
        self.buffer = bytearray(vfat_ioctl.BUFFER_SIZE)
        for root, dirs, files, rootfd in os.fwalk(topdir):
            self.get_directory_entries(root, rootfd)

    def get_directory_entries(self, directory_name, directory_fd):

        # Get the path relative to the top level directory
        relative_path = os.path.relpath(directory_name, self.topdir)

        # If we don't have it, it's the top level directory so we
        # seed the paths dictionary. If we have it, get the shortname
        # for the directory (collected one level up).
        if relative_path not in self.paths:
            self.paths[relative_path] = {
                'shortname': relative_path,
                'files': []}
            current_path_shortname = relative_path
        else:
            current_path_shortname = self.paths[relative_path]['shortname']

        while True:

            # Get both names for the next directory entry using a ioctl call.
            result = fcntl.ioctl(
                directory_fd,
                vfat_ioctl.VFAT_IOCTL_READDIR_BOTH,
                self.buffer)

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
                self.buffer)

            # Decode the bytearrays into strings
            # If longname has zero length, use shortname
            shortname = sn[:sl].decode()
            if ll > 0:
                filename = ln[:ll].decode()
            else:
                filename = shortname

            # Don't process . or ..
            if (filename != '.') and (filename != '..'):
                # Check whether it's a directory
                fullname = os.path.join(directory_name, filename)
                if os.path.isdir(fullname):
                    # Create the paths entry
                    self.paths[os.path.relpath(fullname, self.topdir)] = {
                        'shortname': os.path.join(
                            current_path_shortname, shortname),
                        'files': []}
                else:
                    self.paths[relative_path]['files'].append({
                        'shortname': shortname,
                        'fullname': fullname,
                        'filename': filename})

    def display(self):
        for path in self.paths:
            print('{} --> {}'.format(path, self.paths[path]['shortname']))
            for f in self.paths[path]['files']:
                print('\t {} --> {}'.format(f['filename'], f['shortname']))


def main():
    parser = argparse.ArgumentParser(description="List a FAT directory")
    parser.add_argument(
        dest="inputdir",
        action="store",
        default=None, help="specify input directory")

    args = parser.parse_args()

    if os.path.isdir(args.inputdir):
        fat_parser = FATParser(args.inputdir)
        fat_parser.display()
    else:
        print('Please enter a directory name on a FAT partition')

if __name__ == '__main__':
    main()
