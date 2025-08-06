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
from .._util import EntryDict
from ._prototype import enforceConfigFile
from ._prototype import ConfigFileOrDirBase
from ._prototype import ConfigDirMemberFileBase
from ._prototype import ConfigFileCheckerBase
from ._prototype import ConfigDirCheckerBase


class PackageLicense(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        super().__init__(os.path.join(prefix, "etc", "portage", "package.license"),
                         file_or_dir,
                         PackageLicenseMemberFile,
                         PackageLicensesFileChecker,
                         PackageLicensesDirChecker)

    def merge_content(self, content):
        e = _FileUtil.readEntryDict(self.path)
        e.mergeEntryDict(_FileUtil.parseEntryDict(content))
        _FileUtil.entryDictToFile(self.path, e)

    def get_license_mapping(self):
        if self.is_file_or_dir:
            e = _FileUtil.readEntryDict(self.path)
        else:
            e = EntryDict()
            for fullfn in Util.fileOrDirGetFileList(self.path):
                e.mergeEntryDict(_FileUtil.readEntryDict(fullfn, bRaiseFileNotFoundError=True))
        return e

    @enforceConfigFile
    def merge_license_mapping(self, mapping):
        e = _FileUtil.readEntryDict(self.path)
        for pkgAtom, licList in mapping.items():
            pkgName = Util.portagePkgNameFromPkgAtom(pkgAtom)
            e.mergeEntry(pkgName, licList)
        _FileUtil.entryDictToFile(self.path, e)

    @enforceConfigFile
    def set_license_mapping(self, mapping):
        e = EntryDict()
        for pkgAtom, licList in mapping.items():
            pkgName = Util.portagePkgNameFromPkgAtom(pkgAtom)
            e.mergeEntry(pkgName, licList)
        _FileUtil.entryDictToFile(self.path, e)


class PackageLicenseMemberFile(ConfigDirMemberFileBase):

    def __init__(self, name, prefix="/", _path=None):
        if _path is None:
            _path = os.path.join(prefix, "etc", "portage", "package.license", name)
        super().__init__(name, _path)

    def merge_content(self, content):
        e = _FileUtil.readEntryDict(self.path)
        e.mergeEntryDict(_FileUtil.parseEntryDict(content))
        _FileUtil.entryDictToFile(self.path, e)

    def get_license_mapping(self):
        return _FileUtil.readEntryDict(self.path).toEntryList()

    def merge_license_mapping(self, mapping):
        e = _FileUtil.readEntryDict(self.path)
        for pkgAtom, licList in mapping.items():
            pkgName = Util.portagePkgNameFromPkgAtom(pkgAtom)
            e.mergeEntry(pkgName, licList)
        _FileUtil.entryDictToFile(self.path, e)

    def set_license_mapping(self, mapping):
        e = EntryDict()
        for pkgAtom, licList in mapping.items():
            pkgName = Util.portagePkgNameFromPkgAtom(pkgAtom)
            e.mergeEntry(pkgName, licList)
        _FileUtil.entryDictToFile(self.path, e)


class PackageLicensesFileChecker(ConfigFileCheckerBase):

    def _checkContentFormat(self, content, bAutoFix, errorClass):
        if bAutoFix:
            e = _FileUtil.parseEntryDict(content)
            s = _FileUtil.entryDictToStr(e)
            return None if s == content else s
        else:
            _FileUtil.parseEntryDict(content, valueErrorClass=errorClass)
            return None


class PackageLicensesDirChecker(ConfigDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, PackageLicenseMemberFile, bAutoFix, errorCallback)


class _FileUtil:

    # entry examples:
    #   ("sys-kernel/gentoo-sources", ["GPLv3", "APL"])
    #   ("sys-kernel/*, ["*"])
    #   ("*/*, ["*"])

    @staticmethod
    def parseEntryDict(buf, valueErrorClass=None):
        ret = EntryDict()
        for line in Util.readListBuffer(buf):
            itemlist = line.split()
            if valueErrorClass is not None:
                if not Util.portageIsPkgName(itemlist[0]):
                    raise ValueError("only package name can be specified: %s" % (itemlist[0]))
            pkgName = Util.portagePkgNameFromPkgAtom(itemlist[0])
            licList = itemlist[1:]
            ret.mergeEntry(pkgName, licList)
        return ret

    @classmethod
    def readEntryDict(cls, path, bRaiseFileNotFoundError=False, valueErrorClass=None):
        try:
            return cls.parseEntryDict(pathlib.Path(path).read_text(), valueErrorClass=valueErrorClass)
        except FileNotFoundError:
            if not bRaiseFileNotFoundError:
                return EntryDict()
            else:
                raise

    @staticmethod
    def entryDictToStr(entryDict):
        ret = ""
        for pkgName, licList in entryDict.toEntryList():
            ret += "%s %s\n" % (pkgName, " ".join(licList))
        return ret

    @classmethod
    def entryDictToFile(cls, path, entryDict):
        pathlib.Path(path).write_text(cls.entryDictToStr(entryDict))
