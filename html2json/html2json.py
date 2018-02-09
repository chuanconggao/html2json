#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import *

import re

from pyquery import PyQuery

__reCleaner = re.compile(r"(?P<mode>s)?(?P<sep>\W)(?P<search>(?:(?!(?P=sep)).)*)(?P=sep)(?:(?P<sub>(?:(?!(?P=sep)).)*)(?P=sep)(?P<flag>g)?)?")

def __extract(root, selector, prop, cleaners):
    try:
        tag = root.find(selector) if selector else root
    except:
        return None

    if prop:
        v = tag.attr(prop)
    else:
        v = ''.join(c for c in tag.contents() if isinstance(c, str))
        if v == "":
            v = tag.text()

    v = v.strip()

    for c in cleaners:
        m = __reCleaner.match(c)

        v = (
            re.sub(m.group("search"), m.group("sub"), v, count=(0 if m.group("flag") == "g" else 1))
            if m.group("mode") == "s"
            else re.search(m.group("search"), v).group(0)
        )

    return v


def collect(html, template):
    def collect_rec(root, template, data):
        for (t, s) in template.items():
            if isinstance(s, dict):
                data[t] = {}
                collect_rec(root, s, data[t])
            elif isinstance(s, list) and len(s) == 1:
                subSelector, subTemplate = s[0]

                data[t] = []
                for subRoot in root.find(subSelector):
                    data[t].append({})
                    collect_rec(subRoot, subTemplate, data[t][-1])
            else:
                v = __extract(root, *s)

                if v is not None:
                    data[t] = v


    data = {}
    collect_rec(PyQuery(html), template, data)

    return data
