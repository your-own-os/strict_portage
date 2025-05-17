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
import pathlib
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


class ConfigFileBase(abc.ABC):

    def __init__(self, path, fileCheckerClass):
        assert issubclass(fileCheckerClass, ConfigFileCheckerBase)

        self._path = path
        self._fileCheckerClass = fileCheckerClass

    @property
    def path(self):
        return self._path

    def create_checker(self, auto_fix=False, error_callback=None):
        return self._fileCheckerClass(self, auto_fix, error_callback)


class ConfigDirBase(abc.ABC):

    def __init__(self, path, dirCheckerClass):
        assert issubclass(dirCheckerClass, ConfigFileCheckerBase)

        self._path = path
        self._dirCheckerClass = dirCheckerClass

    @property
    def path(self):
        return self._path

    def create_checker(self, auto_fix=False, error_callback=None):
        return self._dirCheckerClass(self, auto_fix, error_callback)


class ConfigFileOrDirBase(abc.ABC):

    def __init__(self, path, bFileOrDir, fileClass, fileCheckerClass, dirCheckerClass):
        self._path = path

        if bFileOrDir is not None:
            self._bFileOrDir = bool(bFileOrDir)
        else:
            if os.path.isdir(self._path):
                self._bFileOrDir = False
            else:
                self._bFileOrDir = True

        self._fileClass = fileClass

        if self._bFileOrDir:
            assert issubclass(fileCheckerClass, ConfigFileCheckerBase)
            self._fileCheckerClass = fileCheckerClass
        else:
            assert issubclass(dirCheckerClass, FilesDirCheckerBase)
            self._dirCheckerClass = dirCheckerClass

    @property
    def path(self):
        return self._path

    @property
    def is_file_or_dir(self):
        return self._bFileOrDir

    def create_checker(self, auto_fix=False, error_callback=None):
        if self._bFileOrDir:
            return self._fileCheckerClass(self, auto_fix, error_callback)
        else:
            return self._dirCheckerClass(self, self._fileClass, auto_fix, error_callback)


class ConfigFileCheckerBase(abc.ABC):

    def __init__(self, parent, bAutoFix, errorCallback):
        assert isinstance(parent, ConfigFileBase) or (isinstance(parent, ConfigFileOrDirBase) and parent.is_file_or_dir)

        self._obj = parent
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else Util.doNothing

    def check(self):
        self._basicCheck()

    def _basicCheck(self):
        # check existence
        if not os.path.isfile(self._obj.path):
            self._errorCallback("%s must be a file" % (self._obj.path))
            return True

        return False


class ConfigDirCheckerBase(abc.ABC):

    def __init__(self, parent, bAutoFix, errorCallback):
        assert isinstance(parent, ConfigDirBase)

        self._obj = parent
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else Util.doNothing

    def check_self(self):
        self._basicCheck()

    def _basicCheck(self):
        # not exist, fix: create the directory
        if not os.path.exists(self._obj.path):
            if self._bAutoFix:
                os.makedirs(self._obj.path, exist_ok=True)
            else:
                self._errorCallback("\"%s\" does not exist" % (self._obj.path))
                return True         # returning True means there's fatal error

        # not a directory, fix: no way to fix it
        if not os.path.isdir(self._obj.path):
            self._errorCallback("\"%s\" is not a directory" % (self._obj.path))
            return True             # returning True means there's fatal error

        return False                # returning False means there's no fatal error


class FilesDirCheckerBase(abc.ABC):         # FIXME: name is bad

    def __init__(self, parent, fileClass, bAutoFix, errorCallback):
        assert isinstance(parent, ConfigFileOrDirBase)

        self._obj = parent
        self._fileClass = fileClass
        self._etcDirContentIndex = 1
        self._etcDirContentFileList = []
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else Util.doNothing

    def check_self(self):
        self._basicCheck()

    def check_file(self, file_name, content=None):
        if self._basicCheck():
            return

        if content is not None:
            # FIXME: check content format
            pass

        if "?" in file_name:
            file_name = file_name.replace("?", "%02d" % (self._etcDirContentIndex))
            self._etcDirContentIndex += 1

        fullfn = os.path.join(self._obj.path, file_name)

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
        if self._basicCheck():
            return

        if target is not None:
            assert os.path.exists(target)

        if "?" in link_name:
            link_name = link_name.replace("?", "%02d" % (self._etcDirContentIndex))
            self._etcDirContentIndex += 1

        linkFile = os.path.join(self._obj.path, link_name)

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
                    os.rename(linkFile, Util.getInnerFileFullfn(self._obj.path, "90-unknown"))
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
        if self._basicCheck():
            return

        if "?" in dir_name:
            dir_name = dir_name.replace("?", "%02d" % (self._etcDirContentIndex))
            self._etcDirContentIndex += 1

        fullfn = os.path.join(self._obj.path, dir_name)

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
        if self._basicCheck():
            return

        for fn in os.listdir(self._obj.path):
            fullfn = os.path.join(self._obj.path, fn)
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
        if not os.path.exists(self._obj.path):
            if self._bAutoFix:
                os.makedirs(self._obj.path, exist_ok=True)
            else:
                self._fatalCallback("\"%s\" does not exist" % (self._obj.path))
                return True         # returning True means there's fatal error

        # not a directory, fix: create the directory and move the original file into it
        if not os.path.isdir(self._obj.path):
            if self._bAutoFix:
                Util.safeFileToDir(self._obj.path, "90-unknown")
            else:
                self._fatalCallback("\"%s\" is not a directory" % (self._obj.path))
                return True         # returning True means there's fatal error

        return False                # returning False means there's no fatal error
