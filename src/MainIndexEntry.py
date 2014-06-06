import struct

STRING_ENCODING = "utf_16_le"

class MainIndexEntry(object):
    def __init__(self, mediafile):
        self._mediaFile = mediafile
        
        self.title_length = len(self._mediaFile.get_title().encode(STRING_ENCODING))
        self.title_char_length = 2
        # To be set later
        self.title_offset = 0 
        
        self.shortdir_length = len(self._mediaFile.get_shortdir().encode("ascii"))
        self.shortdir_char_length = 1
        # To be set later
        self.shortdir_offset = 0 
        
        self.shortfile_length = len(self._mediaFile.get_shortfile().encode("ascii"))
        self.shortfile_char_length = 1
        # To be set later
        self.shortfile_offset = 0 
        
        self.longdir_length = len(self._mediaFile.get_longdir().encode(STRING_ENCODING))
        self.longdir_char_length = 2
        # To be set later
        self.longdir_offset = 0 
        
        self.longfile_length = len(self._mediaFile.get_longfile().encode(STRING_ENCODING))
        self.longfile_char_length = 2
        # To be set later
        self.longfile_offset = 0 

    def get_media_file(self):
        return self._mediaFile
    
    # Calls through to mediafile
    
    def get_index(self):
        return self._mediaFile.get_index()
    
    def get_title(self):
        return self._mediaFile.get_title()
    
    def get_shortdir(self):
        return self._mediaFile.get_shortdir()
    
    def get_shortfile(self):
        return self._mediaFile.get_shortfile()
    
    def get_longdir(self):
        return self._mediaFile.get_longdir()
    
    def get_longfile(self):
        return self._mediaFile.get_longfile()
    
    def get_genre_number(self):
        return self._mediaFile.get_genre_number()
    
    def get_performer_number(self):
        return self._mediaFile.get_performer_number()
    
    def get_album_number(self):
        return self._mediaFile.get_album_number()
    
    # Offsets to be set once known
    
    def set_title_offset(self, title_offset):
        self.title_offset = title_offset
        
    def set_shortdir_offset(self, shortdir_offset):
        self.shortdir_offset = shortdir_offset
        
    def set_shortfile_offset(self, shortfile_offset):
        self.shortfile_offset = shortfile_offset
        
    def set_longdir_offset(self, longdir_offset):
        self.longdir_offset = longdir_offset
        
    def set_longfile_offset(self, longfile_offset):
        self.longfile_offset = longfile_offset
    
    # How to write to file
    
    def get_representation(self):
        return struct.pack("<HHH HIII HHI HHI HHI HHI HHI I",
                           self._mediaFile.get_genre_number(),
                           self._mediaFile.get_performer_number(),
                           self._mediaFile.get_album_number(),
                           0x0000, 0xffffffff, 0x80000000, 0x80000000,
                           self.title_length, self.title_char_length, self.title_offset,
                           self.shortdir_length, self.shortdir_char_length, self.shortdir_offset,
                           self.shortfile_length, self.shortfile_char_length, self.shortfile_offset,
                           self.longdir_length, self.longdir_char_length, self.longdir_offset,
                           self.longfile_length, self.longfile_char_length, self.longfile_offset,
                           0x00000000
                           )
