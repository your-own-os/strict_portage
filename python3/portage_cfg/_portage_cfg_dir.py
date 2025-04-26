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
from ._make_conf import MakeConf
from ._package_accept_keywords import PackageAcceptKeywords
from ._package_license import PackageLicense
from ._package_mask import PackageMask
from ._package_use import PackageUse


class PortageConfigDir:

    def __int__(self, prefix="/"):
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

    # portageCfgEnvDir = os.path.join(portageCfgDir, "package.env")
    # portageCfgEnvDataDir = os.path.join(portageCfgDir, "env")
    # portageCfgSetsDir = os.path.join(portageCfgDir, "sets")

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

    def check(self, auto_fix=False, error_callback=None):
        # check /etc/portage
        if not os.path.isdir(self._path):
            if auto_fix:
                os.makedirs(self._path, exist_ok=True)
            else:
                error_callback("\"%s\" is not a directory" % (self._path))

        # check /etc/portage/make.profile
        if not os.path.exists(self.make_profile_link_path):
            error_callback("%s must exist" % (self.make_profile_link_path))
        if True:
            # FIXME: ensure it points to a real profile
            pass

        # check /etc/portage/make.conf
        self.get_make_conf_obj().check(auto_fix, error_callback)

        # check /etc/portage/mirrors
        pass
