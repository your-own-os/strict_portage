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
from .._util import Util
from .._errors import _CheckError


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

    def exists(self):
        return os.path.isfile(self._path)

    def remove(self):
        Util.forceDelete(self._path)

    def get_content(self):
        return pathlib.Path(self._path).read_text()

    @abc.abstractmethod
    def merge_content(self, content):
        pass

    def set_content(self, content):
        pathlib.Path(self._path).write_text(content)

    def clear(self):
        if os.path.exists(self._path):
            pathlib.Path(self._path).write_text("")

    def create_checker(self, auto_fix=False, error_callback=None):
        return self._fileCheckerClass(self, auto_fix, error_callback)


class ConfigDirBase(abc.ABC):

    def __init__(self, path, memberFileClass, dirCheckerClass):
        self._path = path

        assert issubclass(memberFileClass, ConfigDirMemberFileBase)
        self._memberFileClass = memberFileClass

        assert issubclass(dirCheckerClass, ConfigDirCheckerBase)
        self._dirCheckerClass = dirCheckerClass

    @property
    def path(self):
        return self._path

    def exists(self):
        return os.path.isdir(self._path)

    def remove(self):
        Util.forceDelete(self._path)

    def create_checker(self, auto_fix=False, error_callback=None):
        return self._dirCheckerClass(self, auto_fix, error_callback)


def enforceConfigFile(func):
    def wrapper(self, *args, **kwargs):
        assert self._bFileOrDir
        return func(self, *args, **kwargs)
    return wrapper


def enforceConfigDir(func):
    def wrapper(self, *args, **kwargs):
        assert not self._bFileOrDir
        return func(self, *args, **kwargs)
    return wrapper


class ConfigFileOrDirBase(abc.ABC):

    def __init__(self, path, bFileOrDir, memberFileClass, fileCheckerClass, dirCheckerClass):
        self._path = path

        if bFileOrDir is not None:
            self._bFileOrDir = bool(bFileOrDir)
        else:
            if os.path.isdir(self._path):
                self._bFileOrDir = False
            else:
                self._bFileOrDir = True

        assert issubclass(memberFileClass, ConfigDirMemberFileBase)
        self._memberFileClass = memberFileClass

        if self._bFileOrDir:
            assert issubclass(fileCheckerClass, ConfigFileCheckerBase)
            self._fileCheckerClass = fileCheckerClass
        else:
            assert issubclass(dirCheckerClass, ConfigDirCheckerBase)
            self._dirCheckerClass = dirCheckerClass

    @property
    def path(self):
        return self._path

    @property
    def is_file_or_dir(self):
        return self._bFileOrDir

    def exists(self):
        if self._bFileOrDir:
            return os.path.isfile(self._path)
        else:
            return os.path.isdir(self._path)

    def remove(self):
        Util.forceDelete(self._path)

    def get_content(self):
        if self._bFileOrDir:
            return pathlib.Path(self._path).read_text()
        else:
            buf = ""
            for fullfn in Util.fileOrDirGetFileList(self._path):
                buf = buf.rstrip("\n") + "\n\n" + pathlib.Path(fullfn).read_text().lstrip("\n")
            return buf

    @abc.abstractmethod
    @enforceConfigFile
    def merge_content(self, content):
        pass

    @enforceConfigFile
    def set_content(self, content):
        pathlib.Path(self._path).write_text(content)

    @abc.abstractmethod
    def get_entries(self):
        pass

    @abc.abstractmethod
    @enforceConfigFile
    def merge_entries(self, entries):
        pass

    @abc.abstractmethod
    @enforceConfigFile
    def set_entries(self, entries):
        pass

    @enforceConfigFile
    def clear(self):
        if os.path.exists(self._path):
            pathlib.Path(self._path).write_text("")

    @enforceConfigDir
    def has_member_file(self, name):
        return os.path.exists(os.path.join(self._path, name))

    @enforceConfigDir
    def get_member_obj(self, name):
        return self._memberFileClass(name, _path=os.path.join(self._path, name))

    def create_checker(self, auto_fix=False, error_callback=None):
        if self._bFileOrDir:
            return self._fileCheckerClass(self, auto_fix, error_callback)
        else:
            return self._dirCheckerClass(self, auto_fix, error_callback)


class ConfigDirMemberFileBase(abc.ABC):

    def __init__(self, name, path):
        assert name == os.path.basename(path)
        self._path = path

    @property
    def name(self):
        return os.path.basename(self._path)

    @property
    def path(self):
        return self._path

    def exists(self):
        return os.path.exists(self._path)

    def remove(self):
        Util.forceDelete(self._path)

    def get_content(self):
        return pathlib.Path(self._path).read_text()

    @abc.abstractmethod
    def merge_content(self, content):
        pass

    def set_content(self, content):
        pathlib.Path(self._path).write_text(content)

    def merge_member_file(self, name, remove_original=False):
        fullfn = os.path.join(os.path.dirname(self._path), name)
        assert fullfn != self._path
        self.merge_content(pathlib.Path(fullfn).read_text())
        if remove_original:
            os.unlink(fullfn)

    def clear(self):
        if os.path.exists(self._path):
            pathlib.Path(self._path).write_text("")


class ConfigFileCheckerBase(abc.ABC):

    def __init__(self, parent, bAutoFix, errorCallback):
        assert isinstance(parent, ConfigFileBase) or (isinstance(parent, ConfigFileOrDirBase) and parent.is_file_or_dir)

        self._obj = parent
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else Util.doNothing

    def check_file(self, content=None):
        if self._basicCheck():
            return

        if content is not None:
            try:
                self._checkContentFormat(content, False, _CheckError)
            except _CheckError:
                assert False

        # is a symlink, fix: remove the symlink and create a file
        if os.path.islink(self._obj.path):
            if content is not None:
                if self._bAutoFix:
                    os.unlink(self._obj.path)
                    pathlib.Path(self._obj.path).write_text(content)
                    return
                else:
                    self._errorCallback("\"%s\" should not be a symlink" % (self._obj.path))
                    return
            else:
                self._errorCallback("\"%s\" should not be a symlink" % (self._obj.path))
                return

        # content is invalid, fix: re-write content
        if content is not None:
            if pathlib.Path(self._obj.path).read_text() != content:
                if self._bAutoFix:
                    pathlib.Path(self._obj.path).write_text(content)
                else:
                    self._errorCallback("\"%s\" has invalid content" % (self._obj.path))
                    return
        else:
            try:
                newContent = self._checkContentFormat(pathlib.Path(self._obj.path).read_text(), self._bAutoFix, _CheckError)
                if newContent is not None:
                    pathlib.Path(self._obj.path).write_text(newContent)
            except _CheckError as e:
                self._errorCallback("\"%s\" has invalid content: %s" % (self._obj.path, str(e)))
                return

    def check_link(self, content=None, target=None):
        if self._basicCheck():
            return

        if content is not None:
            try:
                self._checkContentFormat(content, False, _CheckError)
            except _CheckError:
                assert False

        if target is not None:
            assert os.path.exists(target)

        # is not a symlink, fix: remove the file and create a symlink
        if not os.path.islink(self._obj.path):
            if target is not None:
                if self._bAutoFix:
                    Util.forceSymlink(target, self._obj.path)
                else:
                    self._errorCallback("\"%s\" must be a symlink to \"%s\"" % (self._obj.path, target))
                    return
            else:
                self._errorCallback("\"%s\" must be a symlink" % (self._obj.path))
                return

        # original target is wrong, fix: re-create the symlink
        if target is not None:
            if os.readlink(self._obj.path) != target:
                if self._bAutoFix:
                    Util.forceSymlink(target, self._obj.path)
                else:
                    self._errorCallback("\"%s\" must be a symlink to \"%s\"" % (self._obj.path, target))
                    return

        # content is invalid, no way to fix
        if content is not None:
            if pathlib.Path(self._obj.path).read_text() != content:
                self._errorCallback("\"%s\" has invalid content" % (self._obj.path))
                return
        else:
            try:
                self._checkContentFormat(pathlib.Path(self._obj.path).read_text(), False, _CheckError)
            except _CheckError as e:
                self._errorCallback("\"%s\" has invalid content: %s" % (self._obj.path, str(e)))
                return

    def check_file_or_link(self, content=None):
        if self._basicCheck():
            return

        if content is not None:
            try:
                self._checkContentFormat(content, False, _CheckError)
            except _CheckError:
                assert False

            if pathlib.Path(self._obj.path).read_text() != content:
                if os.path.islink(self._obj.path):
                    self._errorCallback("\"%s\" has invalid content" % (self._obj.path))
                    return
                else:
                    if self._bAutoFix:
                        pathlib.Path(self._obj.path).write_text(content)
                    else:
                        self._errorCallback("\"%s\" has invalid content" % (self._obj.path))
                        return
        else:
            try:
                if os.path.islink(self._obj.path):
                    self._checkContentFormat(pathlib.Path(self._obj.path).read_text(), False, _CheckError)
                else:
                    newContent = self._checkContentFormat(pathlib.Path(self._obj.path).read_text(), self._bAutoFix, _CheckError)
                    if newContent is not None:
                        pathlib.Path(self._obj.path).write_text(newContent)
            except _CheckError as e:
                self._errorCallback("\"%s\" has invalid content: %s" % (self._obj.path, str(e)))
                return

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _basicCheck(self):
        # check existence
        if not os.path.isfile(self._obj.path):
            self._errorCallback("%s must be a file" % (self._obj.path))
            return True

        return False

    def _checkContentFormat(self, content, bAutoFix, errorClass):
        return None


class ConfigDirCheckerBase(abc.ABC):

    def __init__(self, parent, fileClass, bAutoFix, errorCallback):
        assert isinstance(parent, ConfigDirBase) or (isinstance(parent, ConfigFileOrDirBase) and not parent.is_file_or_dir)

        self._obj = parent
        self._fileClass = fileClass
        self._memberIndex = 1
        self._memberFullfnSet = set()
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else Util.doNothing

    def check_self(self):
        self._basicCheck()

    def check_member_file(self, file_name, content=None):
        if self._basicCheck():
            return

        if content is not None:
            # FIXME: check content format
            pass

        if "?" in file_name:
            file_name = file_name.replace("?", "%02d" % (self._memberIndex))
            self._memberIndex += 1

        fullfn = os.path.join(self._obj.path, file_name)

        if os.path.exists(fullfn):
            if content is not None:
                if pathlib.Path(fullfn).read_text() != content:
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
                pathlib.Path(fullfn).write_text(content if content is not None else "")
            else:
                self._errorCallback("\"%s\" does not exist" % (fullfn))
                return

        self._memberFullfnSet.add(fullfn)

    def check_member_link(self, link_name, target=None):
        if self._basicCheck():
            return

        if target is not None:
            assert os.path.exists(target)

        if "?" in link_name:
            link_name = link_name.replace("?", "%02d" % (self._memberIndex))
            self._memberIndex += 1

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

        self._memberFullfnSet.add(linkFile)

    # FIXME: really?
    def check_extra_file(self, dir_name):
        assert False

    # FIXME: really?
    def check_extra_link(self, dir_name):
        assert False

    # FIXME: really?
    def check_extra_dir(self, dir_name):
        if self._basicCheck():
            return

        if "?" in dir_name:
            dir_name = dir_name.replace("?", "%02d" % (self._memberIndex))
            self._memberIndex += 1

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

        self._memberFullfnSet.add(fullfn)

    def finialize(self):
        if self._basicCheck():
            return

        for fn in os.listdir(self._obj.path):
            fullfn = os.path.join(self._obj.path, fn)
            if fullfn not in self._memberFullfnSet:
                if self._bAutoFix:
                    os.unlink(fullfn)
                else:
                    self._errorCallback("redundant file \"%s\" exists" % (fullfn))

        # reset some variables
        self._memberIndex = 1
        self._memberFullfnSet = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.finialize()

    def _basicCheck(self):
        # not exist, fix: create the directory
        if not os.path.exists(self._obj.path):
            if self._bAutoFix:
                os.makedirs(self._obj.path, exist_ok=True)
            else:
                self._errorCallback("\"%s\" does not exist" % (self._obj.path))
                return True         # returning True means there's fatal error

        # not a directory, fix: create the directory and move the original file into it
        if not os.path.isdir(self._obj.path):
            if self._bAutoFix:
                Util.safeFileToDir(self._obj.path, "90-unknown")
            else:
                self._errorCallback("\"%s\" is not a directory" % (self._obj.path))
                return True         # returning True means there's fatal error

        return False                # returning False means there's no fatal error
