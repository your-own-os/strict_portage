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
from ._make_conf import MakeConf
from ._mirrors import Mirrors
from ._repos_conf import ReposConf
from ._repo_postsync_dir import RepoPostSyncDir
from ._package_accept_keywords import PackageAcceptKeywords
from ._package_env import PackageEnv
from ._package_license import PackageLicense
from ._package_mask import PackageMask
from ._package_unmask import PackageUnmask
from ._package_use import PackageUse
from ._sets import Sets


class PortageConfigDir:

    def __init__(self, prefix="/"):
        self._prefix = prefix
        self._path = os.path.join(self._prefix, "etc", "portage")

    @property
    def path(self):
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
    def package_accept_keywords_file_path(self):
        # /etc/portage/package.accept_keywords
        return os.path.join(self._path, "package.accept_keywords")

    @property
    def package_accept_keywords_dir_path(self):
        # same as self.package_accept_keywords_file_path
        return os.path.join(self._path, "package.accept_keywords")

    @property
    def package_env_file_path(self):
        # /etc/portage/package.env
        return os.path.join(self._path, "package.env")

    @property
    def package_env_dir_path(self):
        # same as self.package_env_file_path
        return os.path.join(self._path, "package.env")

    @property
    def package_license_file_path(self):
        # /etc/portage/package.license
        return os.path.join(self._path, "package.license")

    @property
    def package_license_dir_path(self):
        # same as self.package_license_file_path
        return os.path.join(self._path, "package.license")

    @property
    def package_mask_file_path(self):
        # /etc/portage/package.mask
        return os.path.join(self._path, "package.mask")

    @property
    def package_mask_dir_path(self):
        # same as self.package_mask_file_path
        return os.path.join(self._path, "package.mask")

    @property
    def package_unmask_file_path(self):
        # /etc/portage/package.unmask
        return os.path.join(self._path, "package.unmask")

    @property
    def package_unmask_dir_path(self):
        # same as self.package_unmask_file_path
        return os.path.join(self._path, "package.unmask")

    @property
    def package_use_file_path(self):
        # /etc/portage/package.use
        return os.path.join(self._path, "package.use")

    @property
    def package_use_dir_path(self):
        # same as self.package_use_file_path
        return os.path.join(self._path, "package.use")

    @property
    def custom_sets_dir_path(self):
        # /etc/portage/sets
        return os.path.join(self._path, "sets")

    @property
    def env_data_dir_path(self):
        # /etc/portage/env
        return os.path.join(self._path, "env")

    def exists(self):
        return os.path.isdir(self._path)

    def remove(self):
        Util.forceDelete(self._path)

    def has_make_conf_file(self):
        return os.path.isfile(self.make_conf_file_path)

    def has_mirrors_file(self):
        return os.path.isfile(self.mirrors_file_path)

    def has_make_profile_link(self):
        return os.path.islink(self.make_profile_link_path)

    def has_repos_conf_dir(self):
        return os.path.isdir(self.repos_conf_dir_path)

    def has_repo_postsync_dir(self):
        return os.path.isdir(self.repo_postsync_dir_path)

    def has_package_accept_keywords_file_or_dir(self):
        return os.path.exists(self.package_accept_keywords_file_path)

    def has_package_env_file_or_dir(self):
        return os.path.exists(self.package_env_file_path)

    def has_package_license_file_or_dir(self):
        return os.path.exists(self.package_license_file_path)

    def has_package_mask_file_or_dir(self):
        return os.path.exists(self.package_mask_file_path)

    def has_package_unmask_file_or_dir(self):
        return os.path.exists(self.package_unmask_file_path)

    def has_package_use_file_or_dir(self):
        return os.path.exists(self.package_use_file_path)

    def has_custom_sets_dir(self):
        return os.path.isdir(self.custom_sets_dir_path)

    def has_env_data_dir(self):
        return os.path.isdir(self.env_data_dir_path)

    def get_make_conf_obj(self):
        return MakeConf(prefix=self._prefix)

    def get_mirrors_obj(self):
        return Mirrors(prefix=self._prefix)

    def get_repos_conf_obj(self, file_or_dir=None):
        return ReposConf(prefix=self._prefix, file_or_dir=file_or_dir)

    def get_repo_postsync_dir_obj(self):
        return RepoPostSyncDir(prefix=self._prefix)

    def get_package_accept_keywords_obj(self, file_or_dir=None):
        return PackageAcceptKeywords(prefix=self._prefix, file_or_dir=file_or_dir)

    def get_package_env_obj(self, file_or_dir=None):
        return PackageEnv(prefix=self._prefix, file_or_dir=file_or_dir)

    def get_package_license_obj(self, file_or_dir=None):
        return PackageLicense(prefix=self._prefix, file_or_dir=file_or_dir)

    def get_package_mask_obj(self, file_or_dir=None):
        return PackageMask(prefix=self._prefix, file_or_dir=file_or_dir)

    def get_package_unmask_obj(self, file_or_dir=None):
        return PackageUnmask(prefix=self._prefix, file_or_dir=file_or_dir)

    def get_package_use_obj(self, file_or_dir=None):
        return PackageUse(prefix=self._prefix, file_or_dir=file_or_dir)

    def get_sets_obj(self):
        return Sets(prefix=self._prefix)

    def create_checker(self, auto_fix=False, error_callback=None):
        return PortageConfigDirChecker(self, auto_fix, error_callback)


class PortageConfigDirChecker:

    def __init__(self, parent, bAutoFix, errorCallback):
        self._obj = parent
        self._bAutoFix = bAutoFix
        self._errorCallback = errorCallback if errorCallback is not None else Util.doNothing

        self._fileSet = {
            self._obj.make_profile_link_path,
            self._obj.make_conf_file_path,
            self._obj.mirrors_file_path,
            self._obj.repos_conf_dir_path,
            self._obj.repo_postsync_dir_path,
            self._obj.package_accept_keywords_file_path,
            self._obj.package_env_file_path,
            self._obj.env_data_dir_path,
            self._obj.package_license_file_path,
            self._obj.package_mask_file_path,
            self._obj.package_unmask_file_path,
            self._obj.package_use_file_path,
            self._obj.custom_sets_dir_path,
        }

    def check_self(self):
        self._basicCheck()

    def check_make_profile_link(self, gentoo_repository_dir_path=None, profile=None, fallback_profile=None):
        if gentoo_repository_dir_path is not None:
            assert os.path.isabs(gentoo_repository_dir_path)
            assert Util.isUnderDir(gentoo_repository_dir_path, self._obj._prefix)
        if profile is not None:
            assert gentoo_repository_dir_path is not None
        if fallback_profile is not None:
            assert gentoo_repository_dir_path is not None
            assert profile is None

        if self._basicCheck():
            return

        if profile is not None:
            tTarget = os.path.join("..", "..", gentoo_repository_dir_path[len(self._obj._prefix):], profile)
        else:
            tTarget = None

        if fallback_profile is not None:
            fallbackTarget = os.path.join("..", "..", gentoo_repository_dir_path[len(self._obj._prefix):], fallback_profile)
        else:
            fallbackTarget = None

        # not exist, fix: create using profile & fallback_profile
        if not os.path.islink(self._obj.make_profile_link_path):
            if self._bAutoFix:
                if tTarget is not None:
                    Util.forceSymlink(tTarget, self._obj.make_profile_link_path)
                    return
                if fallbackTarget is not None:
                    Util.forceSymlink(fallbackTarget, self._obj.make_profile_link_path)
                    return
            self._errorCallback("%s must be a symlink" % (self._obj.make_profile_link_path))
            return

        dn = os.readlink(self._obj.make_profile_link_path)

        # not the same with profile, fix: re-create using profile
        if tTarget is not None:
            if dn == tTarget:
                # check passed, no matter if profile exists or not
                return
            if self._bAutoFix:
                Util.forceSymlink(tTarget, self._obj.make_profile_link_path)
                return
            self._errorCallback("%s is invalid" % (self._obj.make_profile_link_path))
            return

        # target not exist, fix: try to re-create using fallback_profile
        if not os.path.exists(self._obj.make_profile_link_path):
            if self._bAutoFix and fallbackTarget is not None:
                Util.forceSymlink(fallbackTarget, self._obj.make_profile_link_path)
                return
            else:
                self._errorCallback("%s points to an non-exist profile" % (self._obj.make_profile_link_path))
                return

        # does not points into "gentoo_repository_dir_path", fix: try to re-create using the same profile
        if gentoo_repository_dir_path is not None:
            if not Util.isUnderDir(os.path.normpath(os.path.join(self._obj.path, dn)), gentoo_repository_dir_path):
                if self._bAutoFix:
                    # we can fix it if the same profile exists in "gentoo_repository_dir_path"
                    while dn != "":
                        idx = dn.find("/")
                        if idx == -1:
                            break
                        if dn[:idx] in [".", ".."]:
                            dn = dn[idx+1:]
                            continue
                        dn = dn[idx+1:]
                        if os.path.exists(os.path.join(gentoo_repository_dir_path, dn)):        # FIXME: should also check it is a real profile dir
                            Util.forceSymlink(os.path.join("..", "..", gentoo_repository_dir_path[len(self._obj.path):], dn), self._obj.make_profile_link_path)
                            return
                self._errorCallback("%s points to an invalid location" % (self._obj.make_profile_link_path))
                return

    def disallow_make_conf_file(self):
        self._fileSet.discard(self._obj.make_conf_file_path)

    def disallow_mirrors_file(self):
        self._fileSet.discard(self._obj.mirrors_file_path)

    def disallow_repos_conf_file_or_dir(self):
        self._fileSet.discard(self._obj.repos_conf_dir_path)

    def disallow_repo_postsync_dir(self):
        self._fileSet.discard(self._obj.repo_postsync_dir_path)

    def disallow_package_accept_keywords_file_or_dir(self):
        self._fileSet.discard(self._obj.package_accept_keywords_file_path)

    def disallow_package_env_file_or_dir(self):
        self._fileSet.discard(self._obj.package_env_file_path)
        self._fileSet.discard(self._obj.env_data_dir_path)

    def disallow_package_license_file_or_dir(self):
        self._fileSet.discard(self._obj.package_license_file_path)

    def disallow_package_mask_file_or_dir(self):
        self._fileSet.discard(self._obj.package_mask_file_path)

    def disallow_package_unmask_file_or_dir(self):
        self._fileSet.discard(self._obj.package_unmask_file_path)

    def disallow_package_use_file_or_dir(self):
        self._fileSet.discard(self._obj.package_use_file_path)

    def disallow_custom_sets_dir(self):
        self._fileSet.discard(self._obj.custom_sets_dir_path)

    def use_and_check_extra_file(self, path, content=None, checker=None, default_content_generator=None):
        if content is not None:
            assert checker is None
        if checker is None:
            assert default_content_generator is None

        if self._basicCheck():
            return

        assert Util.isUnderDir(path, self._obj.path)

        if not os.path.exists(path):
            if content is not None:
                if self._bAutoFix:
                    pathlib.Path(path).write_text(content)
                else:
                    self._errorCallback("\"%s\" does not exist" % (path))
                    return
            else:
                self._errorCallback("\"%s\" does not exist" % (path))
                return

        if content is not None:
            if pathlib.Path(path).read_text() != content:
                if self._bAutoFix:
                    pathlib.Path(path).write_text(content)
                else:
                    self._errorCallback("\"%s\" has invalid content" % (path))

        if checker is not None:
            if not checker(pathlib.Path(path).read_text()):
                if default_content_generator is not None:
                    if self._bAutoFix:
                        pathlib.Path(path).write_text(default_content_generator())
                    else:
                        self._errorCallback("\"%s\" has invalid content" % (path))
                else:
                    self._errorCallback("\"%s\" has invalid content" % (path))

        self._fileSet.add(path)

    def use_and_check_extra_link(self, path, target=None, checker=None, default_target_generator=None):
        if target is not None:
            assert checker is None
        if checker is None:
            assert default_target_generator is None

        if self._basicCheck():
            return

        assert target is not None                                           # FIXME
        assert Util.isUnderDir(path, self._obj.path)

        if not os.path.islink(path) or os.readlink(path) != target:
            if self._bAutoFix:
                Util.forceSymlink(target, path)
            else:
                self._errorCallback("\"%s\" is an invalid symlink" % (path))

        self._fileSet.add(path)

    def use_and_check_extra_dir(self, path, recursive=False):
        if self._basicCheck():
            return

        assert Util.isUnderDir(path, self._obj.path)

        if not os.path.exists(path):
            if self._bAutoFix:
                os.mkdir(path)
            else:
                self._errorCallback("\"%s\" does not exist" % (path))
                return

        if not os.path.isdir(path):
            if self._bAutoFix:
                Util.safeFileToDir(path, "90-unknown")
            else:
                self._errorCallback("\"%s\" is not a directory" % (path))

        self._fileSet.add(path)
        if recursive:
            # only recurse one level
            for fn in os.listdir(path):
                self._fileSet.add(os.path.join(path, fn))

    def finalize(self):
        for fn in os.listdir(self._obj.path):
            fullfn = os.path.join(self._obj.path, fn)
            if fullfn not in self._fileSet:
                if self._bAutoFix:
                    Util.forceDelete(fullfn)
                else:
                    self._errorCallback("redundant file \"%s\" exists" % (fullfn))

        self._fileSet = set()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _basicCheck(self):
        # not exist, fix: create the directory
        if not os.path.exists(self._obj.path):
            if self._bAutoFix:
                os.makedirs(self._obj.path, exist_ok=True)
            else:
                self._errorCallback("\"%s\" does not exist" % (self._obj.path))
                return True         # returning True means there's fatal error

        # not a directory, fix: none
        if not os.path.isdir(self._obj.path):
            self._errorCallback("\"%s\" is not a directory" % (self._obj.path))
            return True             # returning True means there's fatal error

        # returning False means there's no fatal error
        return False
