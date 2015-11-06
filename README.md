#kmel_db

A parser and generator for Kenwood Music Editor Light databases that works under Linux. The database is used by Kenwood car audio systems to allow searching by album, title, genre and artist. It also allows creation of playlists.

My Kenwood stereo only supports mp3 and wma media formats, so this is currently the default for this application.

You'll need Python version 3 or above, and the [hsaudiotag3k](https://pypi.python.org/pypi/hsaudiotag3k) python package installed to run.

## Database format
The kmel_db_format.md document attempts to explain the format of the database. It might be slightly behind the code.

## Generator
To generate a database, just type:

```bash
    ./DapGen.py /path/to/your/usb/drive
```

If you don't specify the path, the generator will process all mounted partitions of type FAT.

Use the '-h' option to see other options.

Current limitations:

* processes mp3 and wma only at this stage (wma not tested)
* include and exclude regular expression parsing for media types not currently implemented
* processes pls playlists only at this stage
* international characters are sorted out of order, so "Bäpa" comes after "By The Hand Of My Father" rather than after "Banks of Newfoundland"

## Parser
To parse a database, just type:

```bash
    ./KenwoodDBReader.py -i /path/to/kenwood.dap/file
```

It will print copious logs, used by me to analyse the database. I may ask for this output if you want me to look into a problem.
