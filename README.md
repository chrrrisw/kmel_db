#kmel_db

A parser and generator for Kenwood Music Editor Light databases.

## Database format
The kmel_db_format.md document attempts to explain the format of the database. It might be slightly behind the code.

## Generator
To generate a database, just type:

```bash
    ./DapGen.py /path/to/your/usb/drive
```

If you don't specify the path, the generator will process all mounted partitions of type FAT.

Use the '-h' option to see other options.

Current limitations
    - processes mp3 and wma only at this stage (wma not tested)
    - include and exclude regular expression parsing not currently implemented
    - playlists not currently implemented

## Parser
The KenwoodDBReader.py program attempts to decode (and print to stdout) a file called kenwood.dap (by default, or any other file given with a -i option). Unexpected values are printed to stderr. Use the '-h' option to see options.
