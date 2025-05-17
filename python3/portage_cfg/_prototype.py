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
import abc
from ._util import Util


class SetBase(abc.ABC):

    @abc.abstractmethod
    def get_package_names(self):
        pass

    def add_package(self, package_name):
        self.add_packages([package_name])

    @abc.abstractmethod
    def add_packages(self, package_names):
        pass

    def remove_package(self, package_name):
        self.remove_packages([package_name])

    @abc.abstractmethod
    def remove_packages(self, package_names, check=True):
        pass


class ConfigFileOrDir:

    def __init__(self, path, bFileOrDir, fileClass, dirCheckerClass, fileCheckerClass):
        self._path = path

        if bFileOrDir is not None:
            self._bFileOrDir = bool(bFileOrDir)
        else:
            if os.path.isdir(self._path):
                self._bFileOrDir = False
            else:
                self._bFileOrDir = True

        self._fileClass = fileClass

        self._dirCheckerClass = dirCheckerClass
        self._fileCheckerClass = fileCheckerClass

    @property
    def path(self):
        return self._path

    @property
    def is_file_or_dir(self):
        if self._bFileOrDir is not None:
            return bool(self._bFileOrDir)
        else:
            if os.path.isfile(self._path):
                return True
            if os.path.isdir(self._path):
                return False
            return True                 # default value: file

    def get_file_object(self):
        assert os.path.isfile(self._path)
        return self._fileClass(self._path)

    def get_file_objects(self):
        assert os.path.isdir(self._path)
        return [self._fileClass(os.path.join(self._path, x)) for x in os.listdir(self._path)]

    def create_checker(self, auto_fix=False, error_callback=None):
        if self.is_file_or_dir:
            return self._fileCheckerClass(self, auto_fix, error_callback)
        else:
            return self._dirCheckerClass(self, self._fileClass, auto_fix, error_callback)


class FilesDirCheckerBase:

    def __init__(self, path, fileClass, bAutoFix, errorCallback):
        self._etcDir = path
        self._fileClass = fileClass
        self._etcDirContentIndex = 1
        self._etcDirContentFileList = []
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else Util.doNothing

    def check_self(self):
        # not exist, fix: create the directory
        if not os.path.exists(self._etcDir):
            if self._bAutoFix:
                os.makedirs(self._etcDir, exist_ok=True)
            else:
                self._errorCallback("\"%s\" does not exist" % (self._etcDir))

        # not a directory, fix: create the directory and move the original file into it
        if not os.path.isdir(self._etcDir):
            if self._bAutoFix:
                Util.safeFileToDir(self._etcDir, _unknownFilename)
            else:
                self._errorCallback("\"%s\" is not a directory" % (self._etcDir))
                return

    def check_file(self, file_name, content=None):
        if content is not None:
            # FIXME: check content format
            pass

        if "?" in file_name:
            file_name = file_name.replace("?", "%02d" % (self._etcDirContentIndex))
            self._etcDirContentIndex += 1

        fullfn = os.path.join(self._etcDir, file_name)

        if os.path.exists(fullfn):
            if content is not None:
                if pathlib.path(fullfn).read_text() != content:
                    if self._bAutoFix:
                        pathlib.Path(fullfn).write_text(content)
                    else:
                        self._errorCallback("\"%s\" has invalid content" % (fullfn))
                        return
            else:
                # FIXME: check file format
                pass
        else:
            if self._bAutoFix:
                pathlib.Path(fullfn).write_text(content)
            else:
                self._errorCallback("\"%s\" does not exist" % (fullfn))
                return

        self._etcDirContentFileList.append(fullfn)

    def check_link(self, link_name, target=None):
        if target is not None:
            assert os.path.exists(target)

        if "?" in link_name:
            link_name = link_name.replace("?", "%02d" % (self._etcDirContentIndex))
            self._etcDirContentIndex += 1

        linkFile = os.path.join(self._etcDir, link_name)

        # <linkFile> does not exist
        if not os.path.lexists(linkFile):
            if target is not None:
                if self._bAutoFix:
                    os.symlink(target, linkFile)
                else:
                    self._errorCallback("\"%s\" must be a symlink to \"%s\"" % (linkFile, target))
                    return
            else:
                self._errorCallback("\"%s\" must be a symlink" % (linkFile))
                return

        # <linkFile> is not a symlink
        if not os.path.islink(linkFile):
            if target is not None:
                if self._bAutoFix:
                    # keep the original file, create the symlink
                    os.rename(linkFile, Util.getInnerFileFullfn(self._etcDir, _unknownFilename))
                    os.symlink(target, linkFile)
                else:
                    self._errorCallback("\"%s\" must be a symlink to \"%s\"" % (linkFile, target))
                    return
            else:
                self._errorCallback("\"%s\" must be a symlink" % (linkFile))
                return

        # <linkFile> is wrong, fix: re-create the symlink
        if target is None:
            if os.readlink(linkFile) != target:
                if self._bAutoFix:
                    Util.forceSymlink(target, linkFile)
                else:
                    self._errorCallback("\"%s\" must be a symlink to \"%s\"" % (linkFile, target))
                    return

        self._etcDirContentFileList.append(linkFile)

    def check_dir(self, dir_name):
        if "?" in dir_name:
            dir_name = dir_name.replace("?", "%02d" % (self._etcDirContentIndex))
            self._etcDirContentIndex += 1

        fullfn = os.path.join(self._etcDir, dir_name)

        # <fullfn> does not exist, fix: create the directory
        if not os.path.exists(fullfn):
            if self._bAutoFix:
                os.mkdir(fullfn)
            else:
                self._errorCallback("\"%s\" does not exist" % (fullfn))
                return

        # <fullfn> is not directory
        if not os.path.isdir(fullfn):
            # no way to auto fix
            self._errorCallback("\"%s\" is not a directory" % (fullfn))
            return

        self._etcDirContentFileList.append(fullfn)

    def finialize(self):
        for fn in os.listdir(self._etcDir):
            fullfn = os.path.join(self._etcDir, fn)
            if os.path.islink(fullfn) and fullfn not in self._etcDirContentFileList:                               # remove symlinks
                if self._bAutoFix:
                    os.unlink(fullfn)
                else:
                    self._errorCallback("redundant symlink \"%s\" exists" % (fullfn))
            elif os.path.isfile(fullfn) and fn.startswith("10-") and fullfn not in self._etcDirContentFileList:    # remove redundant "10-*" files
                if self._bAutoFix:
                    os.unlink(fullfn)
                else:
                    self._errorCallback("redundant file \"%s\" exists" % (fullfn))

        # reset some variables
        self._etcDirContentIndex = 1
        self._etcDirContentFileList = []

    def _basicCheck(self):
        # not exist, fix: create the directory
        if not os.path.exists(self._etcDir):
            if self._bAutoFix:
                os.makedirs(self._etcDir, exist_ok=True)
            else:
                self._fatalCallback("\"%s\" does not exist" % (self._etcDir))
                return True     # returning True means there's fatal error

        # not a directory, fix: create the directory and move the original file into it
        if not os.path.isdir(self._etcDir):
            if self._bAutoFix:
                Util.safeFileToDir(self._etcDir, _unknownFilename)
            else:
                self._fatalCallback("\"%s\" is not a directory" % (self._etcDir))
                return True         # returning True means there's fatal error

        return False            # returning False means there's no fatal error


_unknownFilename = "90-unknown"
