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
from ._prototype import ConfigDirMemberFileBase
from ._prototype import FilesDirCheckerBase


class PackageUse(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        # user should guarantee existence when calling other methods
        # but checker is compatible with non-existence senario

        ConfigFileOrDirBase.__init__(self,
                                     os.path.join(prefix, "etc", "portage", "package.use"),
                                     file_or_dir,
                                     PackageUseMemberFile,
                                     PackageUseFileChecker,
                                     PackageUseDirChecker)

    def get_entries(self):
        _FileClass.get_entries(self)

    def merge_entries(self, new_entries):
        _FileClass.merge_entries(self, new_entries)

    def merge_content(self, new_content):
        _FileClass.merge_content(self, new_content)


class PackageUseMemberFile(ConfigDirMemberFileBase):

    def get_entries(self):
        _FileClass.get_entries(self)

    def merge_entries(self, new_entries):
        _FileClass.merge_entries(self, new_entries)

    def merge_content(self, new_content):
        _FileClass.merge_content(self, new_content)


class PackageUseFileChecker:
    pass


class PackageUseDirChecker(FilesDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, PackageUseMemberFile, bAutoFix, errorCallback)


class _FileClass:

    # entry examples:
    #   ("sys-apps/systemd", ["-boot", "kernel-install"])
    #   (">sys-apps/systemd-256.10", ["-boot", "kernel-install"])

    @staticmethod
    def get_entries(p):
        ret = []
        for fullfn in Util.fileOrDirGetFileList(p.path):
            for line in Util.readListFile(fullfn):
                itemlist = line.split()
                ret.append((itemlist[0], itemlist[1:]))
        return ret

    @staticmethod
    def merge_entries(p, new_entries):
        pass

    @staticmethod
    def merge_content(p, new_content):
        pass
