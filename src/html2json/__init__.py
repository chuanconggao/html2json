from __future__ import annotations

import re
from re import Match, Pattern
from typing import Any, cast

from pyquery import PyQuery

Template = dict[str, Any]
Data = dict[str, Any]

__CLEANER_REGEX: Pattern = re.compile(r"(?P<mode>s)?(?P<sep>\W)(?P<search>(?:(?!(?P=sep)).)*)(?P=sep)(?:(?P<sub>(?:(?!(?P=sep)).)*)(?P=sep)(?P<flag>g)?)?")  # noqa: E501


def __extract(
    root: PyQuery,
    selector: str | None = None,
    prop: str | None = None,
    cleaners: list[str] | None = None,
) -> str | list[str] | None:
    try:
        tags: PyQuery = root.find(selector) if selector else root
        # Non-matching selector
        if len(tags) == 0:
            return None
    except:  # noqa: E722
        # Invalid selector
        return None

    results: list[str] = []

    # Must use `.items()` which returns `PyQuery` objects
    for tag in tags.items():
        v: str = str(
            tag.attr(prop) if prop
            else tag.text(),
        ).strip()

        for c in cleaners or []:
            m: Match = cast("Match", __CLEANER_REGEX.match(c))

            v = (
                re.sub(
                    m.group("search"),
                    m.group("sub"),
                    v,
                    count=(0 if m.group("flag") == "g" else 1),
                ) if m.group("mode") == "s"
                else cast("Match", re.search(m.group("search"), v)).group(0)
            )

        results.append(v)

    return results if len(results) > 1 else results[0]


def collect(html: str, template: Template) -> Data:
    def collect_rec(root: PyQuery, template: Template, data: Data) -> None:
        for (t, s) in template.items():
            if isinstance(s, dict):
                data[t] = {}
                collect_rec(root, s, data[t])
            elif isinstance(s, list):
                if len(s) == 1 and isinstance(s[0], list):
                    sub_selector, sub_template = s[0]

                    data[t] = []
                    # Must use `.items()` which returns `PyQuery` objects
                    for sub_root in root.find(sub_selector).items():
                        data[t].append({})
                        collect_rec(sub_root, sub_template, data[t][-1])
                elif len(s) == 2 and isinstance(s[1], dict):
                    sub_selector, sub_template = s[0], s[1]

                    data[t] = {}
                    collect_rec(root.find(sub_selector), sub_template, data[t])
                else:
                    data[t] = __extract(root, *s)

    data: Data = {}
    collect_rec(PyQuery(html), template, data)

    return data
