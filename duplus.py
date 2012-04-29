#!/usr/bin/python
# duplus -- disk usage plus in Python

import os
import sys
import operator
import filesize

def duplus(path=os.getenv('HOME'), nohidden=False):
    sortPrint(iterateDict(path, nohidden))

def iterateDict(path, nohidden=False):
    """iterate through a given path and return a path-size dictionary"""
    if os.path.exists(path) is False:
        print 'Error: Directory does not exist.'
        sys.exit(0)

    listing = os.listdir(path)
    dictionary = dict()
    for item in listing:
        if item == '.' or item == '..':
            continue
        if nohidden == True:
            if item[0] == '.':
                continue
        ipath = os.path.join(path, item)
        if os.path.isfile(ipath):
            dictionary[item] = os.path.getsize(ipath)
        elif os.path.isdir(ipath):
            dictionary[item] = calcFolderSize(ipath)
    return dictionary

def sortPrint(dictionary):
    dic = sorted(dictionary.iteritems(), key=operator.itemgetter(1), reverse=True);
    total = 0;
    for item in dic:
        total += item[1]
    print 'Total: %s' % filesize.size(total)
    for item in dic:
        print '%-5s ......... %s' % (filesize.size(item[1]), item[0])

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
    for arg in sys.argv:
        if arg == '-nh':
            nh = True
            flag = True

    lastArg = sys.argv[len(sys.argv) - 1]
    if lastArg[0] == '-' or lastArg == 'duplus.py' or lastArg == './duplus.py':
        duplus(nohidden = nh)
    else:
        duplus(lastArg, nohidden = nh)

