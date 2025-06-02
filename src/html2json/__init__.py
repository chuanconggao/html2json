from __future__ import annotations

import json
import re
from re import Match, Pattern
from typing import Any, cast

from pyquery import PyQuery

Template = dict[str, Any]
Data = dict[str, Any]

__CLEANER_REGEX: Pattern = re.compile(r"(?P<mode>s)?(?P<sep>\W)(?P<search>(?:(?!(?P=sep)).)*)(?P=sep)(?:(?P<sub>(?:(?!(?P=sep)).)*)(?P=sep)(?P<flag>g)?)?")  # noqa: E501


__TEXT_NODES_SELECTOR_REGEX: Pattern = re.compile(r"(?P<selector>.+ +)?::text")

__NEW_LINE_WHITESPACES_REGEX: Pattern = re.compile(r"\s*\n+\s*")
__LEADING_TRAILING_WHITESPACES_REGEX: Pattern = re.compile(r"^[^\S\n]+|[^\S\n]+$")


def __get_tags(
    root: PyQuery,
    selector: str | None = None,
) -> PyQuery | None:
    try:
        tags: PyQuery = root.find(selector) if selector else root
        # Non-matching selector
        if len(tags) == 0:
            return None
    except:  # noqa: E722
        # Invalid selector
        return None

    return tags


def __clean(
    v: str,
    cleaners: list[str] | None = None,
) -> str:
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

    return v


def __extract_text_nodes(
    root: PyQuery,
    selector: str | None = None,
    cleaners: list[str] | None = None,
) -> str | list[str] | None:
    tags: PyQuery | None = __get_tags(root, selector)
    if not tags:
        return None

    results: list[str] = []

    # Must use `.items()` which returns `PyQuery` objects
    for tag in tags.items():
        results.extend([
            __clean(
                __LEADING_TRAILING_WHITESPACES_REGEX.sub(
                    r" ",
                    __NEW_LINE_WHITESPACES_REGEX.sub(r"\n", e),
                ),
                cleaners,
            )
            for e in tag.contents()
            if isinstance(e, str)
        ])

    return results if len(results) > 1 else results[0]


def __extract(
    root: PyQuery,
    selector: str | None = None,
    prop: str | None = None,
    cleaners: list[str] | None = None,
) -> str | list[str] | None:
    # CSS standard does not support text node yet
    # https://github.com/w3c/csswg-drafts/issues/2208
    # Ideally, we should customize `cssselect` to add support for this new pseudo-class
    # https://cssselect.readthedocs.io/en/latest/#customizing-the-translation
    if selector and (
        text_nodes_selector_match := __TEXT_NODES_SELECTOR_REGEX.fullmatch(selector)
    ):
        if prop:
            return None

        return __extract_text_nodes(
            root,
            text_nodes_selector_match.group("selector").strip(),
            cleaners,
        )

    tags: PyQuery | None = __get_tags(root, selector)
    if tags is None:
        return None

    results: list[str] = []

    # Must use `.items()` which returns `PyQuery` objects
    for tag in tags.items():
        v: str = str(
            tag.attr(prop) if prop
            else tag.text(),
        ).strip()

        results.append(__clean(v, cleaners))

    return results if len(results) > 1 else results[0]


def __collect_keys(root: PyQuery, key_template: str) -> list[str]:
    if key_template[0] == '[' and key_template[-1] == "]":
        keys: str | list[str] = __extract(root, *json.loads(key_template)) or []
        return keys if isinstance(keys, list) else [keys]

    return [key_template]


def __expand_template(root: PyQuery, template: Template) -> Template:
    return {
        key: value
        for key_template, value in template.items()
        for key in __collect_keys(root, key_template)
    }


def collect(html: str, template: Template) -> Data:
    def collect_rec(root: PyQuery, template: Template, data: Data) -> None:
        for (t, s) in __expand_template(root, template).items():
            if isinstance(s, dict):
                data[t] = {}
                collect_rec(root, s, data[t])
            elif isinstance(s, list):
                if len(s) == 1 and isinstance(s[0], list):
                    sub_selector, sub_template = s[0] if len(s[0]) > 1 else (s[0][0], None)
                    sub_selector = sub_selector.format(key=t) if sub_selector else None

                    data[t] = []
                    # Must use `.items()` which returns `PyQuery` objects
                    for sub_root in root.find(sub_selector).items():
                        if sub_template:
                            data[t].append({})
                            collect_rec(sub_root, sub_template, data[t][-1])
                        else:
                            data[t].append(__extract(sub_root))
                elif len(s) == 2 and isinstance(s[1], dict):
                    sub_selector, sub_template = s[0], s[1]
                    sub_selector = sub_selector.format(key=t) if sub_selector else None

                    data[t] = {}
                    collect_rec(root.find(sub_selector), sub_template, data[t])
                else:
                    data[t] = (
                        __extract(root, s[0].format(key=t) if s[0] else None, *s[1:]) if s
                        else __extract(root)
                    )
            elif isinstance(s, str):
                data[t] = __extract(root, s.format(key=t))
            elif s is None:
                data[t] = __extract(root)

    data: Data = {}
    collect_rec(PyQuery(html), template, data)

    return data
