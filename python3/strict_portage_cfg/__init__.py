#!/usr/bin/env python3

# gstage4 - gentoo stage4 building
#
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


__package__ = 'strict_portage_cfg'

__version__ = '0.0.1'

__author__ = 'Fpemud <fpemud@sina.com>'


from ._portage_cfg_dir import PortageConfigDir

from ._make_conf import MakeConf
from ._repos_conf import ReposConf
from ._repo_postsync_dir import RepoPostSyncDir

from ._package_accept_keywords import PackageAcceptKeywords
from ._package_accept_keywords import PackageAcceptKeywordsMemberFile

from ._package_env import PackageEnv

from ._package_license import PackageLicense
from ._package_license import PackageLicenseMemberFile

from ._package_mask import PackageMask
from ._package_mask import PackageMaskMemberFile

from ._package_unmask import PackageUnmask
from ._package_unmask import PackageUnmaskMemberFile

from ._package_use import PackageUse
from ._package_use import PackageUseMemberFile

from ._sets import Sets
from ._sets import CustomSet
from ._sets import World

from ._errors import FileFormatError


__all__ = [
    "PortageConfigDir",
    "MakeConf",
    "ReposConf",
    "RepoPostSyncDir",
    "PackageAcceptKeywords",
    "PackageAcceptKeywordsMemberFile",
    "PackageEnv",
    "PackageLicense",
    "PackageLicenseMemberFile",
    "PackageMask",
    "PackageMaskMemberFile",
    "PackageUnmask",
    "PackageUnmaskMemberFile",
    "PackageUse",
    "PackageUseMemberFile",
    "Sets",
    "CustomSet",
    "World",
    "FileFormatError",
]
