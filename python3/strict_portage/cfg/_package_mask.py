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
import pathlib
from .._util import Util
from ._prototype import ConfigFileOrDirBase
from ._prototype import ConfigDirMemberFileBase
from ._prototype import ConfigFileCheckerBase
from ._prototype import ConfigDirCheckerBase


class PackageMask(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        super().__init__(os.path.join(prefix, "etc", "portage", "package.mask"),
                         file_or_dir,
                         PackageMaskMemberFile,
                         PackageMaskFileChecker,
                         PackageMaskDirChecker)

    def merge_content(self, content):
        e = _Util.readEntryList(self.path)
        _Util.mergeEntryList(e, Util.readListBuffer(content))
        _Util.writeEntryList(self.path, e)

    def get_entries(self):
        if self.is_file_or_dir:
            e = _Util.readEntryList(self.path)
        else:
            e = []
            for fullfn in Util.fileOrDirGetFileList(self.path):
                _Util.mergeEntryList(e, _Util.readEntryList(fullfn, bStrict=True))
        return sorted(e)

    def merge_entries(self, entries):
        e = _Util.readEntryList(self.path)
        _Util.mergeEntryList(e, entries)
        _Util.writeEntryList(self.path, e)

    def set_entries(self, entries):
        assert False


class PackageMaskMemberFile(ConfigDirMemberFileBase):

    def __init__(self, name, prefix="/", _path=None):
        if _path is None:
            _path = os.path.join(prefix, "etc", "portage", "package.mask", name)
        super().__init__(name, _path)

    def merge_content(self, content):
        e = _Util.readEntryList(self.path)
        _Util.mergeEntryList(e, Util.readListBuffer(content))
        _Util.writeEntryList(self.path, e)

    def get_entries(self):
        return sorted(_Util.readEntryList(self.path))

    def merge_entries(self, entries):
        e = _Util.readEntryList(self.path)
        _Util.mergeEntryList(e, entries)
        _Util.writeEntryList(self.path, e)

    def set_entries(self, entries):
        assert False


class PackageMaskFileChecker(ConfigFileCheckerBase):

    def _checkContentFormat(self, content, bAutoFix, errorClass):
        return None


class PackageMaskDirChecker(ConfigDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, PackageMaskMemberFile, bAutoFix, errorCallback)


class _Util:

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

    def mergeEntryList(dst, src):
        for x in src:
            if x not in dst:
                dst.append(x)

    def readEntryList(path, bStrict=False):
        try:
            return Util.readListFile(path)
        except FileNotFoundError:
            if not bStrict:
                return []
            else:
                raise

    def writeEntryList(path, entryList):
        buf = ""
        for entry in sorted(entryList):
            buf += "%s\n" % (entry)
        pathlib.Path(path).write_text(buf)
