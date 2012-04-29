#!/usr/bin/python
# duplus -- disk usage plus in Python

import os
import sys
import operator
import filesize

ARG_HELP = ['--help', '-?', '-help', '-h']
ARG_NOHIDDEN = '-nh'
ARG_FROMSIZE = '-frm'


USAGE = """Usage: python duplus.py [options] [directory=HOME_DIR]
Example: 
    python duplus.py -nh -frm20.12m ~/Desktop
Available ptions:
    -nh : Ignore hidden files/directories.
    -frmXX : Only show the files/directoies from a minimum size. 'XX' stands for the size, e.g. 20k.
Note:
    If the 'directory' is not given, HOME_DIR will be the target.
For the latest version, please see:
<URL:https://github.com/hufyhang/Duplus>"""

def duplus(path=os.getenv('HOME'), fromSize='0B', nohidden=False):
    sortPrint(iterateDict(path, nohidden), filesize.bytes(fromSize))

def iterateDict(path, nohidden=False):
    """iterate through a given path and return a path-size-type list"""
    if os.path.exists(path) is False:
        print 'Error: Directory does not exist.'
        sys.exit(0)

    listing = os.listdir(path)
    resultList = []
    for item in listing:
        if item == '.' or item == '..':
            continue
        if nohidden == True:
            if item[0] == '.':
                continue
        ipath = os.path.join(path, item)
        if os.path.isfile(ipath):
            resultList.append([item, os.path.getsize(ipath), 'f'])
        elif os.path.isdir(ipath):
            resultList.append([item, calcFolderSize(ipath), 'd'])
    return resultList

def sortPrint(list, fromBytes):
    items = sorted(list, key=operator.itemgetter(1), reverse=True)
    total = 0;
    for item in items:
        total += item[1]
    print 'Total: %s' % filesize.size(total)
    for item in items:
        if item[1] < fromBytes:
            continue
        print '%-5s <%s> ......... %-10s' % (filesize.size(item[1]), item[2], item[0])

def calcFolderSize(path):
    """Calculate and return size of a given path"""
    total = os.path.getsize(path)
    for item in os.listdir(path):
        ipath = os.path.join(path, item)
        if os.path.isfile(ipath):
            total += os.path.getsize(ipath)
        elif os.path.isdir(ipath):
            total += calcFolderSize(ipath)
    return total


if __name__ == '__main__':
    flag, nh = False, False
    frm = '0B'
    for arg in sys.argv:
        # firstly, check if usage info is needed
        if arg in ARG_HELP:
            print USAGE
            sys.exit(0)
        elif arg == ARG_NOHIDDEN:
            nh = True
            flag = True
        elif ARG_FROMSIZE in arg:
            frm = arg.replace(ARG_FROMSIZE, '')
            if len(frm) == 0:
                frm = '0B'

    lastArg = sys.argv[len(sys.argv) - 1]
    if lastArg[0] == '-' or lastArg == 'duplus.py' or lastArg == './duplus.py':
        duplus(nohidden = nh, fromSize = frm)
    else:
        duplus(lastArg, nohidden = nh, fromSize = frm)

