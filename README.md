html2json
====

[![PyPI version](https://badge.fury.io/py/html2json.svg)](https://badge.fury.io/py/html2json)

Convert a HTML webpage to JSON data using a template defined in JSON.

Installation
----

This package is available on PyPi. Just use `pip install -U html2json` to install it. Then you can import it using `from html2json import collect`.

API
----

The method is `collect(html, template)`. `html` is the HTML of page loaded as string, and `template` is the JSON of template loaded as Python objects.

Note that the HTML must contain the root node, like `<html>...</html>` or `<div>...</div>`. The root node itself cannot be matched.

Template Syntax
----

- The basic syntax is `keyName: [cssSelector, attribute, [listOfRegexes]]`. The list of regexes supports two forms of regex operations. The operations with in the list are executed sequentially.
    - Replacement: `s/regex/replacement/g`. `g` is optional for multiple replacements.
    - Extraction: `/regex/`.

For example:

```json
{
    "Color": ["head link:nth-of-type(1)", "href", ["/\\w+(?=\\.css)/"]],
}
```

- As JSON, nested structure can be easily constructed.

```json
{
    "Cover": {
        "URL": [".cover img", "src", []],
        "Number of Favorites": [".cover .favorites", "value", []]
    },
}
```

An alternative simplified syntax `keyName: [subRoot, subTemplate]` can be used. `subRoot` a CSS selector of the new root for each sub entry. `subTemplate` is a sub-template for each entry, recursively.

For example, the previous example can be simplified as follow.

```json
{
    "Cover": [".cover", {
        "URL": ["img", "src", []],
        "Number of Favorites": [".favorites", "value", []]
    }],
}
```

- To extract a list of sub-entries following the same sub-template, the list syntax is `keyName: [[subRoot, subTemplate]]`. `subRoot` is the CSS selector of the new root for each sub entry. `subTemplate` is the sub-template for each entry, recursively. Please note the difference (surrounding `[` and `]`) from the previous syntax above.

For example:

```json
{
    "Comments": [[".comments", {
        "From": [".from", null, []],
        "Content": [".content", null, []],
        "Photos": [[".content img", {
            "URL": ["", "src", []]
        }]]
    }]]
}
```
