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


class PackageUse(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        super().__init__(os.path.join(prefix, "etc", "portage", "package.use"),
                         file_or_dir,
                         PackageUseMemberFile,
                         PackageUseFileChecker,
                         PackageUseDirChecker)

    def merge_content(self, content):
        e = _FileUtil.readEntryDict(self.path)
        e.mergeEntryDict(_FileUtil.parseEntryDict(content))
        _FileUtil.entryDictToFile(self.path, e)

    def get_entries(self):
        if self.is_file_or_dir:
            e = _FileUtil.readEntryDict(self.path)
        else:
            e = _EntryDict()
            for fullfn in Util.fileOrDirGetFileList(self.path):
                e.mergeEntryDict(_FileUtil.readEntryDict(fullfn, bRaiseFileNotFoundError=True))
        return e.toEntryList()

    def merge_entries(self, entries):
        e = _FileUtil.readEntryDict(self.path)
        for pkgAtom, flagList in entries:
            pkgName = Util.portagePkgNameFromPkgAtom(pkgAtom)
            e.mergeEntry(pkgName, flagList)
        _FileUtil.entryDictToFile(self.path, e)

    def set_entries(self, entries):
        assert False


class PackageUseMemberFile(ConfigDirMemberFileBase):

    def __init__(self, name, prefix="/", _path=None):
        if _path is None:
            _path = os.path.join(prefix, "etc", "portage", "package.use", name)
        super().__init__(name, _path)

    def merge_content(self, content):
        e = _FileUtil.readEntryDict(self.path)
        e.mergeEntryDict(_FileUtil.parseEntryDict(content))
        _FileUtil.entryDictToFile(self.path, e)

    def get_entries(self):
        return _FileUtil.readEntryDict(self.path).toEntryList()

    def merge_entries(self, entries):
        e = _FileUtil.readEntryDict(self.path)
        for pkgAtom, flagList in entries:
            pkgName = Util.portagePkgNameFromPkgAtom(pkgAtom)
            e.mergeEntry(pkgName, flagList)
        _FileUtil.entryDictToFile(self.path, e)

    def set_entries(self, entries):
        e = _EntryDict()
        for pkgAtom, flagList in entries:
            pkgName = Util.portagePkgNameFromPkgAtom(pkgAtom)
            e.mergeEntry(pkgName, flagList)
        _FileUtil.entryDictToFile(self.path, e)

    def get_use_flag_mapping(self):
        return _FileUtil.readEntryDict(self.path)

    def set_use_flag_mapping(self, mapping):
        _FileUtil.entryDictToFile(self.path, mapping)


class PackageUseFileChecker(ConfigFileCheckerBase):

    def _checkContentFormat(self, content, bAutoFix, errorClass):
        if bAutoFix:
            e = _FileUtil.parseEntryDict(content)
            s = _FileUtil.entryDictToStr(e)
            return None if s == content else s
        else:
            _FileUtil.parseEntryDict(content, valueErrorClass=errorClass)
            return None


class PackageUseDirChecker(ConfigDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, PackageUseMemberFile, bAutoFix, errorCallback)


class _EntryDict(dict):

    def __init__(self, entryList=[]):
        super().__init__()
        for pkgName, flagList in entryList:
            assert pkgName not in self
            assert len(set(flagList)) == len(flagList)
            self[pkgName] = set(flagList)

    def mergeEntry(self, pkgName, flagList):
        if pkgName not in self:
            self[pkgName] = set()
        self[pkgName] |= set(flagList)

    def mergeEntryDict(self, entryDict):
        for pkgName, flagList in entryDict.items():
            if pkgName not in self:
                self[pkgName] = set()
            self[pkgName] |= set(flagList)

    def toEntryList(self):
        ret = []
        for k in sorted(self.keys()):
            ret.append((k, sorted(self[k])))
        return ret


class _FileUtil:

    # entry examples:
    #   ("sys-apps/systemd", ["-boot", "kernel-install"])
    #
    # we don't support this kind of entries:
    #   (">sys-apps/systemd-256.10", ["-boot", "kernel-install"])
    #

    @staticmethod
    def parseEntryDict(buf, valueErrorClass=None):
        ret = _EntryDict()
        for line in Util.readListBuffer(buf):
            itemlist = line.split()
            if valueErrorClass is not None:
                if not Util.portageIsPkgName(itemlist[0]):
                    raise ValueError("only package name can be specified: %s" % (itemlist[0]))
            pkgName = Util.portagePkgNameFromPkgAtom(itemlist[0])
            flagList = itemlist[1:]
            ret.mergeEntry(pkgName, flagList)
        return ret

    @classmethod
    def readEntryDict(cls, path, bRaiseFileNotFoundError=False, valueErrorClass=False):
        try:
            return cls.parseEntryDict(pathlib.Path(path).read_text(), valueErrorClass=valueErrorClass)
        except FileNotFoundError:
            if not bRaiseFileNotFoundError:
                return _EntryDict()
            else:
                raise

    @staticmethod
    def entryDictToStr(entryDict):
        ret = ""
        for pkgName, flagList in entryDict.toEntryList():
            ret += "%s %s\n" % (pkgName, " ".join(flagList))
        return ret

    @classmethod
    def entryDictToFile(cls, path, entryDict):
        pathlib.Path(path).write_text(cls.entryDictToStr(entryDict))
