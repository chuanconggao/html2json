#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import *

import re

_reCleaner = re.compile(r"(s)?(?P<sep>\W)((?:(?!(?P=sep)).)*)(?P=sep)(?:((?:(?!(?P=sep)).)*)(?P=sep)(g)?)?")

def _extract(root, selector, prop, cleaners):
    try:
        if selector == "":
            tag = root
        else:
            tag = root.select(selector)[0]
    except:
        return None

    if prop is None:
        v = ''.join(str(c) for c in tag.contents if isinstance(c, str)).strip()
        if v == "":
            v = tag.text.strip()
    else:
        v = tag[prop].strip()

    for c in cleaners:
        m = _reCleaner.match(c)
        if m.group(1) == "s":
            v = re.sub(m.group(3), m.group(4), v, count=(0 if m.group(5) == "g" else 1))
        else:
            v = re.search(m.group(3), v).group(0)

    return v

def collect(root, template):
    def collect_rec(root, template, data):
        for (t, s) in template.items():
            if isinstance(s, dict):
                data[t] = {}
                collect_rec(root, s, data[t])
            elif isinstance(s, list) and len(s) == 1:
                data[t] = []
                for cRoot in root.select(s[0][0]):
                    data[t].append({})
                    collect_rec(cRoot, s[0][1], data[t][-1])
            else:
                v = _extract(root, s[0], s[1], s[2])

                if v is not None:
                    data[t] = v

    data = {}
    collect_rec(root, template, data)
    return data
