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
from .._errors import FileFormatError
from ._prototype import enforceConfigFile
from ._prototype import ConfigFileOrDirBase
from ._prototype import ConfigDirMemberFileBase
from ._prototype import ConfigFileCheckerBase
from ._prototype import ConfigDirCheckerBase


class PackageEnv(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        super().__init__(os.path.join(prefix, "etc", "portage", "package.env"),
                         file_or_dir,
                         PackageEnvMemberFile,
                         PackageEnvFileChecker,
                         PackageEnvDirChecker)
        self._envDataDir = os.path.join(prefix, "etc", "portage", "env")

    def merge_content(self, content):
        assert False

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

    @enforceConfigFile
    def merge_entries(self, entries):
        assert False

    @enforceConfigFile
    def set_entries(self, entries):
        assert False


class PackageEnvMemberFile(ConfigDirMemberFileBase):

    def __init__(self, name, prefix="/", _path=None):
        if _path is None:
            _path = os.path.join(prefix, "etc", "portage", "package.env", name)
        super().__init__(name, _path)

    def merge_content(self, content):
        assert False

    def get_entries(self):
        assert False

    def merge_entries(self, entries):
        assert False

    def set_entries(self, entries):
        assert False


class PackageEnvFileChecker(ConfigFileCheckerBase):

    def check_file(self, content=None):
        if _checkDataEnvDir(self):
            return
        super().check_file(content)

    def check_link(self, content=None, target=None):
        if _checkDataEnvDir(self):
            return
        super().check_file(content)

    def _checkContentFormat(self, content, bAutoFix, errorClass):
        return None


class PackageEnvDirChecker(ConfigDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, PackageEnvMemberFile, bAutoFix, errorCallback)

    def check_self(self):
        if _checkDataEnvDir(self):
            return
        super().check_self()

    def check_member_file(self, file_name, content=None, env_data=None):
        if _checkDataEnvDir(self):
            return
        super().check_member_file(file_name, content)
        _checkEnvData(self, file_name, env_data, True)

    def check_member_link(self, link_name, target=None, env_data=None):
        if _checkDataEnvDir(self):
            return
        super().check_member_link(link_name, target)
        _checkEnvData(self, link_name, env_data, False)

    def check_extra_file(self, dir_name):
        assert False

    def check_extra_link(self, dir_name):
        assert False

    def check_extra_dir(self, dir_name):
        assert False


def _checkDataEnvDir(obj):
    # /etc/portage/env does not exist, fix: create the directory
    if not os.path.exists(obj._obj._envDataDir):
        if obj._bAutoFix:
            os.makedirs(obj._obj._envDataDir, exist_ok=True)
        else:
            obj._errorCallback("\"%s\" does not exist" % (obj._obj.path))
            return True         # returning True means there's fatal error

    # /etc/portage/env is not a directory, fix: none
    if not os.path.isdir(obj._obj._envDataDir):
        obj._errorCallback("\"%s\" is not a directory" % (obj._obj._envDataDir))
        return True             # returning True means there's fatal error

    # returning False means there's no fatal error
    return False


def _checkEnvData(obj, fileName, envData, bCanAutoFix):
    fullfn = os.path.join(obj._obj.path, fileName)
    if not os.path.exists(fullfn):
        return

    for line in Util.readListFile(fullfn):
        fn2 = line.split()[1]
        fullfn2 = os.path.join(obj._obj._envDataDir, fn2)

        if os.path.exists(fullfn2):
            if envData is not None:
                if pathlib.Path(fullfn2).read_text() != envData[fn2]:
                    if bCanAutoFix and obj._bAutoFix:
                        pathlib.Path(fullfn2).write_text(envData[fn2])
                    else:
                        obj._errorCallback("\"%s\" has invalid content" % (fullfn2))
                        continue
        else:
            if envData is not None:
                if bCanAutoFix and obj._bAutoFix:
                    pathlib.Path(fullfn2).write_text(envData[fn2])
                else:
                    obj._errorCallback("\"%s\" does not exist" % (fullfn2))
                    continue
            else:
                obj._errorCallback("\"%s\" does not exist" % (fullfn2))
                continue
