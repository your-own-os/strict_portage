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
from ._prototype import ConfigDirBase
from ._prototype import ConfigDirMemberFileBase
from ._prototype import ConfigDirCheckerBase


class RepoPostSyncDir(ConfigDirBase):

    def __init__(self, prefix="/"):
        super().__init__(os.path.join(prefix, "etc", "portage", "repo.postsync.d"),
                         RepoPostSyncDirMemberFile,
                         RepoPostSyncDirDirChecker)

    def merge_content(self, content):
        assert False


class RepoPostSyncDirMemberFile(ConfigDirMemberFileBase):

    def __init__(self, name, prefix="/", _path=None):
        if _path is None:
            _path = os.path.join(prefix, "etc", "portage", "repo.postsync.d", name)
        super().__init__(name, _path)

    def merge_content(self, content):
        assert False


class RepoPostSyncDirDirChecker(ConfigDirCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, RepoPostSyncDirMemberFile, bAutoFix, errorCallback)
