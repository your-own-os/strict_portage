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
        self._prefix = prefix
        self._path = os.path.join(self._prefix, "var", "lib", "portage", "world")
        self._setPath = os.path.join(self._prefix, "var", "lib", "portage", "world_sets")

    @property
    def world_filepath(self):
        return self._path

    @property
    def world_sets_filepath(self):
        return self._setPath

    def get_packages(self, including_subset=False):
        ret = set()

        try:
            ret |= set(self._read(self._path))
        except FileNotFoundError:
            pass

        if including_subset:
            for sn in self._read(self._setPath):
                fullfn = os.path.join(self._prefix, "etc", "portage", "sets", sn)
                try:
                    ret |= set(self._read(fullfn))
                except FileNotFoundError:
                    pass

        return sorted(list(ret))

    def get_sets(self):
        return self._read(self._setPath)

    def add_package(self, package_name):
        self.add_packages([package_name])

    def add_packages(self, package_names):
        pkgList2 = self.get_packages()
        for pkg in package_names:
            if pkg not in pkgList2:
                pkgList2.append(pkg)
        self._write(self._path, sorted(pkgList2))

    def remove_package(self, package_name):
        self.remove_packages([package_name])

    def remove_packages(self, package_names, strict=True):
        pkgList2 = self.get_packages()
        for pkg in package_names:
            i = pkgList2.find(pkg)
            assert i >= 0
            pkgList2.pop(i)
        self._write(self._path, pkgList2)

    def add_set(self, set_name):
        self.add_set([set_name])

    def add_sets(self, *set_names):
        setList2 = self.get_sets()
        for sn in set_names:
            if sn not in setList2:
                setList2.append(sn)
        self._write(self._setPath, setList2)

    def remove_set(self, set_name):
        self.remove_set([set_name])

    def remove_sets(self, *set_names):
        setList2 = self.get_sets()
        for sn in set_names:
            i = setList2.find(sn)
            if i >= 0:
                setList2.pop(i)
        self._write(self._setPath, setList2)

    def _read(self, fullfn):
        try:
            itemList = pathlib.Path(self._path).read_text().split("\n")
            return [x for x in itemList if x != ""]
        except FileNotFoundError:
            return []

    def _write(self, fullfn, itemList):
        with open(fullfn, "w") as f:
            for pkg in sorted(itemList):
                f.write(pkg + "\n")
