#!/usr/bin/python3
# encoding: utf-8
"""
A parser for the output from mdir -s.

This is necessary, because there is no obvious way to get the 8.3 DOS filenames from a
vfat volume mounted under Linux.

I currently see no maintained Python library to access the vfat volume directly, and this
would necessitate root privileges anyway. Rather than write my own, and have the program
installed as suid root, I've chosen to use the mtools suite instead.

This is a hack, but an expedient one.

Directory listings start with a line stating the directory name, then a blank line. The directory listing
ends with a line stating the total number of files, and another blank line.
"""

# The regex for the start of a directory
CURRENT_DIR_ENTRY_START = "Directory for "
DIRECTORY_ENTRY = "<DIR>"

mdir_output = open("/tmp/kwdb.tmp", "r")

found_dir = False

paths = {}

for line in mdir_output:
    if line[:14] == CURRENT_DIR_ENTRY_START:
        curdirname = line[14:].strip().split(":")[1]
        # add a slask if needed
        if curdirname[-1:] != "/":
            curdirname = curdirname + "/"
        print ("\nCurrent directory: {}".format(curdirname))
        if curdirname not in paths:
            paths[curdirname] = (curdirname, {})
        found_dir = True
    elif found_dir:
        if line[13:18] == DIRECTORY_ENTRY:
            # ignore current and parent entries
            if line[:1] != ".":
                dirname = line[:8].strip()
                dirext = line[9:12].strip()
                longdirname = line[42:].strip() + "/"
                if len(dirext) == 0:
                    completedirname = dirname + "/"
                else:
                    completedirname = dirname + "." + dirext + "/"
                # if there's no long name, make one
                if len(longdirname) == 1:
                    longdirname = completedirname
                print ("Directory entry: {}.{} :{}:".format(dirname, dirext, longdirname))
                print ("\t{}{}".format(curdirname, longdirname))
                paths[curdirname+longdirname] = (paths[curdirname][0]+completedirname, {})
        elif line[10:15] == "files":
            # ignore totals line
            pass
        elif len(line) == 1:
            # ignore empty line
            pass
        elif line[:19] == "Total files listed:":
            found_dir = False
        else:
            filename = line[:8].strip()
            fileext = line[9:12].strip()
            longfilename = line[42:].strip()
            if len(fileext) == 0:
                completefilename = filename
            else:
                completefilename = filename + "." + fileext
            # if there's no long name, make one
            if len(longfilename) == 0:
                longfilename = completefilename
            print ("File: {}.{} :{}:".format(filename, fileext, longfilename))
            paths[curdirname][1][longfilename] = completefilename
            #split_line = line.split()
            #if len(split_line) > 0:
            #    print (split_line[0], split_line[1])

print ("\nPaths\n")
for e in paths:
    print (e, paths[e][0])
    for f in paths[e][1]:
        print ("\t{} {}".format(f, paths[e][1][f]))
