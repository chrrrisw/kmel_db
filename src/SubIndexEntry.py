import struct


class SubIndexEntry(object):

    __isfrozen = False

    def __init__(self):
        self._offset = 0
        self._size = 0
        self._count = 0

        self._freeze()

    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError("%r is a frozen class" % self)
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        self._count = count

    def get_representation(self):
        return struct.pack(
            "<IHH",
            self._offset,
            self._size,
            self._count)
