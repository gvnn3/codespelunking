#!env python
#
#  Purpose: Collect all the actions that preceed a code spelunking
#  session into a single script file.  Note, this script MUST be
#  executed from the root of where you wish to work.  This script can
#  take many minutes if executed over a large code base, for example
#  starting it in FreeBSD's /usr/src directory.

# Use option parsing.  Right now we have one option, which is whether
# or not we're looking at a kernel code base.  This is important to
# cscope because it will normally use /usr/include unless the -k
# (kernel) option is used.

# Redefine these to find the correct programs

cscope="/opt/homebrew/bin/cscope"
gtags="/opt/homebrew/bin/gtags"
htags="/opt/homebrew/bin/htags"
doxygen="/opt/homebrew/bin/doxygen"

import sys
import os

def main():

    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-k", "--kernel",
                      action="store_true", dest="kernel", default=False,
                      help="kernel code, do not use /usr/include with cscope")
    parser.add_option("-d", "--doxygen",
                      action="store_true", dest="doxygen", default=False,
                      help="build doxygen output")
    parser.add_option("-c", "--cscope",
                      action="store_true", dest="cscope", default=False,
                      help="generate cscope database")
    parser.add_option("-w", "--web",
                      action="store_true", dest="web", default=False,
                      help="build web pages as well")
    parser.add_option("-t", "--title",
                      dest="title", default=None,
                      help="title to give to web pages")
    
    (options, args) = parser.parse_args()
    
    # Execute Doxygen, cscope and then gtags/htags.
    # We use this ordering because if you select Doxygen but have no
    # Doxyfile then we want to bail early and force you to update the
    # Doxyfile before re-executing.

    if (options.doxygen == True):
        if (not os.path.exists("Doxyfile")):
            exit_status = os.spawnlp(os.P_WAIT, doxygen, 'doxygen', '-g')
            print("doxygen option selected but no DoxyFile")
            if (os.path.exists("Doxyfile")):
                print("Doxyfile created.  Please update Doxyfile and re-run either %s or run doxygen directly" % sys.argv[0])
            sys.exit(1)
        else:
            exit_status = os.spawnlp(os.P_WAIT, doxygen, 'doxygen', 'Doxyfile')
            if (exit_status == 0):
                print("doxygen complete")
            else:
                print("doxygen failed")
                sys.exit(1)
            
    if (options.cscope == True):
        if (options.kernel == True):
            exit_status = os.spawnlp(os.P_WAIT, cscope, 'cscope', '-R', '-q', '-b', '-k')
        else:
            exit_status = os.spawnlp(os.P_WAIT, cscope, 'cscope', '-R', '-q', '-b')
        if (exit_status == 0):
            print("cscope complete")
        else:
            print("cscope failed")
            sys.exit(1)

    exit_status = os.spawnlp(os.P_WAIT, gtags, 'gtags')

    if (exit_status == 0):
        print("gtags complete")
    else:
        print("gtags failed")
        sys.exit(1)

    if (options.web == True):
        if (options.title != None):
            exit_status = os.spawnlp(os.P_WAIT, htags, 'htags', 
                                     '--line-number', '--symbol',
                                     '--title', options.title)
        else:
            exit_status = os.spawnlp(os.P_WAIT, htags, 'htags',
                                 '--line-number', '--symbol')
        if (exit_status == 0):
            print("htags complete")
        else:
            print("htags failed")
            sys.exit(1)

    print("ready to spelunk")

# Call the main function.
main()
