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


import pathlib


class World:

    def __init__(self, prefix="/"):
        self._path = os.path.join(prefix, "var", "lib", "portage", "world")
        self._setPath = os.path.join(prefix, "var", "lib", "portage", "world_sets")

    @property
    def world_filepath(self):
        return self._path

    @property
    def world_sets_filepath(self):
        return self._setPath

    def get_packages(self, including_set=False):
        ret = []
        try:
            pkgList = pathlib.Path(self._path).read_text().split("\n")
            ret += [x for x in pkgList if x != ""]
        except FileNotFoundError:
            return ret

    def get_sets(self):
        pass

    def add_packages(self, *package_names):
        pkgList2 = self.get_packages()
        for pkg in package_names:
            if pkg not in pkgList2:
                pkgList2.append(pkg)
        self._writeWorldFile(pkgList2)

    def remove_packages(self, *package_names):
        pkgList2 = self.get_packages()
        for pkg in package_names:
            i = pkgList2.find(pkg)
            if i >= 0:
                pkgList2.pop(i)
        self._writeWorldFile(pkgList2)

    def add_sets(self, *set_names):
        pass

    def remove_sets(self, *set_names):
        pass

    def _writeWorldFile(self, pkgList):
        with open(self._path, "w") as f:
            for pkg in sorted(pkgList):
                f.write(pkg + "\n")
