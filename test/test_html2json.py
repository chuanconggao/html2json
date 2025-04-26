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
        <div class="item">
            alpha
            <img src="alpha.png"/>
        </div>
        <div class="item">
            beta
            <img src="beta.png"/>
        </div>
        <div class="item">
            gamma
            <img src="gamma.png"/>
        </div>
    </body>
</html>
"""


def test_basic() -> None:
    assert collect(html1, {
        "text": [],
    }) == {
        "text": "Hello!\nI am Bob.",
    }

    assert collect(html1, {
        "title": ["body h1"],
    }) == {
        "title": "Hello!",
    }

    assert collect(html1, {
        "title": ["body / h1"],
    }) == {
        "title": None,
    }

    assert collect(html1, {
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
    }) == {
        "text": "Hello! I am Bob.",
    }
    assert collect(html1, {
        "text": [None, None, ["s|\\s+| |g"]],
    }) == {
        "text": "Hello! I am Bob.",
    }

    assert collect(html1, {
        "text": ["body", None, ["s/\\s+/ /g"]],
    }) == {
        "text": "Hello! I am Bob.",
    }
    assert collect(html1, {
        "text": ["body", None, ["s|\\s+| |g"]],
    }) == {
        "text": "Hello! I am Bob.",
    }

    assert collect(html1, {
        "img.src": ["body img", "src", ["/\\w+\\.png$/"]],
    }) == {
        "img.src": "img.png",
    }
    assert collect(html1, {
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
    }) == {
        "body": {
            "title": "Hello!",
        },
    }

    assert collect(html1, {
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
