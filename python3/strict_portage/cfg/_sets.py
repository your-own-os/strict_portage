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
from ._prototype import SetBase


class Sets:

    def __init__(self, prefix="/"):
        self._prefix = prefix
        self._customSetDir = os.path.join(self._prefix, "etc", "portage", "sets")

    def get_world(self):
        return self.get_system_set("world")

    def get_system_set(self, name):
        if name == "world":
            return World(self._prefix)
        else:
            assert False

    def get_custom_set_names(self):
        if os.path.isdir(self._customSetDir):
            return os.listdir(self._customSetDir)
        else:
            return []

    def get_custom_set(self, name):
        return CustomSet(name, prefix=self._prefix)


class CustomSet(SetBase):

    def __init__(self, name, prefix="/"):
        # user should guarantee existence

        self._path = os.path.join(self._prefix, "etc", "portage", "sets", name)

    @property
    def filepath(self):
        return self._path

    def get_package_names(self):
        return _read(self._path)

    def add_packages(self, package_names):
        _add(self._path, package_names)

    def remove_packages(self, package_names, check=True):
        _remove(self._path, package_names, check)


class World(SetBase):

    def __init__(self, prefix="/"):
        # user should guarantee existence

        self._prefix = prefix
        self._path = os.path.join(self._prefix, "var", "lib", "portage", "world")
        self._setPath = os.path.join(self._prefix, "var", "lib", "portage", "world_sets")

    @property
    def world_filepath(self):
        return self._path

    @property
    def world_sets_filepath(self):
        return self._setPath

    def get_package_names(self):
        ret = set()

        try:
            ret |= set(_read(self._path))
        except FileNotFoundError:
            pass

        for sn in _read(self._setPath):
            ret |= set(CustomSet(sn, prefix=self._prefix).get_packages())

        return sorted(list(ret))

    def get_set_names(self):
        return _read(self._setPath)

    def add_packages(self, package_names):
        _add(self._path, package_names)

    def remove_packages(self, package_names, check=True):
        assert check
        _remove(self._path, package_names, check)

    def add_set(self, set_name):
        self.add_sets([set_name])

    def add_sets(self, *set_names):
        setList2 = self.get_sets()
        for x in set_names:
            if x not in setList2:
                setList2.append(x)
        _write(self._setPath, sorted(setList2))

    def remove_set(self, set_name):
        self.remove_set([set_name])

    def remove_sets(self, *set_names):
        setList2 = self.get_sets()
        for x in set_names:
            i = setList2.find(x)
            if i >= 0:
                setList2.pop(i)
        _write(self._setPath, setList2)


def _read(fullfn):
    try:
        itemList = pathlib.Path(fullfn).read_text().split("\n")
        return [x for x in itemList if x != ""]
    except FileNotFoundError:
        return []


def _write(fullfn, itemList):
    with open(fullfn, "w") as f:
        for pkg in itemList:
            f.write(pkg + "\n")


def _add(fullfn, newItemList):
    itemList = _read(fullfn)
    for x in newItemList:
        if x not in itemList:
            itemList.append(x)
    _write(fullfn, sorted(itemList))


def _remove(fullfn, newItemList, bCheck):
    itemList = _read(fullfn)
    for x in newItemList:
        i = itemList.find(x)
        if not bCheck and i < 0:
            continue
        itemList.pop(i)
    _write(fullfn, itemList)
