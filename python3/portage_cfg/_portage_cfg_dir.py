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


class PortageConfigDir:

    def __int__(self, prefix="/"):
        self._path = os.path.join(prefix, "etc", "portage")

        self._makeProfile = os.path.join(self._path, "make.profile")

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

    # portageCfgMaskDir = os.path.join(portageCfgDir, "package.mask")
    # portageCfgUnmaskDir = os.path.join(portageCfgDir, "package.unmask")
    # portageCfgUseDir = os.path.join(portageCfgDir, "package.use")
    # portageCfgEnvDir = os.path.join(portageCfgDir, "package.env")
    # portageCfgLicFile = os.path.join(portageCfgDir, "package.license")
    # portageCfgAcceptKeywordsDir = os.path.join(portageCfgDir, "package.accept_keywords")
    # portageCfgEnvDataDir = os.path.join(portageCfgDir, "env")
    # portageCfgSetsDir = os.path.join(portageCfgDir, "sets")

    def check(self, auto_fix=False, error_callback=None):
        # check /etc/portage
        if not os.path.isdir(self._path):
            if auto_fix:
                os.makedirs(self._path, exist_ok=True)
            else:
                error_callback("\"%s\" is not a directory" % (self._path))

        # check /etc/portage/make.profile
        if not os.path.exists(self._makeProfile):
            error_callback("%s must exist" % (self._makeProfile))
        if True:
            # FIXME: ensure it points to a real profile
            pass

        # check /etc/portage/make.conf
        makeConf = MakeConf(portage_config_dir_path=self._path)
        makeConf.check(auto_fix, error_callback)
