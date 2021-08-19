'''
@author		William Hutton <williamhutton@gmail.com>
@version	20210819.01
@description	Append the first 1 MB of a file to prevent ransomware.
'''

import fnmatch, os

def all_files(root, patterns='*', single_level=False, yield_folders=False):
    '''
    From "Python Cookbook" 2.16 Walking Directory Trees pgs. 88-89

    Looks wicked inefficient w/ nested loops and possibly unneeded
    pattern matching, but starting here in case we need to exclude
    certain file types, which will be determined by testing.
    '''
    # Expand patterns from semicolon-separated string to list
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)
        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break
            if single_level:
                break

def is_1MB(filename):
    '''
    Return True if file is 1 Mb or larger.
    '''
    filesize = os.stat(filename).st_size
    if filesize >= 1000000:
        return True
    else:
        return False

def append1MB(file):
    '''
    It is probably more efficient to only open the file once,
    seek to the beginning, read the 1st MB, then seek to the
    end of the file for writing.

    Just being explicit for coding and testing purposes.
    '''
    f = open(file, 'rb')
    firstMB = f.read(1000000)
    f.close()
    f = open(file, 'ab')
    f.write(firstMB)
    f.close()

def padAndAppend(file):
    '''
    If the file is too small, pad it with '0x00' bytes until it is 1MB
    then just call 'append1MB'.
    '''
    fileSize = os.stat(file).st_size
    padSize = 1000000 - fileSize
    padding = bytes(padSize)
    f = open(file, 'ab')
    f.write(padding)
    f.close()
    append1MB(file)

# DEBUG
thefiles = list(all_files('./TestDirectory'))
for file in thefiles:
    if is_1MB(file):
        append1MB(file)
    else:
        padAndAppend(file)
