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

Current limitations:

* processes mp3 and wma only at this stage (wma not tested)
* include and exclude regular expression parsing not currently implemented
* playlists not currently implemented
* international characters are sorted out of order, so "Bäpa" comes after "By The Hand Of My Father" rather than after "Banks of Newfoundland"

## Parser
To parse a database, just type:

```bash
    ./KenwoodDBReader.py -i /path/to/kenwood.dap/file
```

It will print copious logs, used by me to analyse the database. I may ask for this output if you want me to look into a problem.
