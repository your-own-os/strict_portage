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
from ._errors import FileFormatError
from ._prototype import ConfigFileOrDirBase
from ._prototype import ConfigFileCheckerBase
from ._prototype import FilesDirCheckerBase


class PackageEnv(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        # user should guarantee existence when calling other methods
        # but checker is compatible with non-existence senario

        ConfigFileOrDirBase.__init__(self,
                                     os.path.join(prefix, "etc", "portage", "package.env"),
                                     file_or_dir,
                                     None,
                                     PackageEnvFileChecker,
                                     PackageEnvDirChecker)
        self._envDataDir = os.path.join(prefix, "etc", "portage", "env")

    def get_entries(self):
        # entry examples:
        #   ("sys-libs/glibc", "glibc.conf")

        ret = []
        for fullfn in Util.fileOrDirGetFileList(self._path):
            for i, line in enumerate(Util.readListFile(fullfn)):
                itemlist = line.split()
                if len(itemlist) != 2:
                    raise FileFormatError('format error at "%s" line %d' % (fullfn, i + 1))
                ret.append((itemlist[0], itemlist[1]))
        return ret


class PackageEnvFileChecker(ConfigFileCheckerBase):

    def _basicCheck(self):
        if super()._basicCheck():
            return True

        # /etc/portage/env does not exist, fix: create the directory
        if not os.path.exists(self._obj._envDataDir):
            if self._bAutoFix:
                os.makedirs(self._obj._envDataDir, exist_ok=True)
            else:
                self._errorCallback("\"%s\" does not exist" % (self._obj.path))
                return True         # returning True means there's fatal error

        # /etc/portage/env is not a directory, fix: no way to fix it
        if not os.path.isdir(self._obj._envDataDir):
            self._errorCallback("\"%s\" is not a directory" % (self._obj._envDataDir))
            return True             # returning True means there's fatal error

        return False                # returning False means there's no fatal error


class PackageEnvDirChecker(FilesDirCheckerBase):

    def _basicCheck(self):
        if super()._basicCheck():
            return True

        # /etc/portage/env does not exist, fix: create the directory
        if not os.path.exists(self._obj._envDataDir):
            if self._bAutoFix:
                os.makedirs(self._obj._envDataDir, exist_ok=True)
            else:
                self._errorCallback("\"%s\" does not exist" % (self._obj.path))
                return True         # returning True means there's fatal error

        # /etc/portage/env is not a directory, fix: no way to fix it
        if not os.path.isdir(self._obj._envDataDir):
            self._errorCallback("\"%s\" is not a directory" % (self._obj._envDataDir))
            return True             # returning True means there's fatal error

        return False                # returning False means there's no fatal error
