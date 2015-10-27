#!/usr/bin/python3
# encoding: utf-8
'''
A parser for the output from mdir -s.

This is necessary, because there is no obvious way to get the 8.3 DOS filenames from a
vfat volume mounted under Linux.

I currently see no maintained Python library to access the vfat volume directly, and this
would necessitate root privileges anyway. Rather than write my own, and have the program
installed as suid root, I've chosen to use the mtools suite instead.

This is a hack, but an expedient one.

Directory listings start with a line stating the directory name, then a blank line. The directory listing
ends with a line stating the total number of files, and another blank line.
'''

DIRECTORY_ENTRY_DESIGNATOR = "<DIR>"
START_DIRECTORY_ENTRY = 13
END_DIRECTORY_ENTRY = 18

CURRENT_DIR_ENTRY_DESIGNATOR = "Directory for "
START_CURRENT_DIR_ENTRY = 0
END_CURRENT_DIR_ENTRY = 14

START_FILE_DIR_NAME = 0
END_FILE_DIR_NAME = 8

START_FILE_DIR_EXT = 9
END_FILE_DIR_EXT = 12

START_LONG_NAME = 42

class MdirParser(object):
    def __init__(self, mdir_outfile):
        '''
        Parse the mdir -s output contained in mdir_output.
        Results are held in self.paths which is a map of directory name.
        '''

        found_dir = False

        self.paths = {}

        mdir_output = open(mdir_outfile, "r")

        for line in mdir_output:
            if line[START_CURRENT_DIR_ENTRY:END_CURRENT_DIR_ENTRY] == CURRENT_DIR_ENTRY_DESIGNATOR:
                curdirname = line[END_CURRENT_DIR_ENTRY:].strip().split(":")[1]
                # add a slash if needed
                if curdirname[-1:] != "/":
                    curdirname = curdirname + "/"
                # print ("\nCurrent directory: {}".format(curdirname))
                if curdirname not in self.paths:
                    self.paths[curdirname] = (curdirname, {})
                found_dir = True
            elif found_dir:
                if line[START_DIRECTORY_ENTRY:END_DIRECTORY_ENTRY] == DIRECTORY_ENTRY_DESIGNATOR:
                    # ignore current and parent entries
                    if line[:1] != ".":
                        dirname = line[START_FILE_DIR_NAME:END_FILE_DIR_NAME].strip()
                        dirext = line[START_FILE_DIR_EXT:END_FILE_DIR_EXT].strip()
                        longdirname = line[START_LONG_NAME:].strip() + "/"
                        if len(dirext) == 0:
                            completedirname = dirname + "/"
                        else:
                            completedirname = dirname + "." + dirext + "/"
                        # if there's no long name, make one
                        if len(longdirname) == 1:
                            longdirname = completedirname
                        # print ("Directory entry: {}.{} :{}:".format(dirname, dirext, longdirname))
                        # print ("\t{}{}".format(curdirname, longdirname))
                        self.paths[curdirname+longdirname] = (self.paths[curdirname][0]+completedirname, {})
                elif line[10:15] == "files":
                    # ignore totals line
                    pass
                elif len(line) == 1:
                    # ignore empty line
                    pass
                elif line[:19] == "Total files listed:":
                    found_dir = False
                else:
                    filename = line[START_FILE_DIR_NAME:END_FILE_DIR_NAME].strip()
                    fileext = line[START_FILE_DIR_EXT:END_FILE_DIR_EXT].strip()
                    longfilename = line[START_LONG_NAME:].strip()
                    if len(fileext) == 0:
                        completefilename = filename
                    else:
                        completefilename = filename + "." + fileext
                    # if there's no long name, make one
                    if len(longfilename) == 0:
                        longfilename = completefilename
                    # print ("File: {}.{} :{}:".format(filename, fileext, longfilename))
                    self.paths[curdirname][1][longfilename] = completefilename
                    # split_line = line.split()
                    # if len(split_line) > 0:
                    #     print (split_line[0], split_line[1])

        mdir_output.close()

    def short_directory_name(self, dirname):
        return self.paths[dirname][0]

    def short_file_name(self, dirname, filename):
        return self.paths[dirname][1][filename]

if __name__ == "__main__":
    mp = MdirParser("/tmp/kwdb.tmp")

    print ("\nPaths\n")
    for e in mp.paths:
        print (e, mp.paths[e][0])
        for f in mp.paths[e][1]:
            print ("\t{} {}".format(f, mp.paths[e][1][f]))

    # print(mp.short_directory_name("/Podcasts/Wood Talk – Woodworking Podcast/"))
    # print(mp.short_file_name("/Podcasts/Wood Talk – Woodworking Podcast/", "WoodTalkOnline5.mp3"))
