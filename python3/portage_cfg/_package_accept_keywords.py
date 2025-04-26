#!/usr/bin/env python3

# Copyright (c) 2020-2021 Fpemud <fpemud@sina.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import os
from ._util import Util


class PackageAcceptKeywords:

    def __init__(self, prefix="/"):
        self._path = os.path.join(prefix, "etc", "portage", "package.accept_keywords")

    @property
    def path(self):
        return self._path

    @property
    def is_file_or_dir(self):
        return os.path.isfile(self._path)

    def get_entries(self):
        # entry examples:
        #   "sys-kernel/gentoo-sources ~x86 ~amd64"
        #   "sys-kernel/gentoo-sources **"

        fullfnList = []
        if os.path.isfile(self._path):
            fullfnList.append(self._path)
        else:
            for fn in sorted(os.listdir(self._path)):
                fullfnList.append(os.path.join(self._path, fn))

        ret = []
        for fullfn in fullfnList:
            for line in Util.readListFile(fullfn):
                itemlist = line.split()
                ret.append((itemlist[0], itemlist[1:]))
        return ret
