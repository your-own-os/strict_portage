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
from ._errors import defaultErrorCallback
from ._make_conf import MakeConf
from ._package_accept_keywords import PackageAcceptKeywords
from ._package_license import PackageLicense
from ._package_mask import PackageMask
from ._package_use import PackageUse
from ._sets import Sets


class PortageConfigDir:

    def __init__(self, prefix="/"):
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

    def __init__(self, portageConfigDir, bAutoFix, errorCallback):
        self._obj = portageConfigDir
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else defaultErrorCallback

    def check_self(self):
        # check /etc/portage
        if not os.path.isdir(self._obj.path):
            if self._bAutoFix:
                os.makedirs(self._obj.path, exist_ok=True)
            else:
                self._errorCallback("\"%s\" is not a directory" % (self._obj.path))

    def check_mirrors_file(self):
        # check /etc/portage/mirrors
        pass

    def check_make_conf_file(self):
        self._obj.get_make_conf_obj().check(auto_fix=self._bAutoFix, error_callback=self._errorCallback)

    def check_make_profile_link(self, gentoo_repository_dir_path):
        if self._obj._prefix == "/":
            assert gentoo_repository_dir_path.startswith(self._obj._prefix)
        else:
            assert gentoo_repository_dir_path.startswith(self._obj._prefix + "/")

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

    def check_package_accept_keywords_file(self):
        # check /etc/portage/package.accept_keywords
        assert False

    def check_package_license_file(self):
        # check /etc/portage/package.license
        assert False

    def check_package_mask_file(self):
        # check /etc/portage/package.mask
        assert False

    def check_package_unmask_file(self):
        # check /etc/portage/package.unmask
        assert False

    def check_package_use_file(self):
        # check /etc/portage/package.use
        assert False

    def check_custom_sets_dir(self):
        # check /etc/portage/sets
        assert False

    def check_custom_file(self, path, content):
        assert path.startswith(self._obj.path + "/")

        if not os.path.exists(path):
            if self._bAutoFix:
                pathlib.Path(path).write_text(content)
            else:
                self._errorCallback("\"%s\" does not exist" % (path))
            return

        if pathlib.Path(path).read_text() != content:
            if self._bAutoFix:
                pathlib.Path(path).write_text(content)
            else:
                self._errorCallback("\"%s\" has invalid content" % (path))

    def check_custom_link(self, path, target):
        assert path.startswith(self._obj.path + "/")

        if not os.path.islink(path) or os.readlink(path) != target:
            if self._bAutoFix:
                Util.forceSymlink(target, path)
            else:
                self._errorCallback("\"%s\" is an invalid symlink" % (path))

    def check_custom_dir(self, path):
        assert path.startswith(self._obj.path + "/")

        if not os.path.exists(path):
            if self._bAutoFix:
                os.mkdir(path)
            else:
                self._errorCallback("\"%s\" is not a directory" % (path))
            return

        if not os.path.isdir(path):
            if self._bAutoFix:
                etcDir2 = path + ".2"
                os.mkdir(etcDir2)
                os.rename(path, os.path.join(etcDir2, _getUnknownFilename(etcDir2)))
                os.rename(etcDir2, path)
            else:
                self._errorCallback("\"%s\" is not a directory" % (path))


class PortageConfigDirFilesDirChecker:

    def __init__(self, portageConfigDir, path, bAutoFix, errorCallback):
        if self._obj._prefix == "/":
            assert path.startswith(self._obj._prefix)
        else:
            assert path.startswith(self._obj._prefix + "/")

        self._obj = portageConfigDir
        self._etcDir = path
        self._etcDirContentIndex = 1
        self._etcDirContentFileList = []
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else defaultErrorCallback

    def check_content_file(self, file_name, content=None):
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

    def check_content_link(self, link_name, target):
        assert os.path.exists(target)

        if "?" in link_name:
            link_name = link_name.replace("?", "%02d" % (self._etcDirContentIndex))
            self._etcDirContentIndex += 1

        linkFile = os.path.join(self._etcDir, link_name)

        # <linkFile> does not exist, fix: create the symlink
        if not os.path.lexists(linkFile):
            if self._bAutoFix:
                os.symlink(target, linkFile)
            else:
                self._errorCallback("\"%s\" must be a symlink to \"%s\"" % (linkFile, target))
                return

        # <linkFile> is not a symlink, fix: keep the original file, create the symlink
        if not os.path.islink(linkFile):
            if self._bAutoFix:
                os.rename(linkFile, os.path.join(self._etcDir, _getUnknownFilename(self._etcDir)))
                os.symlink(target, linkFile)
            else:
                self._errorCallback("\"%s\" must be a symlink to \"%s\"" % (linkFile, target))
                return

        # <linkFile> is wrong, fix: re-create the symlink
        if os.readlink(linkFile) != target:
            if self._bAutoFix:
                Util.forceSymlink(target, linkFile)
            else:
                self._errorCallback("\"%s\" must be a symlink to \"%s\"" % (linkFile, target))
                return

        self._etcDirContentFileList.append(linkFile)

    def check_content_dir(self, dir_name):
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

        # <fullfn> is not directory, fix: backup original file and re-create the directory
        if not os.path.isdir(fullfn):
            if self._bAutoFix:
                os.rename(fullfn, fullfn + ".unknown")
                os.mkdir(fullfn)
            else:
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


def _getUnknownFilename(dirpath):
    if not os.path.exists(os.path.join(dirpath, "90-unknown")):
        return "90-unknown"
    i = 2
    while True:
        if not os.path.exists(os.path.join(dirpath, "90-unknown-%d" % (i))):
            return "90-unknown-%d" % (i)
        i += 1
