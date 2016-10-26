import string
import random
from kmeldb import MediaFile
from pprint import pprint


def single_cd(
        album_name,
        number_of_tracks,
        disc_number,
        offset=0,
        performer='performer',
        genre='genre',
        reversed=False):
    '''
    Creates a single CD worth of tracks and returns it.
    '''
    longdir = '{}/{}'.format(performer, album_name)
    longfile_template = '{} - Title.mp3'
    media_files = []
    if reversed:
        indices = range(number_of_tracks - 1, -1, -1)
    else:
        indices = range(number_of_tracks)
    for index in indices:
        mf = MediaFile.MediaFile(
            index=index + offset,
            fullname='fullname_{}'.format(index + offset),
            shortdir='shortdir_{}'.format(index + offset),
            shortfile='shortfile_{}'.format(index + offset),
            longdir=longdir,
            longfile=longfile_template.format(index + offset),
            title='Title {} Track {}'.format(album_name, index + offset),
            performer=performer,
            album=album_name,
            genre=genre,
            tracknumber=index + 1,
            discnumber=disc_number)
        media_files.append(mf)
    return media_files


def multiple_cds(album_names, numbers_of_tracks, disc_numbers, offsets=0):

    def number_of_tracks(index):
        if isinstance(numbers_of_tracks, list):
            return numbers_of_tracks[index]
        else:
            return numbers_of_tracks

    def disc_number(index):
        if isinstance(disc_numbers, list):
            return disc_numbers[index]
        else:
            return disc_numbers

    def offset(index):
        if isinstance(offsets, list):
            return offsets[index]
        else:
            return offsets

    media_files = []
    for index in range(len(album_names)):
        performer = 'Performer {}'.format(album_names[index])
        genre = 'Genre {}'.format(album_names[index])
        media_files.extend(single_cd(
            album_name=album_names[index],
            number_of_tracks=number_of_tracks(index),
            disc_number=disc_number(index),
            offset=offset(index),
            performer=performer,
            genre=genre))
    return media_files


def single_genre(
        genre_name,
        number_of_tracks,
        offset=0,
        performer='performer',
        album='album'):
    '''
    Creates a single genre worth of tracks and returns it.
    '''
    longdir = '{}/{}'.format(performer, album)
    longfile_template = '{} - Title.mp3'
    media_files = []
    for index in range(number_of_tracks):
        mf = MediaFile.MediaFile(
            index=index + offset,
            fullname='fullname_{}'.format(index + offset),
            shortdir='shortdir_{}'.format(index + offset),
            shortfile='shortfile_{}'.format(index + offset),
            longdir=longdir,
            longfile=longfile_template.format(index + offset),
            title='Title {} Track {}'.format(album, index + offset),
            performer=performer,
            album=album,
            genre=genre_name,
            tracknumber=index + 1,
            discnumber=1)
        media_files.append(mf)
    return media_files


def single_performer(
        performer_name,
        number_of_tracks,
        offset=0,
        genre='genre',
        album='album'):
    '''
    Creates a single performer worth of tracks and returns it.
    '''
    longdir = '{}/{}'.format(performer_name, album)
    longfile_template = '{} - Title.mp3'
    media_files = []
    for index in range(number_of_tracks):
        mf = MediaFile.MediaFile(
            index=index + offset,
            fullname='fullname_{}'.format(index + offset),
            shortdir='shortdir_{}'.format(index + offset),
            shortfile='shortfile_{}'.format(index + offset),
            longdir=longdir,
            longfile=longfile_template.format(index + offset),
            title='Title {} Track {}'.format(album, index + offset),
            performer=performer_name,
            album=album,
            genre=genre,
            tracknumber=index + 1,
            discnumber=1)
        media_files.append(mf)
    return media_files


def random_string(length, suffix=''):
    return ''.join(
        random.choice(
            string.ascii_letters + string.digits) for _ in range(length)) + suffix

FILE_LIST = []
FILES = {}
PERFORMER_FILES = {}
PERFORMER_NAMES = []
ALBUM_FILES = {}
ALL_ALBUM_NAMES = []
GENRE_FILES = {}
GENRE_NAMES = []


def random_tracks():
    global PERFORMER_NAMES
    global GENRE_NAMES

    num_performers = random.randint(4, 8)
    PERFORMER_NAMES = [random_string(6, '_per') for _ in range(num_performers)]
    PERFORMER_NAMES.sort(key=str.lower)
    # print(PERFORMER_NAMES)

    albums = {}
    for performer in PERFORMER_NAMES:
        num_albums = random.randint(1, 3)
        album_names = [random_string(6, '_alb') for _ in range(num_albums)]
        album_names.sort(key=str.lower)
        ALL_ALBUM_NAMES.extend(album_names)
        albums[performer] = album_names
    # print(albums)
    ALL_ALBUM_NAMES.sort(key=str.lower)

    num_genres = random.randint(1, 10)
    GENRE_NAMES = [random_string(6, '_gen') for _ in range(num_genres)]
    GENRE_NAMES.sort(key=str.lower)
    # print(GENRE_NAMES)

    file_index = 0
    for performer in PERFORMER_NAMES:
        FILES[performer] = {}
        PERFORMER_FILES[performer] = []
        for album in albums[performer]:
            FILES[performer][album] = []
            ALBUM_FILES[album] = []
            num_files = random.randint(5, 10)
            for index in range(num_files):
                title = random_string(8)
                genre = random.choice(GENRE_NAMES)
                if genre not in GENRE_FILES:
                    GENRE_FILES[genre] = []
                mf = MediaFile.MediaFile(
                    index=file_index,
                    fullname=''.format(),
                    shortdir='{}/{}'.format(performer, album),
                    shortfile='{}.mp3'.format(title),
                    longdir='{}/{}'.format(performer, album),
                    longfile='{}.mp3'.format(title),
                    title=title,
                    performer=performer,
                    album=album,
                    genre=genre,
                    tracknumber=index + 1,
                    discnumber=1)
                FILE_LIST.append(mf)
                FILES[performer][album].append(mf)
                PERFORMER_FILES[performer].append(mf)
                ALBUM_FILES[album].append(mf)
                GENRE_FILES[genre].append(mf)
                file_index += 1

    # print(len(files))
    # print(len(performer_files))
    # print(len(album_files))
    # print(len(genre_files))
    # pprint(album_files)

    # Now need to sort media files by album, disc and track to re-index
    # for album in sorted(ALBUM_FILES.keys(), key=str.lower):
    #     print(album)
