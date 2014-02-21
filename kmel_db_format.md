# Kenwood Music Editor Light

I have a Kenwood in-car stereo that can play music and podcasts stored on a USB memory stick. Unfortunately some of the functionality offered by the stereo (such as creating playlists and searching by artist, album or genre) is only available after a database has been created on the USB stick. This database is created using a Windows-only application called "Kenwood Music Editor Light".

I store all my podcasts and music on my desktop machine - which is running Linux. The workflow to create this database therefore involves updating the USB key with the music and podcasts I want and then borrowing my partner's Windows laptop to generate the database. This is not ideal.

The other issue I have with Music Editor Light is it's poor handling of playlists. Essentially you have to copy media files into a directory structure that is below where you usually place your media, and then tell the application the directory levels from which to create the playlists. This means that you now have two copies of each media file - one in the album where it belongs, and one in the playlist. I would like a more intelligent way of processing playlists.

I would also like to be able to generate the database in the application that I use to manage my media files. As usual, the database format is not documented anywhere that I can find, so this page is the result of staring at hex for some time. Some of the fields are guesses, and will be labelled with a question mark. References to TCON, TPE1, TALB etc are references to the ID3v2 tags found in some media files.

## The Database Format (so far...)

_Note: Although there are still some unknowns here, they are constant across all the files analysed. The format is, therefore, completely described for the purposes of writing an encoder/decoder._

The description below comes from the comparison of multiple files. These files are named: 1.xxd, 2.xxd, 3.xxd, 4.xxd, 5.xxd, 6.xxd and many.xxd. The 7 digit number next to the file name in the examples below is the file offset (in some cases it may be a relative offset - this will be mentioned). The file format appears to be little-endian. Wide-character strings appear to be UTF-16 encoded. All strings are null-terminated.

The general layout of the file appears to be:

    Signature
    Item Counts
    Offsets to tables
    Main Index
    Title Table
    Short Directory Table
    Short File Table
    Long Directory Table
    Long File Table
    Alphabetically-Ordered-Title List
    Genre Index
    Genre Name Table
    Genre Title Table
    Genre-Ordered-Title List
    Performer Index
    Performer Name Table
    Performer Title Table
    Performer-Ordered-Title List
    Album Index
    Album Name Table
    Album Title Table
    Album-Ordered-Title List
    Unknown 8
    Playlist Index
    Playlist Name Table
    Playlist Title Table
    Unknown 9
    Unknown 10
    Unknown 11
    Unknown 12
    Sub-indices

### Database Header (signature, counts, offsets)

The first eight bytes appear to be a signature (KWDB) and perhaps a version number.<br>
The short int at offset 0x08 is the number of entries in the main index.<br>
The short int at offset 0x0a is the size of entries in the main index.<br>
The short int at offset 0x0c is the number of entries in the TCON (Genre) index.<br>
The short int at offset 0x0e is the size of entries in the TCON (Genre) index.

    1.xxd:0000000:    4b57 4442 0001 0301 0100 4000 0200 1000  KWDB......@.....
    2.xxd:0000000:    4b57 4442 0001 0301 0200 4000 0200 1000  KWDB......@.....
    3.xxd:0000000:    4b57 4442 0001 0301 0300 4000 0200 1000  KWDB......@.....
    4.xxd:0000000:    4b57 4442 0001 0301 0400 4000 0300 1000  KWDB......@.....
    5.xxd:0000000:    4b57 4442 0001 0301 0500 4000 0300 1000  KWDB......@.....
    6.xxd:0000000:    4b57 4442 0001 0301 0600 4000 0300 1000  KWDB......@.....
    many.xxd:0000000: 4b57 4442 0001 0301 2406 4000 1b00 1000  KWDB....$.@.....
                      ^00 Signature
                                ^04 Always 0x0100?
                                     ^06 Always 0x0103?
                                          ^08 Count of main index
                                               ^0a Size of main index entry
                                                    ^0c Count of TCON index
                                                         ^0e Size of TCON index entry

The short int at offset 0x10 is the number of entries in the TPE1 (Performer) index.<br>
The short int at offset 0x12 is the size of entries in the TPE1 (Performer) index.<br>
The short int at offset 0x14 is the number of entries in the TALB (Album) index.<br>
The short int at offset 0x16 is the size of entries in the TALB (Album) index.<br>
The short int at offset 0x18 is the number of entries in the Playlist index.<br>
The short int at offset 0x1a is the size of entries in the Playlist index.<br>
The short int at offset 0x1c is always 0x0001.<br>
The short int at offset 0x1e is always 0x0014.

    1.xxd:0000010:    0200 1000 0200 1000 0100 1000 0100 1400  ................
    2.xxd:0000010:    0200 1000 0200 1000 0100 1000 0100 1400  ................
    3.xxd:0000010:    0300 1000 0300 1000 0200 1000 0100 1400  ................
    4.xxd:0000010:    0400 1000 0400 1000 0300 1000 0100 1400  ................
    5.xxd:0000010:    0400 1000 0400 1000 0300 1000 0100 1400  ................
    6.xxd:0000010:    0500 1000 0500 1000 0300 1000 0100 1400  ................
    many.xxd:0000010: 5300 1000 7f00 1000 5f00 1000 0100 1400  S......._.......
                      ^10 Count of TPE1 index
                           ^12 Size of TPE1 index entry
                                ^14 Count of TALB index
                                     ^16 Size of TALB index entry
                                          ^18 Count of Playlist index
                                               ^1a Size of Playlist index entry
                                                    ^1c Count of unknown 9 (always 0x0001)
                                                         ^1e Size of unknown 9 (always 0x0014)

Unknown. Constant across all files analysed.

    1.xxd:0000020:    0100 0200 0000 0000 0100 0200 0000 0000  ................
    2.xxd:0000020:    0100 0200 0000 0000 0100 0200 0000 0000  ................
    3.xxd:0000020:    0100 0200 0000 0000 0100 0200 0000 0000  ................
    4.xxd:0000020:    0100 0200 0000 0000 0100 0200 0000 0000  ................
    5.xxd:0000020:    0100 0200 0000 0000 0100 0200 0000 0000  ................
    6.xxd:0000020:    0100 0200 0000 0000 0100 0200 0000 0000  ................
    many.xxd:0000020: 0100 0200 0000 0000 0100 0200 0000 0000  ................
                      ^20 Count of unknown 10?
                           ^22 Size unknown 10?

Unknown. Constant across all files analysed.

    1.xxd:0000030:    0000 0600 0400 0000 0000 0000 0000 0000  ................
    2.xxd:0000030:    0000 0600 0400 0000 0000 0000 0000 0000  ................
    3.xxd:0000030:    0000 0600 0400 0000 0000 0000 0000 0000  ................
    4.xxd:0000030:    0000 0600 0400 0000 0000 0000 0000 0000  ................
    5.xxd:0000030:    0000 0600 0400 0000 0000 0000 0000 0000  ................
    6.xxd:0000030:    0000 0600 0400 0000 0000 0000 0000 0000  ................
    many.xxd:0000030: 0000 0600 0400 0000 0000 0000 0000 0000  ................

The int at offset 0x40 is the offset to the main index.<br>
The int at offset 0x44 is the offset to the title table.<br>
The int at offset 0x48 is the offset to the short directory table.<br>
The int at offset 0x4c is the offset to the short file table.

_The short directory and short file tables hold the 8.3 format DOS FAT directory and file names._

    1.xxd:0000040:    c000 0000 0001 0000 7401 0000 8801 0000  ........t.......
    2.xxd:0000040:    c000 0000 4001 0000 1002 0000 2402 0000  ....@.......$...
    3.xxd:0000040:    c000 0000 8001 0000 8002 0000 a802 0000  ................
    4.xxd:0000040:    c000 0000 c001 0000 d602 0000 1003 0000  ................
    5.xxd:0000040:    c000 0000 0002 0000 4803 0000 8203 0000  ........H.......
    6.xxd:0000040:    c000 0000 4002 0000 bc03 0000 f803 0000  ....@...........
    many.xxd:0000040: c000 0000 c089 0100 5ccf 0200 a3d6 0200  ........\.......
                      ^40 Start of main index
                                ^44 Start of title table
                                          ^48 Start of short directory table
                                                    ^4c Start of short file table

The int at offset 0x50 is the offset to the long directory table.<br>
The int at offset 0x54 is the offset to the long file table.<br>
The int at offset 0x58 is the offset to a list of alphabetically ordered titles.<br>
The int at offset 0x5c is the offset to the Genre (TCON) index.

_The long directory and long file tables hold the VFAT directory and file names._

    1.xxd:0000050:    9501 0000 bd01 0000 f501 0000 f701 0000  ................
    2.xxd:0000050:    3e02 0000 6602 0000 d602 0000 da02 0000  >...f...........
    3.xxd:0000050:    cf02 0000 2103 0000 cb03 0000 d103 0000  ....!...........
    4.xxd:0000050:    4403 0000 ca03 0000 9804 0000 a004 0000  D...............
    5.xxd:0000050:    c303 0000 4904 0000 5705 0000 6105 0000  ....I...W...a...
    6.xxd:0000050:    4604 0000 d004 0000 2006 0000 2c06 0000  F....... ...,...
    many.xxd:0000050: 0825 0300 f03d 0300 d061 0400 186e 0400  .%...=...a...n..
                      ^50 Start of long directory table
                                ^54 Start of long file table
                                          ^58 Start of Alphabetically-Ordered-Title List
                                                    ^5c Start of TCON index

The int at offset 0x60 is the offset to the Genre (TCON) name table.<br>
The int at offset 0x64 is the offset to the Genre (TCON) title table.<br>
The int at offset 0x68 is the offset to a list of Genre ordered titles.<br>
The int at offset 0x6c is the offset to the Performer (TPE1) index.

    1.xxd:0000060:    1702 0000 2902 0000 2b02 0000 2d02 0000  ....)...+...-...
    2.xxd:0000060:    fa02 0000 0c03 0000 1003 0000 1403 0000  ................
    3.xxd:0000060:    f103 0000 0304 0000 0904 0000 0f04 0000  ................
    4.xxd:0000060:    d004 0000 fa04 0000 0205 0000 0a05 0000  ................
    5.xxd:0000060:    9105 0000 bb05 0000 c505 0000 cf05 0000  ................
    6.xxd:0000060:    5c06 0000 8606 0000 9206 0000 9e06 0000  \...............
    many.xxd:0000060: c86f 0400 a271 0400 ea7d 0400 328a 0400  .o...q...}..2...
                      ^60 Start of TCON name table
                                ^64 Start of TCON title table
                                          ^68 Start of Genre-Ordered-Title List
                                                    ^6c Start of TPE1 index

The int at offset 0x70 is the offset to the Performer (TPE1) name table.<br>
The int at offset 0x74 is the offset to the Performer (TPE1) title table.<br>
The int at offset 0x78 is the offset to a list of Performer ordered titles.<br>
The int at offset 0x7c is the offset to the Album (TALB) index.

    1.xxd:0000070:    4d02 0000 6702 0000 6902 0000 6b02 0000  M...g...i...k...
    2.xxd:0000070:    3403 0000 4e03 0000 5203 0000 5603 0000  4...N...R...V...
    3.xxd:0000070:    3f04 0000 7d04 0000 8304 0000 8904 0000  ?...}...........
    4.xxd:0000070:    4a05 0000 aa05 0000 b205 0000 ba05 0000  J...............
    5.xxd:0000070:    0f06 0000 6f06 0000 7906 0000 8306 0000  ....o...y.......
    6.xxd:0000070:    ee06 0000 9e07 0000 aa07 0000 b607 0000  ................
    many.xxd:0000070: 628f 0400 de98 0400 26a5 0400 6eb1 0400  b.......&...n...
                      ^70 Start of TPE1 name table
                                ^74 Start of TPE1 title table
                                          ^78 Start of Performer-Ordered-Title List
                                                    ^7c Start of TALB index

The int at offset 0x80 is the offset to the Album (TALB) name table.<br>
The int at offset 0x84 is the offset to the Album (TALB) title table.<br>
The int at offset 0x88 is the offset to a list of Album ordered titles.<br>
The int at offset 0x8c is the offset to an unknown table.

    1.xxd:0000080:    8b02 0000 9f02 0000 a302 0000 0000 0000  ................
    2.xxd:0000080:    7603 0000 8a03 0000 9203 0000 0000 0000  v...............
    3.xxd:0000080:    b904 0000 e104 0000 ed04 0000 0000 0000  ................
    4.xxd:0000080:    fa05 0000 3006 0000 4006 0000 0000 0000  ....0...@.......
    5.xxd:0000080:    c306 0000 f906 0000 0d07 0000 0000 0000  ................
    6.xxd:0000080:    0608 0000 7a08 0000 9208 0000 0000 0000  ....z...........
    many.xxd:0000080: 5eb9 0400 a6cc 0400 36e5 0400 0000 0000  ^.......6.......
                      ^80 Start of TALB name table
                                ^84 Start of TALB title table
                                          ^88 Start of Album-Ordered-Title List
                                                    ^8c Start of unknown (0x00000000)

The int at offset 0x90 is the offset to the playlist index.<br>
The int at offset 0x94 is the offset to the playlist name table.<br>
The int at offset 0x98 is the offset to the playlist title table.<br>
The int at offset 0x9c is the offset to an unknown table.

    1.xxd:0000090:    a502 0000 b502 0000 c702 0000 c902 0000  ................
    2.xxd:0000090:    9603 0000 a603 0000 b803 0000 bc03 0000  ................
    3.xxd:0000090:    f304 0000 1305 0000 3905 0000 3f05 0000  ........9...?...
    4.xxd:0000090:    4806 0000 7806 0000 ac06 0000 b406 0000  H...x...........
    5.xxd:0000090:    1707 0000 4707 0000 7b07 0000 8507 0000  ....G...{.......
    6.xxd:0000090:    9e08 0000 ce08 0000 0209 0000 0c09 0000  ................
    many.xxd:0000090: 7ef1 0400 6ef7 0400 9e04 0500 e010 0500  ~...n...........
                      ^90 Start of playlist index
                                ^94 Start of playlist name table
                                          ^98 Start of playlist title table
                                                    ^9c Start of unknown 9

The int at offset 0xa0 is the offset to an unknown table.<br>
The int at offset 0xa4 is the offset to an unknown table.<br>
The int at offset 0xa8 is the offset to an unknown table.<br>
The int at offset 0xac is the offset to an unknown table.

    1.xxd:00000a0:    dd02 0000 df02 0000 e702 0000 eb02 0000  ................
    2.xxd:00000a0:    d003 0000 d203 0000 da03 0000 e203 0000  ................
    3.xxd:00000a0:    5305 0000 5505 0000 6105 0000 6d05 0000  S...U...a...m...
    4.xxd:00000a0:    c806 0000 ca06 0000 da06 0000 ea06 0000  ................
    5.xxd:00000a0:    9907 0000 9b07 0000 ab07 0000 bf07 0000  ................
    6.xxd:00000a0:    2009 0000 2209 0000 3609 0000 4e09 0000   ..."...6...N...
    many.xxd:00000a0: f410 0500 f610 0500 f212 0500 822b 0500  .............+..
                      ^a0 Start of unknown 10
                                ^a4 Start of unknown 11
                                          ^a8 Start of unknown 12
                                                    ^ac Start of Sub-indices

Unknown, seems always to be a row of 0x00.

    1.xxd:00000b0:    0000 0000 0000 0000 0000 0000 0000 0000  ................
    2.xxd:00000b0:    0000 0000 0000 0000 0000 0000 0000 0000  ................
    3.xxd:00000b0:    0000 0000 0000 0000 0000 0000 0000 0000  ................
    4.xxd:00000b0:    0000 0000 0000 0000 0000 0000 0000 0000  ................
    5.xxd:00000b0:    0000 0000 0000 0000 0000 0000 0000 0000  ................
    6.xxd:00000b0:    0000 0000 0000 0000 0000 0000 0000 0000  ................
    many.xxd:00000b0: 0000 0000 0000 0000 0000 0000 0000 0000  ................

### The Main Index

The Main Index consists of an array (length given at offset 0x08) of entries. Each entry is 64 bytes long (size given at offset 0x0a).

Offsets shown are from the start of each entry.

The "Genre", "Performer" and "Album" fields indicate the indices into each of the corresponding tables.

The "title length", "shortdir length", "shortfile length", "longdir length" and "longfile length" fields indicate the length of the corresponding strings (inclusive of null terminator).

The "character length" fields indicate whether the corresponding string is ASCII or UTF-16 encoded (1=ASCII, 2=UTF-8).

The "title offset", "shortdir offset", "shortfile offset", "longdir offset", "longfile offset" indicate the offsets from the start of the corresponding tables.

    0000000: 0200 0200 0100 0000 ffff ffff 0000 0080  ................
             ^00 Genre
                  ^02 Performer
                       ^04 Album
                            ^06 Unknown (0x0000)
                                 ^08 Unknown (0xffffffff)
                                           ^0c Unknown (0x80000000)
                                       
    0000010: 0000 0080 7400 0200 0000 0000 1400 0100  ....t...........
             ^10 Unknown (0x80000000)
                       ^14 Title length
                            ^16 Title character length
                                 ^18 Title offset
                                           ^1c Shortdir length
                                                ^1e Shortdir character length
                                            
    0000020: 1400 0000 0d00 0100 2700 0000 2800 0200  ........'...(...
             ^20 Shortdir offset
                       ^24 Shortfile length
                            ^26 Shortfile character length
                                 ^28 Shortfile offset
                                           ^2c Longdir length
                                                ^2e Longdir character length
                                            
    0000030: 3800 0000 3800 0200 a600 0000 0000 0000  8...8...........
             ^30 Longdir offset
                       ^34 Longfile length
                            ^36 Longfile character length
                                 ^38 Longfile offset
                                           ^3c Unknown (0x00000000)

### The Title Table

The Title Table consists of an array of UTF-16 encoded, null terminated strings. These seem to correspond to the TIT2 ID3 v2 tag in the media files.

### The Short Directory Table

The Short Directory Table consists of an array of ASCII encoded, null terminated strings. These are the 8.3 DOS FAT directory names in which the media files appear.

### The Short File Table

The Short File Table consists of an array of ASCII encoded, null terminated strings. These are the 8.3 DOS FAT file names for the media files.

### The Long Directory Table

The Long Directory Table consists of an array of UTF-16 encoded, null terminated strings. These are the VFAT directory names in which the media files appear.

### The Long File Table

The Long File Table consists of an array of UTF-16 encoded, null terminated strings. These are the VFAT file names for the media files.

### Alphabetically-Ordered-Title List

Number short ints consistent with number of titles.

Seems to be a list of titles in alphabetical order.

### The Genre Index

The following shows three entries from a Genre index.

Offsets shown are from the start of each entry.

    0000000: 0200 0200 0000 0000 0000 0000 0000 0000
    0000000: 1800 0200 0200 0000 0000 0300 0000 0000
    0000000: 1000 0200 1a00 0000 0000 0300 0600 0000             
             ^00 Genre name length
                  ^02 Genre character length
                       ^04 Genre name offset
                                 ^08 Unknown
                                      ^0a Number of titles in Genre
                                           ^0c Genre title entry offset
                                                ^0e Unknown

### The Genre Name Table

The Genre Table consists of an array of UTF-16 encoded, null terminated strings. It always starts with an empty string.

### The Genre Title Table

The Genre Title Table consists of indices (short int) pointing to the Main Index to indicate which titles belong to this Genre.

### Genre-Ordered-Title List

Number short ints consistent with number of titles.

Seems to be a list of titles in Genre order.

### The Performer Index

The following shows five entries from a Performer index.

Offsets shown are from the start of each entry.

    0000000: 0200 0200 0000 0000 0000 0000 0000 0000
    0000000: 2200 0200 0200 0000 0000 0200 0000 0000
    0000000: 1800 0200 2400 0000 0000 0200 0400 0000
    0000000: 2400 0200 3c00 0000 0000 0100 0800 0000
    0000000: 5000 0200 6000 0000 0000 0100 0a00 0000            
             ^00 Performer name length
                  ^02 Performer character length
                       ^04 Performer name offset
                                 ^08 Unknown
                                      ^0a Number of titles for Performer
                                           ^0c Performer title entry offset
                                                ^0e Unknown

### The Performer Name Table

The Performer Table consists of an array of UTF-16 encoded, null terminated strings. It always starts with an empty string.

### The Performer Title Table

The Performer Title Table consists of indices (short int) pointing to the Main Index to indicate which titles belong to this _Performer_.

### Performer-Ordered-Title List

Number short ints consistent with number of titles.

Seems to be a list of titles in Performer order.

### The Album Index

The following shows five entries for an Album index.

Offsets shown are from the start of each entry.

    0000000: 0200 0200 0000 0000 0000 0000 0000 0000
    0000000: 1200 0200 0200 0000 0000 0200 0000 0000
    0000000: 1400 0200 1400 0000 0000 0100 0400 0000
    0000000: 0e00 0200 2800 0000 0000 0200 0600 0000
    0000000: 3e00 0200 3600 0000 0000 0100 0a00 0000          
             ^00 Album name length
                  ^02 Album character length
                       ^04 Album name offset
                                 ^08 Unknown
                                      ^0a Number of titles for Album
                                           ^0c Album title entry offset
                                                ^0e Unknown

### The Album Name Table

The Album Name Table consists of an array of UTF-16 encoded, null terminated strings. It always starts with an empty string.

### The Album Title Table

The Album Title Table consists of indices (short int) pointing to the Main Index to indicate which titles belong to this _Album_.

### Album-Ordered-Title List

Number short ints consistent with number of titles.

Seems to be a list of titles in Album order.

### The Playlist Index

The following shows three entries for a playlist index.

The Playlist Index is overwritten by unknown 9 if no playlist is present

Offsets shown are from the start of each entry.

    0000000: 1200 0200 0000 0000 0000 0200 0000 0000
    0000000: 1400 0200 1200 0000 0000 0100 0400 0000
    0000000: 0e00 0200 2600 0000 0000 0200 0600 0000
             ^00 Playlist name length
                  ^02 Playlist character length
                       ^04 Playlist name offset
                                 ^08 Unknown
                                      ^0a Number of titles for playlist
                                           ^0c Playlist title entry offset
                                                ^0e Unknown

### The Playlist Name Table

The Playlist Name Table consists of an array of UTF-16 encoded, null terminated strings.

The Playlist Name Table is overwritten by unknown 9 if no playlist is present.

### Playlist Title Table

The Playlist Title Table consists of indices (short int) pointing to the Main Index to indicate which titles belong to this playlist.

The Playlist Title Table is overwritten by unknown 9 if no playlist is present.

### Unknown 9

10 short ints. Always FFFF FFFF 0000 0000 0002 0002 0000 0000 0000 0000.

### Unknown 10

1 short int (zero value)

### Unknown 11

Number of ints consistent with number of Albums (all zero value).

### Unknown 12

Number of ints consistent with number of titles (all zero value).

### Sub-indices

Sub-indices starts with a relative offset (int) to the start of more tables. This is then followed by a number (always 13) of entries that seem to consist of an absolute offset (int), a size (short int) and a count (short int).

The absolute offset points to another table that either contains "count" short ints (if "size" is 2), or "count" arrays of 4 short ints (if "size" is 8).

#### Sub-indices _Genre_ _Performers_ offsets and counts (0)

This table seems to contain the number of _Performers_ per _Genre_.

The number of entries is the number of _Genres_ minus 1 (_Genre_ 0 is excluded). The format of each entry is four short ints.

The first short int is the _Genre_ number (ascending order).<br>
The second short int is an offset into the next table (_Genre_ _Performer_ _Albums_).<br>
The third short int is the number of _Performers_ in this _Genre_.<br>
The last short int is always 0.

#### Sub-indices _Genre_ _Performer_ _Albums_ offsets and counts (1)

This table seems to contain the number of _Albums_ per _Performer_ per _Genre_.

The first short int is the _Performer_ number. Ascending order within _Genre_.<br>
The second short int is an offset into the next table (_Genre_ _Performer_ _Album_ _Titles_).<br>
The third short int is the number of _Albums_ for that _Performer_ that contain the _Genre_.<br>
The last short int is always 0.

#### Sub-indices _Genre_ _Performer_ _Album_ _Titles_ offsets and counts (2)

This table seems to contain the number of _Titles_ per _Album_ per _Performer_ per _Genre_.

The first short int is the _Album_ number.<br>
The second short int is an offset into the next table (Genre-Ordered-Titles).<br>
The third short int is the number of _Titles_.<br>
The last short int is always zero.

#### Sub-indices Genre-Ordered-Title List (3)

Points to table Genre-Ordered-Title List

#### Sub-indices _Genre_ _Albums_ offsets and counts (4)

This table seems to contain the number of _Albums_ per _Genre_.

The number of entries is the number of _Genres_ minus 1 (_Genre_ 0 is excluded). The format of each entry is four short ints.

The first short int is the _Genre_ number (ascending order).<br>
The second short int is an offset into the next table (_Genre_ _Album_ _Titles_).<br>
The third short int is the number of _Albums_ in this _Genre_.<br>
The last short int is always 0.

#### Sub-indices _Genre_ _Album_ _Titles_ offsets and counts (5)

This table seems to contain the number of _Titles_ per _Album_ per _Genre_.

The first short int is the _Album_ number.<br>
The second short int is an offset into the next table (_Genre_ _Titles_).<br>
The third short int is the number of _Titles_ for that _Album_ that contain the _Genre_.<br>
The last short int is always 0.

#### Sub-indices _Genre_ _Titles_ (6)

Points to the _Genre_ _Title_ table.

#### Sub-indices _Performer_ _Albums_ offsets and counts (7)

This table seems to contain the number of _Albums_ per _Performer_.

The number of entries is the number of _Performers_ minus 1 (_Performer_ 0 is excluded). The format of each entry is four short ints.

The first short int is the _Performer_ number (ascending order).<br>
The second short int is an offset into the next table (_Performer_ _Album_ _Titles_).<br>
The third short int is the number of _Albums_ for this _Performer_.<br>
The last short int is always 0.

#### Sub-indices _Performer_ _Album_ _Titles_ offsets and counts (8)

This table seems to contain the number of _Titles_ per _Album_ per _Performer_.

The first short int is the _Album_ number.<br>
The second short int is an offset into the next table (_Performer_ _Titles_).<br>
The third short int is the number of _Titles_ for the _Album_ for the _Performer_.<br>
The last short int is always 0.

#### Sub-indices _Performer_ _Titles_ (9)

Points to the _Performer_ _Title_ table.

#### Sub-indices _Genre_ _Performers_ offsets and counts (10)

This table seems to contain the number of _Performers_ per _Genre_. As such, it is the same as Sub-indices Table 0.

The first short int is the _Genre_ number.<br>
The second short int is an offset into the next table (_Genre_ _Performer_ _Titles_).<br>
The third short int is the number of _Performers_ for this _Genre_.<br>
The last short int is always 0.

#### Sub-indices _Genre_ _Performer_ _Titles_ offsets and counts (11)

The first short int is the _Performer_ number.<br>
The second short int is an offset into the next table (Genre-Ordered-Titles).<br>
The third short int is the number of _Titles_ for the _Performer_ for the _Genre_.<br>
The last short int is always 0.

#### Sub-indices Genre-Ordered-Titles (12)

Points to table Genre-Ordered-Title List

