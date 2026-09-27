from app.utils import sanitize_text


def test_sanitize_text():

    result = sanitize_text(
        'Hello “LegalEase” — Draft…'
    )

    assert result == (
        'Hello "LegalEase" - Draft...'
    )