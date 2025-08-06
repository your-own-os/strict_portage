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
import pathlib
from ._prototype import ConfigFileBase
from ._prototype import ConfigFileCheckerBase


class MakeConf(ConfigFileBase):

    def __init__(self, prefix="/"):
        super().__init__(os.path.join(prefix, "etc", "portage", "make.conf"),
                         MakeConfChecker)

    def merge_content(self, content):
        # FIXME
        assert False

    def has_var(self, var_name):
        buf = pathlib.Path(self._path).read_text()
        m = re.search("^%s=\"(.*)\"$" % (var_name), buf, re.MULTILINE)
        return m is not None

    def get_var(self, var_name, parse=False):
        # parse is True:
        #     returns parsed variable value, returns appropriate default value when not found
        #     multiline variable definition is not supported yet
        # parse is False:
        #     returns raw variable value, returns "" when not found
        #     multiline variable definition is not supported yet

        if parse:
            if var_name in ["FEATURES", "ACCEPT_KEYWORDS"]:
                value = self._get_var(var_name)
                return value.split(" ") if value != "" else []

        return self._get_var(var_name)

    def set_var(self, var_name, *value, synthesize=False):
        # create or set variable in make.conf
        # multiline variable definition is not supported yet

        if synthesize:
            if var_name in ["FEATURES", "ACCEPT_KEYWORDS"]:
                assert len(value) == 1
                self._set_var(var_name, " ".join(*value))
                return

        assert len(value) == 1
        self._set_var(var_name, *value)

    def update_var_as_value_set(self, var_name, value_list):
        # Check variable in make.conf
        # Create or set variable in make.conf

        endEnter = False
        buf = ""
        with open(self._path, 'r') as f:
            buf = f.read()
            if buf[-1] == "\n":
                endEnter = True

        m = re.search("^%s=\"(.*)\"$" % (var_name), buf, re.MULTILINE)
        if m is not None:
            if set(m.group(1).split(" ")) != set(value_list):
                newLine = "%s=\"%s\"" % (var_name, " ".join(value_list))
                buf = buf.replace(m.group(0), newLine)
                with open(self._path, 'w') as f:
                    f.write(buf)
        else:
            with open(self._path, 'a') as f:
                if not endEnter:
                    f.write("\n")
                f.write("%s=\"%s\"\n" % (var_name, " ".join(value_list)))

    def remove_var(self, var_name):
        # Remove variable in make.conf
        # Multiline variable definition is not supported yet

        endEnterCount = 0
        lineList = []
        with open(self._path, 'r') as f:
            buf = f.read()
            endEnterCount = len(buf) - len(buf.rstrip("\n"))

            buf = buf.rstrip("\n")
            for line in buf.split("\n"):
                if re.search("^%s=" % (var_name), line) is None:
                    lineList.append(line)

        buf = ""
        for line in lineList:
            buf += line + "\n"
        buf = buf.rstrip("\n")
        for i in range(0, endEnterCount):
            buf += "\n"

        with open(self._path, 'w') as f:
            f.write(buf)

    def _get_var(self, var_name):
        buf = pathlib.Path(self._path).read_text()
        m = re.search("^%s=\"(.*)\"$" % (var_name), buf, re.MULTILINE)
        if m is None:
            return ""
        varVal = m.group(1)

        while True:
            m = re.search("\\${(\\S+)?}", varVal)
            if m is None:
                break
            varName2 = m.group(1)
            varVal2 = self._get_var(varName2)
            if varVal2 is None:
                varVal2 = ""

            varVal = varVal.replace(m.group(0), varVal2)

        return varVal

    def _set_var(self, var_name, value):
        buf = pathlib.Path(self._path).read_text()
        endEnter = (buf[-1] == "\n")

        m = re.search("^%s=\"(.*)\"$" % (var_name), buf, re.MULTILINE)
        if m is not None:
            if m.group(1) != value:
                newLine = "%s=\"%s\"" % (var_name, value)
                buf = buf.replace(m.group(0), newLine)
                with open(self._path, 'w') as f:
                    f.write(buf)
        else:
            with open(self._path, 'a') as f:
                if not endEnter:
                    f.write("\n")
                f.write("%s=\"%s\"\n" % (var_name, value))


class MakeConfChecker(ConfigFileCheckerBase):

    def __init__(self, parent, bAutoFix, errorCallback):
        super().__init__(parent, bAutoFix, errorCallback)

    def check(self):
        if self._basic_check():
            return

        # check CHOST variable
        if self._obj.has_var("CHOST"):
            self._errorCallback("variable CHOST should not exist in %s" % (self._obj.path))

        # check/fix DISTDIR variable
        if self._obj.has_var("DISTDIR"):
            if not os.path.isdir(self._obj.path):
                # FIXME
                pass
