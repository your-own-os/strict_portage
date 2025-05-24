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
from ._prototype import ConfigDirBase
from ._prototype import ConfigDirCheckerBase
from ._make_conf import MakeConf
from ._repos_conf import ReposConf
from ._repo_postsync_dir import RepoPostSyncDir
from ._package_accept_keywords import PackageAcceptKeywords
from ._package_env import PackageEnv
from ._package_license import PackageLicense
from ._package_mask import PackageMask
from ._package_unmask import PackageUnmask
from ._package_use import PackageUse
from ._sets import Sets


class PortageConfigDir(ConfigDirBase):

    def __init__(self, prefix="/"):
        # user should guarantee existence when calling other methods
        # but checker is compatible with non-existence senario

        self._prefix = prefix
        super().__init__(os.path.join(self._prefix, "etc", "portage"), PortageConfigDirChecker)

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


class PortageConfigDirChecker(ConfigDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, bAutoFix, errorCallback)
        self._fileSet = set()

    def use_and_check_mirrors_file(self):
        if self._basicCheck():
            return

        if not self._obj.has_mirrors_file():
            self._errorCallback("%s must exist" % (self._obj.mirrors_file_path))
            return

        self._fileSet.add(self._obj.mirrors_file_path)

    def dont_use_mirrors_file(self):
        if self._basicCheck():
            return

        if self._obj.has_mirrors_file():
            self._errorCallback("\"%s\" should not exist" % (self._obj.mirrors_file_path))
            return

        self._fileSet.discard(self._obj.mirrors_file_path)

    def use_make_conf_file(self):
        if self._basicCheck():
            return

        if not self._obj.has_make_conf_file():
            self._errorCallback("%s must exist" % (self._obj.mirrors_file_path))
            return

        self._fileSet.add(self._obj.make_conf_file_path)

    def dont_use_make_conf_file(self):
        if self._basicCheck():
            return

        if self._obj.has_make_conf_file():
            self._errorCallback("\"%s\" should not exist" % (self._obj.make_conf_file_path))

        self._fileSet.discard(self._obj.make_conf_file_path)

    def use_and_check_make_profile_link(self, gentoo_repository_dir_path):
        if self._basicCheck():
            return

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

        self._fileSet.add(self._obj.make_profile_link_path)

    def dont_use_make_profile_link(self):
        if self._basicCheck():
            return

        if self._obj.has_make_profile_link():
            self._errorCallback("\"%s\" should not exist" % (self._obj.make_profile_link_path))
            return

        self._fileSet.discard(self._obj.make_profile_link_path)

    def use_repos_conf_file_or_dir(self):
        if self._basicCheck():
            return

        if not self._obj.has_repos_conf_dir():
            self._errorCallback("%s must exist" % (self._obj.repos_conf_dir_path))
            return

        self._fileSet.add(self._obj.repos_conf_dir_path)

    def dont_use_repos_conf_file_or_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_repos_conf_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.repos_conf_dir_path))
            return

        self._fileSet.discard(self._obj.repos_conf_dir_path)

    def use_repo_postsync_dir(self):
        if self._basicCheck():
            return

        if not self._obj.has_repo_postsync_dir():
            self._errorCallback("%s must exist" % (self._obj.repo_postsync_dir_path))
            return

        self._fileSet.add(self._obj.repo_postsync_dir_path)

    def dont_use_repo_postsync_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_repo_postsync_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.repo_postsync_dir_path))
            return

        self._fileSet.discard(self._obj.repo_postsync_dir_path)

    def use_package_accept_keywords_file_or_dir(self):
        if self._basicCheck():
            return

        # check /etc/portage/package.accept_keywords
        self._fileSet.add(self._obj.package_accept_keywords_file_path)

    def dont_use_package_accept_keywords_file_or_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_package_accept_keywords_file_or_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.package_accept_keywords_file_path))
            return

        self._fileSet.discard(self._obj.package_accept_keywords_file_path)

    def use_package_env_file_or_dir(self):
        if self._basicCheck():
            return

        # check /etc/portage/package.env
        self._fileSet.add(self._obj.package_env_file_path)

        # check /etc/portage/env, which must be with /etc/portage/package.env
        self._fileSet.add(self._obj.env_data_dir_path)

    def dont_use_package_env_file_or_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_package_env_file_or_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.package_env_file_path))
            return

        if self._obj.has_env_data_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.env_data_dir_path))
            return

        self._fileSet.discard(self._obj.package_env_file_path)
        self._fileSet.discard(self._obj.env_data_dir_path)

    def use_package_license_file_or_dir(self):
        if self._basicCheck():
            return

        # check /etc/portage/package.license
        self._fileSet.add(self._obj.package_license_file_path)

    def dont_use_package_license_file_or_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_package_license_file_or_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.package_license_file_path))
            return

        self._fileSet.discard(self._obj.package_license_file_path)

    def use_package_mask_file_or_dir(self):
        if self._basicCheck():
            return

        # check /etc/portage/package.mask
        self._fileSet.add(self._obj.package_mask_file_path)

    def dont_use_package_mask_file_or_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_package_mask_file_or_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.package_mask_file_path))
            return

        self._fileSet.discard(self._obj.package_mask_file_path)

    def use_package_unmask_file_or_dir(self):
        if self._basicCheck():
            return

        # check /etc/portage/package.unmask
        self._fileSet.add(self._obj.package_unmask_file_path)

    def dont_use_package_unmask_file_or_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_package_unmask_file_or_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.package_unmask_file_path))
            return

        self._fileSet.discard(self._obj.package_unmask_file_path)

    def use_package_use_file_or_dir(self):
        if self._basicCheck():
            return

        # check /etc/portage/package.use
        self._fileSet.add(self._obj.package_use_file_path)

    def dont_use_package_use_file_or_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_package_use_file_or_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.package_use_file_path))
            return

        self._fileSet.discard(self._obj.package_use_file_path)

    def use_and_check_custom_sets_dir(self):
        if self._basicCheck():
            return

        # check /etc/portage/sets
        self._fileSet.add(self._obj.custom_sets_dir_path)

    def dont_use_custom_sets_dir(self):
        if self._basicCheck():
            return

        if self._obj.has_custom_sets_dir():
            self._errorCallback("\"%s\" should not exist" % (self._obj.custom_sets_dir_path))
            return

        self._fileSet.discard(self._obj.custom_sets_dir_path)

    def use_and_check_extra_file(self, path, content=None, checker=None, default_content_generator=None):
        if content is not None:
            assert checker is None
            assert default_content_generator is None
        if checker is None:
            assert default_content_generator is None

        if self._basicCheck():
            return

        assert path.startswith(self._obj.path + "/")

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

    def use_and_check_extra_link(self, path, target=None, checker=None):
        if target is not None:
            assert checker is None

        if self._basicCheck():
            return

        assert target is not None                           # FIXME
        assert path.startswith(self._obj.path + "/")

        if not os.path.islink(path) or os.readlink(path) != target:
            if self._bAutoFix:
                Util.forceSymlink(target, path)
            else:
                self._errorCallback("\"%s\" is an invalid symlink" % (path))

        self._fileSet.add(path)

    def use_and_check_extra_dir(self, path, recursive=False):
        if self._basicCheck():
            return

        assert path.startswith(self._obj.path + "/")

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

    def finialize(self):
        for fn in os.listdir(self._obj.path):
            fullfn = os.path.join(self._obj.path, fn)
            if fullfn not in self._fileSet:
                if self._bAutoFix:
                    Util.forceDelete(fullfn)
                else:
                    self._errorCallback("redundant file \"%s\" exists" % (fullfn))

        self._fileSet = set()
