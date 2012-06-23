#!/usr/bin/python

########################################################
# Downloads entire album on imgur album
# Copyright 2012 James Otten <james_otten@lavabit.com>
########################################################

############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################

import os
import re
import sys
import urllib
import urllib2
import urlparse
import multiprocessing

DIR = os.environ['HOME'] + "/Pictures/imgur/"

IMAGE_URL_REGEX = re.compile("(\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.[a-z]+)")
PROCESSES = 8


def download(url, path):
    if os.path.exists(path):
        return
    urllib.urlretrieve(url, path)

def uniqueify(l):
    eset = []
    for e in l:
        if e not in eset:
            if e[:len(e) - 5] + e[len(e)-4:] not in eset:
                eset.append(e)
    return eset

def usage():
    print("Usage:")
    print("album-grabber <URL> [TITLE]")
    sys.exit(1)

def main(args):
    pool = multiprocessing.Pool(PROCESSES)
    source = urllib2.urlopen(args[0]).read()
    tokens = args[0].split('/')
    title = ""
    if(len(args) == 2):
        title = args[1] + " - "

    path = "%s%s%s" % (DIR, title, tokens[4])
    if not os.path.exists(path):
        os.mkdir(path)

    images = uniqueify(re.findall(IMAGE_URL_REGEX, source))
    print("Found: %d images" % len(images))
    for image_url in set(images):
        url = urlparse.urljoin(args[0], image_url)
        filename = url.split('/')[-1]
        path_ = os.path.join(path, filename)
        pool.apply_async(download, [url, path_])
    pool.close()
    pool.join()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        usage()
