html2json
====

[![PyPI version](https://badge.fury.io/py/html2json.svg)](https://badge.fury.io/py/html2json)

Convert a HTML webpage to JSON data using a template defined in JSON.

Installation
----

This package is available on PyPi. Just use `pip install -U html2json` to install it. Then you can import it using `from html2json import html2json`.

API
----

The method is `collect(root, template)`. `root` is the root element of the page derived by [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/) and `template` is the loaded JSON object of the template.

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

- To extract a list of sub-entries following the same sub-template, the list syntax is `keyName: [[subRoot, subTemplate]]`. `subRoot` is the CSS selector of the new root for each sub entry. `subTemplate` is the sub-template for each entry, recursively.

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
