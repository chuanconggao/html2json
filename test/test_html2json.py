import json

from html2json import collect

html1 = """
<html>
    <body>
        <h1>Hello!</h1>
        I am <span>Bob</span>.

        <img alt="image" src="http://localhost/img.png"/>
    </body>
</html>
"""

html2 = """
<html>
    <body>
        <div id="alpha" class="item">
            alpha
            <img src="alpha.png"/>
        </div>
        <div id="beta" class="item">
            beta
            <img src="beta.png"/>
        </div>
        <div id="gamma" class="item">
            gamma
            <img src="gamma.png"/>
        </div>
    </body>
</html>
"""

html3 = """
<html>
    <body>
        The quick brown fox
        jumps over
        the lazy dog.
    </body>
</html>
"""

html4 = """
<html>
    <body>
        The <b>quick brown fox</b>
        jumps over
        the <b>lazy dog</b>.
    </body>
</html>
"""


def test_basic() -> None:
    assert collect(html1, {
        "text": [],
    }) == collect(html1, {
        "text": None,
    }) == {
        "text": "Hello!\nI am Bob.",
    }

    assert collect(html1, {
        "title": ["body h1"],
    }) == collect(html1, {
        "title": "body h1",
    }) == {
        "title": "Hello!",
    }

    assert collect(html1, {
        # Invalid selector syntax
        "title": ["body / h1"],
    }) == collect(html1, {
        "title": ["body h2"],
    }) == {
        "title": None,
    }

    assert collect(html1, {
        "img.alt": ["body img", "alt"],
    }) == {
        "img.alt": "image",
    }

    assert collect(html1, {
        "text": [None, None, ["s/\\s+/ /g"]],
    }) == collect(html1, {
        "text": [None, None, ["s|\\s+| |g"]],
    }) == collect(html1, {
        "text": ["body", None, ["s/\\s+/ /g"]],
    }) == collect(html1, {
        "text": ["body", None, ["s|\\s+| |g"]],
    }) == {
        "text": "Hello! I am Bob.",
    }

    assert collect(html1, {
        "img.src": ["body img", "src", ["/\\w+\\.png$/"]],
    }) == collect(html1, {
        "img.src": ["body img", "src", ["|\\w+\\.png$|"]],
    }) == {
        "img.src": "img.png",
    }


def test_basic_multiple() -> None:
    assert collect(html2, {
        "items": [".item"],
    }) == {
        "items": [
            "alpha",
            "beta",
            "gamma",
        ],
    }


def test_nested() -> None:
    assert collect(html1, {
        "body": {
            "title": ["body h1"],
        },
    }) == collect(html1, {
        "body": ["body", {
            "title": ["h1"],
        }],
    }) == {
        "body": {
            "title": "Hello!",
        },
    }


def test_multiple() -> None:
    assert collect(html2, {
        "items": [".item"],
    }) == collect(html2, {
        "items": [[".item"]],
    }) == collect(html2, {
        "items": [[".item", None]],
    }) == {
        "items": [
            "alpha",
            "beta",
            "gamma",
        ],
    }

    assert collect(html2, {
        "items": [[".item", {
            "text": [],
            "img.src": ["img", "src"],
        }]],
    }) == {
        "items": [
            {
                "text": "alpha",
                "img.src": "alpha.png",
            },
            {
                "text": "beta",
                "img.src": "beta.png",
            },
            {
                "text": "gamma",
                "img.src": "gamma.png",
            },
        ],
    }


def test_key_matching() -> None:
    assert collect(html1, {
        json.dumps(["p"]): [],
    }) == {}

    assert collect(html1, {
        json.dumps(["span"]): [],
    }) == {
        "Bob": "Hello!\nI am Bob.",
    }

    assert collect(html2, {
        "items": [[".item", {
            json.dumps([]): {
                "img.src": ["img", "src"],
            },
        }]],
    }) == {
        "items": [
            {
                "alpha": {
                    "img.src": "alpha.png",
                },
            },
            {
                "beta": {
                    "img.src": "beta.png",
                },
            },
            {
                "gamma": {
                    "img.src": "gamma.png",
                },
            },
        ],
    }


def test_key_replace() -> None:
    assert collect(html2, {
        "items": {
            json.dumps([".item"]): ["#{key}", {
                "img.src": ["img", "src"],
            }],
        },
    }) == {
        "items": {
            "alpha": {
                "img.src": "alpha.png",
            },
            "beta": {
                "img.src": "beta.png",
            },
            "gamma": {
                "img.src": "gamma.png",
            },
        },
    }


def test_text_nodes() -> None:
    assert collect(html1, {
        "text": ["body ::text"],
    }) == {
        "text": ["\n", "\nI am ", ".\n", "\n"],
    }

    assert collect(html1, {
        "text": ["body h1 ::text"],
    }) == {
        "text": "Hello!",
    }

    assert collect(html2, {
        "text": ["body .item ::text"],
    }) == {
        "text": ["\nalpha\n", "\n", "\nbeta\n", "\n", "\ngamma\n", "\n"],
    }

    assert collect(html2, {
        "text": ["body .item#alpha ::text"],
    }) == {
        "text": ["\nalpha\n", "\n"],
    }

    assert collect(html3, {
        "text": ["body ::text"],
    }) == {
        "text": "\nThe quick brown fox\njumps over\nthe lazy dog.\n",
    }

    assert collect(html4, {
        "text": ["body ::text"],
    }) == {
        "text": [
            "\nThe ",
            "\njumps over\nthe ",
            ".\n",
        ],
    }
