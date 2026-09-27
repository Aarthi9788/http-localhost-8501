import re


TRANSLATIONS = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
)


def sanitize_text(
    text: str
) -> str:

    text = (
        text or ""
    ).translate(
        TRANSLATIONS
    )

    text = re.sub(
        r"[^\x09\x0A\x0D\x20-\x7E]",
        "",
        text
    )

    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text
    )

    return text.strip()