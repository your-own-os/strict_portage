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
from ._prototype import enforceConfigFile
from ._prototype import ConfigFileOrDirBase
from ._prototype import ConfigDirMemberFileBase
from ._prototype import ConfigFileCheckerBase
from ._prototype import ConfigDirCheckerBase


class PackageUnmask(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        super().__init__(os.path.join(prefix, "etc", "portage", "package.unmask"),
                         file_or_dir,
                         PackageUnmaskMemberFile,
                         PackageUnmaskFileChecker,
                         PackageUnmaskDirChecker)

    def merge_content(self, content):
        e = _FileUtil.readEntryList(self.path)
        _FileUtil.mergeEntryList(e, Util.readListBuffer(content))
        _FileUtil.writeEntryList(self.path, e)

    def get_unmask_pkgatoms(self):
        if self.is_file_or_dir:
            e = _FileUtil.readEntryList(self.path)
        else:
            e = []
            for fullfn in Util.fileOrDirGetFileList(self.path):
                _FileUtil.mergeEntryList(e, _FileUtil.readEntryList(fullfn, bRaiseFileNotFoundError=True))
        return sorted(e)

    @enforceConfigFile
    def merge_unmask_pkgatoms(self, pkgatoms):
        e = _FileUtil.readEntryList(self.path)
        _FileUtil.mergeEntryList(e, pkgatoms)
        _FileUtil.writeEntryList(self.path, e)

    @enforceConfigFile
    def set_unmask_pkgatoms(self, pkgatoms):
        _FileUtil.writeEntryList(self.path, pkgatoms)


class PackageUnmaskMemberFile(ConfigDirMemberFileBase):

    def __init__(self, name, prefix="/", _path=None):
        if _path is None:
            _path = os.path.join(prefix, "etc", "portage", "package.unmask", name)
        super().__init__(name, _path)

    def merge_content(self, content):
        e = _FileUtil.readEntryList(self.path)
        _FileUtil.mergeEntryList(e, Util.readListBuffer(content))
        _FileUtil.writeEntryList(self.path, e)

    def get_unmask_pkgatoms(self):
        return sorted(_FileUtil.readEntryList(self.path))

    def merge_unmask_pkgatoms(self, pkgatoms):
        e = _FileUtil.readEntryList(self.path)
        _FileUtil.mergeEntryList(e, pkgatoms)
        _FileUtil.writeEntryList(self.path, e)

    def set_unmask_pkgatoms(self, pkgatoms):
        _FileUtil.writeEntryList(self.path, pkgatoms)


class PackageUnmaskFileChecker(ConfigFileCheckerBase):

    def _checkContentFormat(self, content, bAutoFix, errorClass):
        if bAutoFix:
            e = Util.readListBuffer(content)
            s = Util.genListBuffer(e)
            return None if s == content else s
        else:
            return None


class PackageUnmaskDirChecker(ConfigDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, PackageUnmaskMemberFile, bAutoFix, errorCallback)


class _FileUtil:

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

    @staticmethod
    def readEntryList(path, bRaiseFileNotFoundError=False):
        try:
            return Util.readListFile(path)
        except FileNotFoundError:
            if not bRaiseFileNotFoundError:
                return []
            else:
                raise

    @staticmethod
    def mergeEntryList(dst, src):
        for x in src:
            if x not in dst:
                dst.append(x)

    @staticmethod
    def writeEntryList(path, entryList):
        pathlib.Path(path).write_text(Util.genListBuffer(entryList))
