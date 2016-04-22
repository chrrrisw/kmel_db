import unittest
from kmeldb import KenwoodDatabase
from tests import create_media_files as cmf


class TestDB(unittest.TestCase):

    def test_db_1(self):
        mf = cmf.multiple_cds(
            album_names=['Album 1', 'Album 2', 'Album 2', 'Album 3'],
            numbers_of_tracks=10,
            disc_numbers=1,
            offsets=0)

        # for f in mf:
        #     print(f)

        db = KenwoodDatabase.KenwoodDatabase('/tmp')
        db.write_db(mf, [])
        db.finalise()

    def test_db_2(self):
        cmf.random_tracks()
        db = KenwoodDatabase.KenwoodDatabase('/tmp')
        db.write_db(cmf.FILE_LIST, [])
        db.finalise()
