#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import os
import re
import glob
import pathlib

try:
    for fn in glob.glob("*.ebuild"):
        if "9999" in fn:
            # 9999 version does not depends on virtualbox-modules, but it builds kernel modules, so we have to delete it
            os.unlink(fn)
        else:
            buf = pathlib.Path(fn).read_text()
            m = re.search(".*app-emulation/virtualbox-modules-.*", buf, re.M)
            if m is None:
                raise ValueError(fn)
            buf = buf.replace(m.group(0), "")
            with open(fn, "w") as f:
                f.write(buf)
except ValueError as e:
    print("outdated " + str(e))
