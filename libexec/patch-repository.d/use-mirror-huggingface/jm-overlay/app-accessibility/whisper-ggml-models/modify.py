#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import glob
import pathlib

try:
    for fn in sorted(glob.glob("*.ebuild"), reverse=True):
        buf = pathlib.Path(fn).read_text()
        buf = buf.replace('( https://huggingface.co/', '( mirror://hf-co/')
        with open(fn, "w") as f:
            f.write(buf)
except ValueError:
    print("outdated")
