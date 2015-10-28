import logging
log = logging.getLogger()


class BaseIndexEntry(object):
    identifier = "Base"

    def __init__(self, values):
        pass

    def set_dir_count(self, dir_count):
        self.dir_count = dir_count

    def set_title_count(self, title_count):
        self.title_count = title_count

    def set_genre_count(self, genre_count):
        self.genre_count = genre_count

    def set_performer_count(self, performer_count):
        self.performer_count = performer_count

    def set_album_count(self, album_count):
        self.album_count = album_count

    def set_playlist_count(self, playlist_count):
        self.playlist_count = playlist_count

    def set_name(self, name):
        self.name = name
        log.debug("{} name: '{}'".format(self.__class__.identifier, self.name))

    def set_titles(self, titles, entries):
        self.titles = titles
        self.set_title_count(len(self.titles))

        log.debug("\t{} titles: {}".format(
            self.__class__.identifier, self.titles))

        # Count things

        self.counts = []
        dirlist = []
        genlist = []
        self.performer_albums = {}
        self.performer_titles = {}
        self.album_titles = {}
        for title in self.titles:
            self.counts.append(
                (entries[title].genre,
                    entries[title].performer,
                    entries[title].album))

            if entries[title].longdir not in dirlist:
                dirlist.append(entries[title].longdir)
            if entries[title].genre not in genlist:
                genlist.append(entries[title].genre)

            if entries[title].performer not in self.performer_albums.keys():
                self.performer_albums[entries[title].performer] = [entries[title].album]
                self.performer_titles[entries[title].performer] = [title]
            else:
                if entries[title].album not in self.performer_albums[entries[title].performer]:
                    self.performer_albums[entries[title].performer].append(entries[title].album)
                if title not in self.performer_titles[entries[title].performer]:
                    self.performer_titles[entries[title].performer].append(title)

            if entries[title].album not in self.album_titles.keys():
                self.album_titles[entries[title].album] = [title]
            else:
                if title not in self.album_titles[entries[title].album]:
                    self.album_titles[entries[title].album].append(title)

        self.set_dir_count(len(dirlist))
        self.set_genre_count(len(genlist))
        self.set_performer_count(len(self.performer_albums))
        self.set_album_count(len(self.album_titles))

        log.debug("\t{} performer albums {}".format(
            self.__class__.identifier, self.performer_albums))
        log.debug("\t{} performer titles {}".format(
            self.__class__.identifier, self.performer_titles))
        log.debug("\t{} album titles {}".format(
            self.__class__.identifier, self.album_titles))

    def __str__(self):
        contents = "{}: '{}', titles: {}".format(
            self.__class__.identifier, self.name, str(self.titles))
        return contents


