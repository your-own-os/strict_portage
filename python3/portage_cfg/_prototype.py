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
import abc


class SetBase(abc.ABC):

    @abc.abstractmethod
    def get_package_names(self):
        pass

    def add_package(self, package_name):
        self.add_packages([package_name])

    @abc.abstractmethod
    def add_packages(self, package_names):
        pass

    def remove_package(self, package_name):
        self.remove_packages([package_name])

    @abc.abstractmethod
    def remove_packages(self, package_names, check=True):
        pass


class ConfigFileOrDir:

    def __init__(self, path, fileClass):
        self._path = path
        self._fileClass = fileClass

    def is_file_or_directory(self):
        if os.path.isdir(self._path):
            return False
        if os.path.isfile(self._path):
            return True
        assert False

    def get_file_object(self):
        assert os.path.isfile(self._path)
        return self._fileClass(self._path)

    def get_file_objects(self):
        assert os.path.isdir(self._path)
        return [self._fileClass(os.path.join(self._path, x)) for x in os.listdir(self._path)]
