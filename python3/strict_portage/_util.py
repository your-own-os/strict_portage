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
import time
import shutil
import pathlib
import platform
import itertools
import subprocess


class Util:

    @staticmethod
    def forceRemoveFromList(lst, element):
        try:
            lst.remove(element)
        except ValueError:
            pass

    @staticmethod
    def doNothing(msg):
        pass

    @staticmethod
    def getTmpPathInPlace(path):
        path2 = None
        for i in itertools.count(2):
            path2 = "%s.%d" % (path, i)
            if not os.path.exists(path2):
                return path2

    @staticmethod
    def getInnerFileFullfn(dirpath, innerFileName):
        fullfn = os.path.join(dirpath, innerFileName)
        if not os.path.exists(fullfn):
            return innerFileName
        for i in itertools.count(2):
            fullfn = os.path.join(dirpath, "%s-%d" % (innerFileName, i))
            if not os.path.exists(fullfn):
                return fullfn

    @staticmethod
    def isUnderDir(path, dir, bAllowSame=False):
        assert os.path.isabs(path) and os.path.isabs(dir)

        if bAllowSame:
            if dir == "/":
                return path.startswith("/")
            else:
                return path == dir or path.startswith(dir + "/")
        else:
            if dir == "/":
                return len(path) > 1 and path.startswith("/")
            else:
                return path.startswith(dir + "/")

    @classmethod
    def safeFileToDir(cls, path, innerFileName):
        path2 = cls.getTmpPathInPlace(path)
        os.mkdir(path2)
        os.rename(path, cls.getInnerFileFullfn(path2, innerFileName))
        os.rename(path2, path)

    @staticmethod
    def fileOrDirGetFileList(path):
        fullfnList = []
        if os.path.isfile(path):
            fullfnList.append(path)
        else:
            for fn in sorted(os.listdir(path)):
                fullfnList.append(os.path.join(path, fn))
        return fullfnList

    @staticmethod
    def advGetFileList(dirName, level, typeList):
        """typeList is a string, value range is "d,f,l,a"
           returns basename"""

        ret = []
        for fbasename in os.listdir(dirName):
            fname = os.path.join(dirName, fbasename)

            if os.path.isdir(fname) and level - 1 > 0:
                for i in Util.advGetFileList(fname, level - 1, typeList):
                    ret.append(os.path.join(fbasename, i))
                continue

            appended = False
            if not appended and ("a" in typeList or "d" in typeList) and os.path.isdir(fname):         # directory
                ret.append(fbasename)
            if not appended and ("a" in typeList or "f" in typeList) and os.path.isfile(fname):        # file
                ret.append(fbasename)
            if not appended and ("a" in typeList or "l" in typeList) and os.path.islink(fname):        # soft-link
                ret.append(fbasename)

        return ret

    @staticmethod
    def repoIsSysFile(fbasename):
        """fbasename value is like "sys-devel", "sys-devel/gcc", "profiles", etc"""

        if fbasename.startswith("."):
            return True
        if fbasename == "licenses" or fbasename.startswith("licenses/"):
            return True
        if fbasename == "metadata" or fbasename.startswith("metadata/"):
            return True
        if fbasename == "profiles" or fbasename.startswith("profiles/"):
            return True
        if fbasename == "eclass" or fbasename.startswith("eclass/"):
            return True
        return False

    @staticmethod
    def readListBuffer(buf):
        ret = []
        for line in buf.split("\n"):
            idx = line.find("#")
            if idx >= 0:
                line = line[:idx]
            line = line.strip()
            if line == "":
                continue
            ret.append(line)
        return ret

    @classmethod
    def readListFile(cls, path):
        return cls.readListBuffer(pathlib.Path(path).read_text())

    @staticmethod
    def genListBuffer(lines):
        ret = ""
        for line in sorted(lines):
            ret += "%s\n" % (line)
        return ret

    @staticmethod
    def realPathSplit(path):
        """os.path.split() only split a path into 2 component, I believe there are reasons, but it is really inconvenient.
           So I write this function to split a unix path into basic components.
           Reference: http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python"""

        folders = []
        while True:
            path, folder = os.path.split(path)
            if folder != "":
                folders.append(folder)
            else:
                if path != "":
                    folders.append(path)
                break
        if path.startswith("/"):
            folders.append("")
        folders.reverse()
        return folders

    @staticmethod
    def getCpuArch():
        ret = platform.machine()
        if ret == "x86_64":
            return "amd64"
        else:
            return ret

    @staticmethod
    def isArchCompatible(targetArch, curArch):
        if targetArch == curArch:
            return True
        if targetArch == "i386" and curArch == "amd64":
            return True
        return False

    @staticmethod
    def listStartswith(theList, subList):
        return len(theList) >= len(subList) and theList[:len(subList)] == subList

    @staticmethod
    def forceDelete(path):
        if os.path.islink(path):
            os.remove(path)
        elif os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.lexists(path):
            os.remove(path)             # other type of file, such as device node
        else:
            pass                        # path does not exist, do nothing

    @staticmethod
    def forceSymlink(target, link_path):
        if os.path.islink(link_path) and os.readlink(link_path) == target:      # already exist
            return
        Util.forceDelete(link_path)                   # os.symlink won't overwrite anything, so we delete it first
        os.symlink(target, link_path)

    @staticmethod
    def removeDirContentExclude(dirPath, excludeList):
        for fn in os.listdir(dirPath):
            if fn not in excludeList:
                Util.forceDelete(os.path.join(dirPath, fn))

    @staticmethod
    def pathCompare(path1, path2):
        # Change double slashes to slash
        path1 = re.sub(r"//", r"/", path1)
        path2 = re.sub(r"//", r"/", path2)
        # Removing ending slash
        path1 = re.sub("/$", "", path1)
        path2 = re.sub("/$", "", path2)

        if path1 == path2:
            return 1
        return 0

    @staticmethod
    def isMount(path):
        """Like os.path.ismount, but also support bind mounts"""
        if os.path.ismount(path):
            return 1
        a = os.popen("mount")
        mylines = a.readlines()
        a.close()
        for line in mylines:
            mysplit = line.split()
            if Util.pathCompare(path, mysplit[2]):
                return 1
        return 0

    @staticmethod
    def isInstanceList(obj, *instances):
        for inst in instances:
            if isinstance(obj, inst):
                return True
        return False

    @staticmethod
    def cmdCall(cmd, *kargs):
        # call command to execute backstage job
        #
        # scenario 1, process group receives SIGTERM, SIGINT and SIGHUP:
        #   * callee must auto-terminate, and cause no side-effect
        #   * caller must be terminated by signal, not by detecting child-process failure
        # scenario 2, caller receives SIGTERM, SIGINT, SIGHUP:
        #   * caller is terminated by signal, and NOT notify callee
        #   * callee must auto-terminate, and cause no side-effect, after caller is terminated
        # scenario 3, callee receives SIGTERM, SIGINT, SIGHUP:
        #   * caller detects child-process failure and do appopriate treatment

        ret = subprocess.run([cmd] + list(kargs),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True)
        if ret.returncode > 128:
            # for scenario 1, caller's signal handler has the oppotunity to get executed during sleep
            time.sleep(1.0)
        if ret.returncode != 0:
            print(ret.stdout)
            ret.check_returncode()
        return ret.stdout.rstrip()

    @staticmethod
    def shellCall(cmd):
        # call command with shell to execute backstage job
        # scenarios are the same as FmUtil.cmdCall

        ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             shell=True, text=True)
        if ret.returncode > 128:
            # for scenario 1, caller's signal handler has the oppotunity to get executed during sleep
            time.sleep(1.0)
        if ret.returncode != 0:
            print(ret.stdout)
            ret.check_returncode()
        return ret.stdout.rstrip()

    @staticmethod
    def cmdCallIgnoreResult(cmd, *kargs):
        ret = subprocess.run([cmd] + list(kargs),
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True)
        if ret.returncode > 128:
            time.sleep(1.0)

    @staticmethod
    def portageIsPkgInstalled(rootDir, pkg):
        dir = os.path.join(rootDir, "var", "db", "pkg", os.path.dirname(pkg))
        if os.path.exists(dir):
            for fn in os.listdir(dir):
                if fn.startswith(os.path.basename(pkg)):
                    return True
        return False

    @staticmethod
    def portageIsPkgName(pkgAtom):
        return pkgAtom[0] not in ["<", ">", "=", "!", "~"]

    @staticmethod
    def portagePkgNameFromPkgAtom(pkgAtom):
        pkgName = pkgAtom

        while pkgName[0] in ["<", ">", "=", "!", "~"]:
            pkgName = pkgName[1:]

        i = 0
        while i < len(pkgName):
            if pkgName[i] == "-" and i < len(pkgName) - 1 and pkgName[i + 1].isdigit():
                pkgName = pkgName[:i]
                break
            i = i + 1

        return pkgName


class EntryDict(dict):

    def __init__(self, entryList=[]):
        super().__init__()
        for k, vAsList in entryList:
            assert k not in self
            assert len(set(vAsList)) == len(vAsList)
            self[k] = set(vAsList)

    def mergeEntry(self, k, vAsList):
        if k not in self:
            self[k] = set()
        self[k] |= set(vAsList)

    def mergeEntryDict(self, entryDict):
        for k, vAsList in entryDict.items():
            if k not in self:
                self[k] = set()
            self[k] |= set(vAsList)

    def toEntryList(self):
        ret = []
        for k in sorted(self.keys()):
            ret.append((k, sorted(self[k])))
        return ret
