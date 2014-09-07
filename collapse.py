import sys
import filecmp
import argparse
import shutil
import os
from os.path import isfile, isdir, join


def main():
    parser = argparse.ArgumentParser(description='Collapse directory structures.')
    parser.add_argument('dirnames', metavar='dirnames', nargs='+', help='directories to be collapsed')
    args = parser.parse_args()
    working_dir = os.getcwd()
    for directory in args.dirnames:
        if not (isdir(directory)):
            print "Cannot find directory: " + directory
            continue
        collapse(working_dir, join(working_dir, directory))


def collapse(working_dir, collapse_dir):
    print ('Collapsing ' + collapse_dir + " to " + working_dir)

    try:
        comparison = filecmp.dircmp(working_dir, collapse_dir).right_only
        # print comparison
        unique_files = filter(isfile, [join(collapse_dir, f) for f in comparison])
        # print unique_files
        unique_dirs = filter(isdir, [join(collapse_dir, d) for d in comparison])
        # print unique_dirs

    except OSError:
        print "Cannot find input directory " + collapse_dir
        return

    for directory in unique_dirs:
        collapse(working_dir, directory)

    move_ops = 0
    for f in unique_files:
        if move_file(f, working_dir):
            move_ops += 1
            print "Moved file " + f
        else:
            print "Cannot move file " + f
            continue

    if move_ops > 0:
        print "Merging " + collapse_dir + " to " + working_dir + ' complete, ' + str(move_ops) + ' files moved.'
        remove_dir(collapse_dir)
    else:
        print "Merging " + collapse_dir + " to " + working_dir + ' complete,no files moved.'
        remove_dir(collapse_dir)


def move_file(f,d):
    try:
         print "Moving " + f + " to " + d
         shutil.move(f, d)
    except OSError:
            print "Cannot move object " + join(d, f)
            return False
    return True


def remove_dir(d):
    try:
        shutil.rmtree(d)
    except OSError:
            print ("Cannot remove directory " + d)

if __name__ == '__main__':
    main()
