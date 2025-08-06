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
from ._prototype import ConfigFileOrDirBase
from ._prototype import ConfigDirMemberFileBase
from ._prototype import ConfigFileCheckerBase
from ._prototype import ConfigDirCheckerBase


class PackageAcceptKeywords(ConfigFileOrDirBase):

    def __init__(self, prefix="/", file_or_dir=None):
        super().__init__(os.path.join(prefix, "etc", "portage", "package.accept_keywords"),
                         file_or_dir,
                         PackageAcceptKeywordsMemberFile,
                         PackageAcceptKeywordsFileChecker,
                         PackageAcceptKeywordsDirChecker)

    def merge_content(self, content):
        e = _FileUtil.readEntryDict(self.path)
        e.mergeEntryDict(_FileUtil.parseEntryDict(content))
        _FileUtil.entryDictToFile(self.path, e)

    def get_entries(self):
        if self.is_file_or_dir:
            e = _FileUtil.readEntryDict(self.path)
        else:
            e = EntryDict()
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


class PackageAcceptKeywordsMemberFile(ConfigDirMemberFileBase):

    def __init__(self, name, prefix="/", _path=None):
        if _path is None:
            _path = os.path.join(prefix, "etc", "portage", "package.accept_keywords", name)
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
        e = EntryDict()
        for pkgAtom, flagList in entries:
            pkgName = Util.portagePkgNameFromPkgAtom(pkgAtom)
            e.mergeEntry(pkgName, flagList)
        _FileUtil.entryDictToFile(self.path, e)


class PackageAcceptKeywordsFileChecker(ConfigFileCheckerBase):

    def _checkContentFormat(self, content, bAutoFix, errorClass):
        if bAutoFix:
            e = _FileUtil.parseEntryDict(content)
            s = _FileUtil.entryDictToStr(e)
            return None if s == content else s
        else:
            _FileUtil.parseEntryDict(content, valueErrorClass=errorClass)
            return None


class PackageAcceptKeywordsDirChecker(ConfigDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, PackageAcceptKeywordsMemberFile, bAutoFix, errorCallback)


class _FileUtil:

    # entry examples:
    #   ("sys-kernel/gentoo-sources", ["~x86", "~amd64"])
    #   ("sys-kernel/gentoo-sources", ["**"])
    #
    # we don't support this kind of entries:
    #   (">sys-apps/systemd-256.10", ["-~x86"])
    #

    @staticmethod
    def parseEntryDict(buf, valueErrorClass=None):
        ret = EntryDict()
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
        for pkgName, flagList in entryDict.toEntryList():
            ret += "%s %s\n" % (pkgName, " ".join(flagList))
        return ret

    @classmethod
    def entryDictToFile(cls, path, entryDict):
        pathlib.Path(path).write_text(cls.entryDictToStr(entryDict))
