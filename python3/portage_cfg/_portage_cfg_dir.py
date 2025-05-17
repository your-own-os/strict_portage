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
from ._util import Util
from ._make_conf import MakeConf
from ._package_accept_keywords import PackageAcceptKeywords
from ._package_license import PackageLicense
from ._package_mask import PackageMask
from ._package_use import PackageUse
from ._sets import Sets


class PortageConfigDir:

    def __init__(self, prefix="/"):
        # user should guarantee existence

        self._prefix = prefix
        self._path = os.path.join(self._prefix, "etc", "portage")

    @property
    def path(self):
        # /etc/portage
        return self._path

    @property
    def mirrors_file_path(self):
        # /etc/portage/mirrors
        return os.path.join(self._path, "mirrors")

    @property
    def make_conf_file_path(self):
        # /etc/portage/make.conf
        return os.path.join(self._path, "make.conf")

    @property
    def make_profile_link_path(self):
        # /etc/portage/make.profile
        return os.path.join(self._path, "make.profile")

    @property
    def repos_conf_dir_path(self):
        # /etc/portage/repos.conf
        return os.path.join(self._path, "repos.conf")

    @property
    def repo_postsync_dir_path(self):
        # /etc/portage/repo.postsync.d
        return os.path.join(self._path, "repo.postsync.d")

    @property
    def package_accept_keywords_dir_path(self):
        # /etc/portage/package.accept_keywords
        return os.path.join(self._path, "package.accept_keywords")

    @property
    def package_accept_keywords_file_path(self):
        # same as self.package_accept_keywords_dir_path
        return os.path.join(self._path, "package.accept_keywords")

    @property
    def package_license_dir_path(self):
        # /etc/portage/package.license
        return os.path.join(self._path, "package.license")

    @property
    def package_license_file_path(self):
        # same as self.package_license_dir_path
        return os.path.join(self._path, "package.license")

    @property
    def package_mask_dir_path(self):
        # /etc/portage/package.mask
        return os.path.join(self._path, "package.mask")

    @property
    def package_mask_file_path(self):
        # same as self.package_mask_dir_path
        return os.path.join(self._path, "package.mask")

    @property
    def package_unmask_dir_path(self):
        # /etc/portage/package.unmask
        return os.path.join(self._path, "package.unmask")

    @property
    def package_unmask_file_path(self):
        # same as self.package_unmask_dir_path
        return os.path.join(self._path, "package.unmask")

    @property
    def package_use_dir_path(self):
        # /etc/portage/package.use
        return os.path.join(self._path, "package.use")

    @property
    def package_use_file_path(self):
        # same as self.package_use_dir_path
        return os.path.join(self._path, "package.use")

    @property
    def custom_sets_dir_path(self):
        # /etc/portage/sets
        return os.path.join(self._path, "sets")

    # portageCfgEnvDir = os.path.join(portageCfgDir, "package.env")
    # portageCfgEnvDataDir = os.path.join(portageCfgDir, "env")

    def get_make_conf_obj(self):
        return MakeConf(prefix=self._prefix)

    def get_package_accept_keywords_obj(self):
        return PackageAcceptKeywords(prefix=self._prefix)

    def get_package_license_obj(self):
        return PackageLicense(prefix=self._prefix)

    def get_package_mask_obj(self):
        return PackageMask(prefix=self._prefix)

    def get_package_use_obj(self):
        return PackageUse(prefix=self._prefix)

    def get_sets_obj(self):
        return Sets(prefix=self._prefix)

    def create_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirChecker(self, auto_fix, error_callback)

    def create_repos_conf_dir_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirFilesDirChecker(self, self.repos_conf_dir_path, auto_fix, error_callback)

    def create_repo_postsync_dir_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirFilesDirChecker(self, self.repo_postsync_dir_path, auto_fix, error_callback)

    def create_package_accept_keywords_dir_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirFilesDirChecker(self, self.package_accept_keywords_dir_path, auto_fix, error_callback)

    def create_package_license_dir_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirFilesDirChecker(self, self.package_license_dir_path, auto_fix, error_callback)

    def create_package_mask_dir_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirFilesDirChecker(self, self.package_mask_dir_path, auto_fix, error_callback)

    def create_package_unmask_dir_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirFilesDirChecker(self, self.package_unmask_dir_path, auto_fix, error_callback)

    def create_package_use_dir_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirFilesDirChecker(self, self.package_use_dir_path, auto_fix, error_callback)


class PortageConfigDirChecker:

    def __init__(self, portageConfigDirObj, bAutoFix, errorCallback):
        self._obj = portageConfigDirObj
        self._fileList = []
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else Util.doNothing

    def check_self(self):
        self._basicCheck()

    def check_mirrors_file(self):
        # check /etc/portage/mirrors
        if self._basicCheck():
            return

    def check_make_conf_file(self):
        if self._basicCheck():
            return

        # does /etc/portage/make.conf exist? it would be fatal error
        if not os.path.isfile(self._obj.make_conf_file_path):
            self._errorCallback("%s must be a file" % (self._obj.make_conf_file_path))
            return

        # check /etc/portage/make.conf
        self._obj.get_make_conf_obj().check(auto_fix=self._bAutoFix, error_callback=self._errorCallback)

        self._fileList.append(self._obj.make_conf_file_path)

    def check_make_profile_link(self, gentoo_repository_dir_path):
        if self._obj._prefix == "/":
            assert gentoo_repository_dir_path.startswith(self._obj._prefix)
        else:
            assert gentoo_repository_dir_path.startswith(self._obj._prefix + "/")

        if self._basicCheck():
            return

        # check /etc/portage/make.profile
        # no way to auto fix
        if not os.path.exists(self._obj.make_profile_link_path):
            self._errorCallback("%s must exist" % (self._obj.make_profile_link_path))
            return
        if not os.path.islink(self._obj.make_profile_link_path):
            self._errorCallback("%s is not a symlink" % (self._obj.make_profile_link_path))
            return
        if not os.path.abspath(os.readlink(self._obj.make_profile_link_path)).startswith(os.path.abspath(gentoo_repository_dir_path)):
            self._errorCallback("%s points to an invalid location" % (self._obj.make_profile_link_path))
            return

        self._fileList.append(self._obj.make_profile_link_path)

    def check_package_accept_keywords_file(self, content=None):
        if self._basicCheck():
            return

        # check /etc/portage/package.accept_keywords
        self._fileList.append(self._obj.package_accept_keywords_file_path)

    def check_package_license_file(self, content=None):
        if self._basicCheck():
            return

        # check /etc/portage/package.license
        self._fileList.append(self._obj.package_license_file_path)

    def check_package_mask_file(self, content=None):
        if self._basicCheck():
            return

        # check /etc/portage/package.mask
        self._fileList.append(self._obj.package_mask_file_path)

    def check_package_unmask_file(self, content=None):
        if self._basicCheck():
            return

        # check /etc/portage/package.unmask
        self._fileList.append(self._obj.package_unmask_file_path)

    def check_package_use_file(self, content=None):
        if self._basicCheck():
            return

        # check /etc/portage/package.use
        self._fileList.append(self._obj.package_use_file_path)

    def check_custom_sets_dir(self):
        if self._basicCheck():
            return

        # check /etc/portage/sets
        self._fileList.append(self._obj.custom_sets_dir_path)

    def check_user_file(self, path, content=None):
        assert path.startswith(self._obj.path + "/")

        if self._basicCheck():
            return

        if not os.path.exists(path):
            if content is not None:
                if self._bAutoFix:
                    pathlib.Path(path).write_text(content)
                else:
                    self._fatalCallback("\"%s\" does not exist" % (path))
                    return
            else:
                self._fatalCallback("\"%s\" does not exist" % (path))
                return

        if content is not None:
            if pathlib.Path(path).read_text() != content:
                if self._bAutoFix:
                    pathlib.Path(path).write_text(content)
                else:
                    self._errorCallback("\"%s\" has invalid content" % (path))

        self._fileList.append(path)

    def check_user_link(self, path, target=None):
        assert target is not None                           # FIXME
        assert path.startswith(self._obj.path + "/")

        if self._basicCheck():
            return

        if not os.path.islink(path) or os.readlink(path) != target:
            if self._bAutoFix:
                Util.forceSymlink(target, path)
            else:
                self._errorCallback("\"%s\" is an invalid symlink" % (path))

        self._fileList.append(path)

    def check_user_dir(self, path):
        assert path.startswith(self._obj.path + "/")

        if self._basicCheck():
            return

        if not os.path.exists(path):
            if self._bAutoFix:
                os.mkdir(path)
            else:
                self._fatalCallback("\"%s\" does not exist" % (path))
                return

        if not os.path.isdir(path):
            if self._bAutoFix:
                Util.safeFileToDir(path, _unknownFilename)
            else:
                self._errorCallback("\"%s\" is not a directory" % (path))

        self._fileList.append(path)

    def check_no_mirrors_file(self):
        self._checkNoFileOrDir(self._obj.mirrors_file_path)

    def check_no_make_conf_file(self):
        self._checkNoFileOrDir(self._obj.make_conf_file_path)

    def check_no_make_profile_link(self):
        self._checkNoFileOrDir(self._obj.make_profile_link_path)

    def check_no_package_accept_keywords_file_or_dir(self):
        self._checkNoFileOrDir(self._obj.package_accept_keywords_file_path)

    def check_no_package_license_file_or_dir(self):
        self._checkNoFileOrDir(self._obj.package_license_file_path)

    def check_no_package_mask_file_or_dir(self):
        self._checkNoFileOrDir(self._obj.package_mask_file_path)

    def check_no_package_unmask_file_or_dir(self):
        self._checkNoFileOrDir(self._obj.package_unmask_file_path)

    def check_no_package_use_file_or_dir(self):
        self._checkNoFileOrDir(self._obj.package_use_file_path)

    def check_no_custom_sets_dir(self):
        self._checkNoFileOrDir(self._obj.custom_sets_dir_path)

    def finialize(self):
        for fn in os.listdir(self._obj.path):
            fullfn = os.path.join(self._obj.path, fn)
            if fullfn not in self._fileList:
                if self._bAutoFix:
                    Util.forceDelete(fullfn)
                else:
                    self._errorCallback("redundant file \"%s\" exists" % (fullfn))

        self._fileList = []

    def _basicCheck(self):
        # /etc/portage does not exist, fix: create it
        if not os.path.exists(self._obj.path):
            if self._bAutoFix:
                os.makedirs(self._obj.path, exist_ok=True)
            else:
                self._fatalCallback("\"%s\" does not exist" % (self._obj.path))
                return True     # returning True means there's fatal error

        # /etc/portage is not a directory, fix: no way to fix it
        if not os.path.isdir(self._obj.path):
            self._fatalCallback("\"%s\" is not a directory" % (self._obj.path))
            return True         # returning True means there's fatal error

        return False            # returning False means there's no fatal error

    def _checkNoFileOrDir(self, path):
        if self._basicCheck():
            return

        if os.path.exists(path):
            self._fatalCallback("\"%s\" should not exist" % (path))


class PortageConfigDirFilesDirChecker:

    def __init__(self, portageConfigDirObj, path, bAutoFix, errorCallback):
        if self._obj._prefix == "/":
            assert path.startswith(self._obj._prefix)
        else:
            assert path.startswith(self._obj._prefix + "/")

        self._obj = portageConfigDirObj
        self._etcDir = path
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
                self._fatalCallback("\"%s\" does not exist" % (self._etcDir))

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
