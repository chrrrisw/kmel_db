import argparse
import os
import fcntl
import struct

VFAT_IOCTL_READDIR_BOTH = 2184212993
VFAT_IOCTL_READDIR_SHORT = 2184212994
# sizeof(__fat_dirent) = 280
# struct __fat_dirent {
#     long        d_ino;  --> 8 bytes
#     __kernel_off_t  d_off;  --> 8 bytes
#     unsigned short  d_reclen;  --> 2 bytes
#     char        d_name[256]; /* We must not include limits.h! */
# };


class directory_entry(object):
    def __init__(self):
        pass


class FATParser(object):
    def __init__(self, topdir):
        self.topdir = topdir
        self.paths = {}
        self.buffer = bytearray(560)
        for root, dirs, files, rootfd in os.fwalk(topdir):
            self.get_directory_entries(root, rootfd)

    def get_directory_entries(self, directory_name, directory_fd):
        while True:
            # Get both names for the directory entry
            result = fcntl.ioctl(
                directory_fd,
                VFAT_IOCTL_READDIR_BOTH,
                self.buffer)

            # Have we finished?
            if result < 1:
                break

            si, so, sl, sn, li, lo, ll, ln = struct.unpack(
                '@llH262sllH262s',
                self.buffer)

            shortname = sn[:sl].decode()
            if ll > 0:
                filename = ln[:ll].decode()
            else:
                filename = shortname

            if (filename != '.') and (filename != '..'):
                fullname = os.path.join(directory_name, filename)
                if os.path.isdir(fullname):
                    # pass
                    print('Directory', fullname, shortname)
                    self.paths[fullname] = (shortname, {})
                else:
                    pass
                    # print('File', fullname)
                    # print('\t', shortname)


def main():
    parser = argparse.ArgumentParser(description="List a FAT directory")
    parser.add_argument(
        dest="inputdir",
        action="store",
        default=None, help="specify input directory")

    args = parser.parse_args()
    # print(args.inputdir)

    fat_parser = FATParser(args.inputdir)

    # fd = os.open(args.inputdir, os.O_RDONLY | os.O_DIRECTORY)

    # paths = {}
    # ba = bytearray(560)
    # result = 1
    # while True:
    #     # Get both names for the directory entry
    #     result = fcntl.ioctl(fd, VFAT_IOCTL_READDIR_BOTH, ba)

    #     # Have we finished?
    #     if result < 1:
    #         break

    #     si, so, sl, sn, li, lo, ll, ln = struct.unpack('@llH262sllH262s', ba)
    #     # print(si, so, sl, sn[:sl].decode())
    #     # print(li, lo, ll, ln[:ll].decode())
    #     shortname = sn[:sl].decode()
    #     if ll > 0:
    #         filename = ln[:ll].decode()
    #     else:
    #         filename = shortname

    #     if os.path.isdir(os.path.join(args.inputdir, filename)):
    #         print('Directory', os.path.join(args.inputdir, filename))
    #         paths[filename] = (shortname, {})
    #     else:
    #         print('File', os.path.join(args.inputdir, filename))

    # os.close(fd)

if __name__ == '__main__':
    main()


