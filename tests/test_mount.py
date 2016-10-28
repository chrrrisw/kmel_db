import unittest
from kmeldb import mounts


class TestMount(unittest.TestCase):

    def test_mount(self):
        mounts1 = mounts.get_fat_mounts()
        # for mount in mounts1:
        #     print(mount)

        if mounts.HAVE_PSUTIL:
            mounts.HAVE_PSUTIL = False
            mounts2 = mounts.get_fat_mounts()
            # for mount in mounts2:
            #     print(mount)

            self.assertEqual(mounts1, mounts2)
