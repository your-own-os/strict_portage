#!/usr/bin/python3
# -*- coding: utf-8; tab-width: 4; indent-tabs-mode: t -*-

import glob
import pathlib

try:
    # what to insert (with blank line in the beginning and the end)
    buf2 = r"""
# we don't use kmod-static-nodes
find "${D}" -name "*static-nodes*" | xargs rm -rf
find "${D}" -name "*systemd-tmpfiles-setup-dev*" | xargs rm -rf
sed -i -E ':x; /\\$/ { N; s/\\\n +//; tx }'   ${D}/usr/lib/udev/rules.d/{50-udev-default,70-uaccess}.rules                                          # combind lines ending with \ to one line
sed -i -E 's/, OPTIONS\+="static_node=.+"//g' ${D}/usr/lib/udev/rules.d/*.rules                                                                     # remove rule parts containing "static-nodes"
sed -E '/^#.*static[_-]node/d' ${D}/usr/lib/udev/rules.d/50-udev-default.rules | cat -s > ${D}/usr/lib/udev/rules.d/50-udev-default.rules.2         # remove comments containing "static-nodes"
mv ${D}/usr/lib/udev/rules.d/50-udev-default.rules.2 ${D}/usr/lib/udev/rules.d/50-udev-default.rules
## end ####"""
    buf2 = buf2.replace("\n", "\n\t")
    buf2 += "\n"

    for fn in glob.glob("*.ebuild"):
        buf = pathlib.Path(fn).read_text()

        # insert to the end of src_install()
        pos = buf.find("multilib_src_install_all() {")
        if pos == -1:
            raise ValueError()
        pos = buf.find("\n}\n", pos)
        if pos == -1:
            raise ValueError()
        pos += 1

        # do insert
        buf = buf[:pos] + buf2 + buf[pos:]
        with open(fn, "w") as f:
            f.write(buf)
except ValueError:
    print("outdated")
