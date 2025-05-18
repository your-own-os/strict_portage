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
from ._prototype import ConfigFileOrDirBase
from ._prototype import ConfigFileCheckerBase
from ._prototype import FilesDirCheckerBase


class PackageMask(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        # user should guarantee existence when calling other methods
        # but checker is compatible with non-existence senario

        ConfigFileOrDirBase.__init__(self,
                                     os.path.join(prefix, "etc", "portage", "package.mask"),
                                     file_or_dir,
                                     None,
                                     PackageMaskFileChecker,
                                     PackageMaskDirChecker)

    def get_entries(self):
        # entry examples:
        #   "sys-kernel/gentoo-sources-2.6.37-r1"
        #   "sys-kernel/gentoo-sources-2.6.37-r1::guru"
        #   "=sys-kernel/gentoo-sources-2.6.37-r1"
        #   ">=sys-kernel/gentoo-sources-2.6.37-r1"
        #   "<=sys-kernel/gentoo-sources-2.6.37-r1"
        #   "<sys-kernel/gentoo-sources-2.6.37-r1"
        #   ">sys-kernel/gentoo-sources-2.6.37-r1"
        #   "!sys-kernel/gentoo-sources-2.6.37-r1"
        #   "~sys-kernel/gentoo-sources-2.6.37-r1"

        ret = []
        for fullfn in Util.fileOrDirGetFileList(self._path):
            ret += Util.readListFile(fullfn)
        return ret


class PackageMaskFileChecker(ConfigFileCheckerBase):
    pass


class PackageMaskDirChecker(FilesDirCheckerBase):
    pass
