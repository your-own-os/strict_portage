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
from ._prototype import ConfigFileBase
from ._prototype import ConfigFileCheckerBase


class Mirrors(ConfigFileBase):

    def __init__(self, prefix="/"):
        super().__init__(os.path.join(prefix, "etc", "portage", "mirrors"),
                         MirrorsChecker)

    def merge_content(self, content):
        e = _FileUtil.readEntryDict(self.path)
        e.mergeEntryDict(_FileUtil.parseEntryDict(content))
        _FileUtil.entryDictToFile(self.path, e)

    def get_mirror_mapping(self):
        return _FileUtil.readEntryDict(self.path)

    def merge_use_flag_mapping(self, mapping):
        e = _FileUtil.readEntryDict(self.path)
        e.mergeEntryDict(mapping)
        _FileUtil.entryDictToFile(self.path, e)

    def set_mirror_mapping(self, mapping):
        _FileUtil.entryDictToFile(self.path, mapping)


class MirrorsChecker(ConfigFileCheckerBase):

    def check(self):
        pass


class _EntryDict(dict):

    def __init__(self, entryList=[]):
        super().__init__()
        for mirrorName, mirrorSiteList in entryList:
            assert mirrorName not in self
            assert len(set(mirrorSiteList)) == len(mirrorSiteList)
            self[mirrorName] = set(mirrorSiteList)

    def mergeEntry(self, mirrorName, mirrorSiteList):
        if mirrorName not in self:
            self[mirrorName] = set()
        self[mirrorName] |= set(mirrorSiteList)

    def mergeEntryDict(self, entryDict):
        for mirrorName, mirrorSiteList in entryDict.items():
            if mirrorName not in self:
                self[mirrorName] = set()
            self[mirrorName] |= set(mirrorSiteList)

    def toEntryList(self):
        ret = []
        for k in sorted(self.keys()):
            ret.append((k, sorted(self[k])))
        return ret


class _FileUtil:

    # entry examples:
    #   ("hf-co", ["https://hf-mirror.com", "https://huggingface.co"])

    @staticmethod
    def parseEntryDict(buf):
        ret = _EntryDict()
        for line in Util.readListBuffer(buf):
            itemlist = line.split()
            ret.mergeEntry(itemlist[0], itemlist[1:])
        return ret

    @classmethod
    def readEntryDict(cls, path, bRaiseFileNotFoundError=False):
        try:
            return cls.parseEntryDict(pathlib.Path(path).read_text())
        except FileNotFoundError:
            if not bRaiseFileNotFoundError:
                return _EntryDict()
            else:
                raise

    @staticmethod
    def entryDictToStr(entryDict):
        ret = ""
        for mirrorName, mirrorSiteList in entryDict.toEntryList():
            ret += "%s %s\n" % (mirrorName, " ".join(mirrorSiteList))
        return ret

    @classmethod
    def entryDictToFile(cls, path, entryDict):
        pathlib.Path(path).write_text(cls.entryDictToStr(entryDict))
