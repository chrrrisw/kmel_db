import logging
import os
import struct
from hsaudiotag import auto

from kmeldb.MediaFile import MediaFile, valid_media_files
from kmeldb.playlist import playlist, valid_media_playlists

try:
    import fcntl
except ImportError:
    HAVE_FCNTL = False
else:
    HAVE_FCNTL = True

from kmeldb import vfat_ioctl

log = logging.getLogger(__name__)


class DirWalker(object):

    def __init__(self, topdir, playlists, media_files):
        self._topdir = topdir
        self._playlists = playlists
        self._media_files = media_files

        self._file_index = -1
        self._playlist_index = -1
        self._paths = {}
        self._buffer = bytearray(vfat_ioctl.BUFFER_SIZE)

    def walk(self):
        for root, dirs, files in os.walk(self.topdir):
            rootfd = open(root, 'r')
            self.get_directory_entries(self, root, rootfd, files)
            rootfd.close()

    def get_directory_entries(self, root, rootfd, files):

        log.info('Processing: {}'.format(root))

        # Get the path relative to the top level directory
        relative_path = os.path.relpath(root, self._topdir)

        # If we don't have it, it's the top level directory so we
        # seed the _paths dictionary.
        if relative_path not in self._paths:
            self._paths[relative_path] = {'shortname': '/'}

        # Get the shortname for the directory (collected one level up).
        current_path_shortname = self._paths[relative_path]['shortname']

        while True and HAVE_FCNTL:

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
                    self._paths[os.path.relpath(fullname, self._topdir)] = {
                        'shortname': os.path.join(
                            current_path_shortname, shortname, '')}
                else:
                    if filename.lower().endswith(valid_media_files):
                        self._file_index += 1
                        print('Files: {}, Playlists: {}'.format(
                            self._file_index + 1,
                            self._playlist_index + 1), end='\r')

                        title = ""
                        performer = ""
                        album = ""
                        genre = ""

                        # If there is no ID3 information:
                        #
                        # Title <- filename without extension
                        # Album <- parent directory
                        # Performer <- grandparent directory
                        # Genre <- 0
                        metadata = auto.File(fullname)
                        title = metadata.title
                        if title == "":
                            title = filename.split(".")[0]

                        # KMEL seems to remove all but the first performer
                        # if there is a '/' in this field.
                        # To be compatible, we'll do the same.
                        # TODO: Remove this restriction after compatibility
                        # testing.
                        performer = metadata.artist
                        performer = performer.split('/')[0]
                        if performer == "":
                            # KMEL seems to use the grandparent directory if the
                            # performer is empty.
                            try:
                                performer = os.path.basename(os.path.split(relative_path)[0])
                            except:
                                performer = ""

                        album = metadata.album
                        if album == "":
                            # KMEL seems to use the parent directory if the album
                            # is empty.
                            album = os.path.basename(relative_path)

                        genre = metadata.genre
                        if genre == "":
                            pass

                        track = metadata.track

                        if hasattr(metadata, 'disc'):
                            disc = metadata.disc
                        else:
                            disc = 0

                        mf = MediaFile(
                            index=self._file_index,
                            fullname=fullname,
                            shortdir=self._paths[relative_path]['shortname'],
                            shortfile=shortname,
                            longdir='{}{}{}'.format(
                                os.sep, relative_path, os.sep),
                            longfile=filename,
                            title=title,
                            performer=performer,
                            album=album,
                            genre=genre,
                            tracknumber=track,
                            discnumber=disc)

                        self._media_files.append(mf)

                        log.debug(mf)

                    elif filename.lower().endswith(valid_media_playlists):
                        self._playlist_index += 1
                        print('Files: {}, Playlists: {}'.format(
                            self._file_index + 1,
                            self._playlist_index + 1), end='\r')
                        self._playlists.append(playlist(fullname))
