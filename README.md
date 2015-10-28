#kmel_db

A parser and generator for Kenwood Music Editor Light databases.

At this time, only the parser (decoder) works.

The kmel_db_format.md document attempts to explain the format of the database.

The KenwoodDBReader.py program attempts to decode (and print to stdout) a file called kenwood.dap (by default, or any other file given with a -i option). Unexpected values are printed to stderr.
