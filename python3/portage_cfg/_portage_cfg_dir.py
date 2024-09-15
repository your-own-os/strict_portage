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
import re


class PortageConfigDir:

    def __int__(self, prefix="/"):
        self._path = os.path.join(prefix, "etc", "portage")

        self._makeProfile = os.path.join(self._path, "make.profile")

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
        else:
            tlist = Util.realPathSplit(os.path.realpath(self._makeProfile))
            if not re.fullmatch("[0-9\\.]+", tlist[-1]):
                error_callback("%s must points to a vanilla profile (eg. default/linux/amd64/17.0)" % (self._makeProfile))
