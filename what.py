#!/usr/bin/env python
#
# Copyright (c) 2005-2024, Neville-Neil Consulting
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# Neither the name of Neville-Neil Consulting nor the names of its 
# contributors may be used to endorse or promote products derived from 
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Author: George V. Neville-Neil

#
# Description: This python script will recursively descend a source
# tree and print out several relevant statistics



"""This script is  meant to be run the first time  you encounter a new
source base.  It recursively descends  a file tree and reports several
statistics of interest to code spelunkers.  These include:

- The total number of directories that contain code
- The total number of files in all directories.
- The total number of files in each of the following programming
  languages: Awk, C, C++, HTML, IDL, Java, Perl, PHP, Java, Python, TCL

The code that determines what computer language a file contains is
flexible in how it does its checking.  Right now this is done based on
the file's extension, but can be extended to call an interpreter to
determine if the file is valid code of a particular type.

There are two arguments that can be used.

The -w or --where argument tells the program that for each type of
code it is to list all the directories that contain that type of code.

The -e or --exclude argument excludes certain sub-directories from the
search.  The exclude argument can be used several times on the same
line like this:

The -l or --language option says to only find one language, and not
all of them.

The -p or --pretty option allows the user to select HTML or LaTeX
table output format instead of plain text.

what.py -e HTML -e DoxyFiles

The program automatically ignores any file in a CVS diretory.
"""

import os
from os import F_OK

# This is the file extension mapping code.  Change this array if you
# wish to change the determination of the files.  The format is "key",
# "value" in which the key is the extension and the value is the file
# type.  Both the key and value are strings.
def filetype(name):

    file_ext_map = { "awk" : "AWK",
                     "py" : "Python",
                     "pyl" : "Python",
                     "el" : "Emacs Lisp",
                     "elc" : "Emacs Lisp",
		     "h" : "C or C++ Header Files",
                     "c" : "C",
                     "cc" : "C++",
                     "cpp" : "C++",
                     "c++" : "C++",
                     "m" : "Objective C",
                     "tcl" : "TCL",
                     "html" : "HTML",
                     "htm" : "HTML",
                     "java" : "Java",
                     "idl" : "Interface Definition Language",
                     "xml" : "XML",
                     "xsl" : "XML",
                     "php" : "PHP",
                     "inc" : "PHP include",
                     "sh" : "Shell Script",
                     "ksh" : "Shell Script",
                     "bash" : "Shell Script",
                     "csh" : "Shell Script",
                     "tcsh" : "Shell Script",
                     "mk" : "Makefile",
                     "am" : "Automake",
                     "m4" : "M4"
                     }
  
    (root, extension) = os.path.splitext(name)

    # Special case the search for Makefiles as these are important but
    # do not have an extension
    if (len(extension) <= 0):
        if (root == "Makefile"):
            return "Makefile"
        else:
            if (root == "configure"):
                return "Autoconf"
            else:
                return "Unknown"

    # According to the rules if we have an extension then it ALWAYS has
    # a . at the beginning.  Strip that .

    extension = extension[1:len(extension)]
    if (extension not in file_ext_map):
        return "Unknown"

    return file_ext_map[extension]

# Find out how many lines are in a file.
# We know that "name" is a file because it was passed to us by
# os.walk() in main().

def filelines(name):
    try:
        file = open(name)
    except:
        return -1
    try:
        lines = file.readlines()
    except:
        lines = ""
    file.close()
    return len(lines)

def main():

    file_map = {} # The map of file type to the number that exist.
    size_map = {} # The map of file type to the number of lines.
    location_map = {} # A map of the file type to a list of directories
    dir_num = 0 # How many directories are there?
    exclude_list = [] # List of directories to exclude, can be empty
    
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-w", "--where",
                      action="store_true", dest="where", default=False,
                      help="Print where files are located")
    parser.add_option("-e", "--exclude", action="append", type="string",
                      dest="exclude_list", help="Directories to exclude")
    parser.add_option("-l", "--language", action="store", type="string",
                      dest="language",
                      help="Find only code of a particular language")
    parser.add_option("-p", "--pretty", action="store", type="string",
                      dest="pretty",
                      help="Pretty print in HTML or LaTeX table format")
    
    (options, args) = parser.parse_args()

    where = options.where
    exclude_list = options.exclude_list
    language = options.language
    pretty = options.pretty

    for root, dirs, files in os.walk("."):
        if 'CVS' in dirs:
            dirs.remove('CVS')  # don't visit CVS directories

        if exclude_list:
            for dir in exclude_list:
                if dir in dirs:
                    dirs.remove(dir)

        for name in files:
            fullname = os.path.join(root, name)
            if not os.access(fullname, F_OK):
                continue
            type = filetype(fullname)

            if (language and (type != language)):
                continue

            if type not in file_map:
                file_map[type] = 1
            else:
                file_map[type] += 1
            lines = filelines(fullname)

            if lines == -1:
                continue

            if type not in size_map:
                size_map[type] = lines
            else:
                size_map[type] += lines

            if type == "Unknown":
                continue
            
            if type not in location_map:
                location_map[type] = {root : 1}
                dir_num += 1
                continue

            if root not in location_map[type]:
                location_map[type][root] = 1
                dir_num += 1
                continue
            
            location_map[type][root] += 1
            dir_num += 1
            
    # Now do our fancy printing
    if (pretty == "HTML"):
        print("<table><tr><td>Type</td><td>Number</td><td>Lines</td></tr>")
    elif (pretty == "LaTeX"):
        print("\\begin{tabular}{|l|l|c|}\n\\hline\nType & Number & Lines\\\\\n\\hline")
    else:
        print("Type\t\tNumber\t\tLines")

    types = file_map.keys()

    total_files = 0
    total_lines = 0

    for key in types:
        if key == "Unknown":
            continue
        total_files += file_map[key]
        total_lines += size_map[key]

        if (pretty == "HTML"):
            print("<tr><td>%s</td><td>%d</td><td>%d</td></tr>") % \
                  (key, file_map[key], size_map[key])
        elif (pretty == "LaTeX"):
            print(key, "&", file_map[key], "& \\\\", size_map[key])
        else:
            print(key, "\t\t", file_map[key], "\t\t", size_map[key])
        
        if (where == True):
            dirs = location_map[key].keys()
            dirs.sort()
            for dir in dirs:
                if (pretty == "HTML"):
                    print ("<tr><td>%s</td><td>%d</td></tr>") % \
                          (dir, location_map[key][dir])
                elif (pretty == "LaTeX"):
                    print("%s&%d\\\\" % (dir, location_map[key][dir]))
                else:
                    print("\t%s\t%d" % (dir, location_map[key][dir]))

    if (pretty == "HTML"):
        print("</table><br>")
        print("<table>")
        print("<tr><td></td><td>Files</td><td>Lines</td></tr>")
        print("<tr><td>Identified Code</td><td>%d</td><td>%d</td></tr>") % \
              (total_files, total_lines)
    elif (pretty == "LaTeX"):
        print("\\hline \\hline\n&Files & Lines\\\\")
        print("Identified Code & %d & %d\\\\") % (total_files, total_lines)
    else:
        print("\n\t\t\tFiles\tLines")
        print("Identified Code\t\t", total_files, "\t", total_lines, "\n")

    if "Unknown" in file_map.keys() and "Unknown" in size_map.keys():
        if (pretty == "HTML"):
            print("<tr><td>Unknown</td><td>%d</td><td>%d</td></tr>") % \
                  (file_map["Unknown"], size_map["Unknown"])
        elif (pretty == "LaTeX"):
            print("Unknown & %d & %d\\\\\n\\hline") % \
                  (file_map["Unknown"], size_map["Unknown"])
        else:
            print("Unknown\t\t\t", file_map["Unknown"], "\t", size_map["Unknown"], "\n")
        total_files += file_map["Unknown"]
        total_lines += size_map["Unknown"]

    if (pretty == "HTML"):
        print("<tr><td>Total</td><td>%d</td><td>%d</td></tr>") % \
              (total_files, total_lines)
    elif (pretty == "LaTeX"):
        print("Total & %d & %d\\\\\\hline") % (total_files, total_lines)        
    else:
        print("Total\t\t\t", total_files, "\t", total_lines, "\n")

    if (where == True):
        if (pretty == "HTML"):
            print("<tr><td>Number of directories</td><td>%d</td></tr>") % \
                  dir_num
        elif (pretty == "LaTeX"):
            print("Number of directories & %d") % dir_num
        else:
            print("Number of directories\t%d") % dir_num

    if (pretty == "HTML"):
        print("</table>")
    elif (pretty == "LaTeX"):
        print("\\end{tabular}")
        
main()        
