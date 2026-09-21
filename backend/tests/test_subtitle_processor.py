"""EN - EN"""

import re

from backend.utils.subtitle_processor import SubtitleProcessor


def _split(text: str):
    """EN，EN（EN）"""
    sp = SubtitleProcessor()
    parts = re.split(sp.word_separators, text)
    return [p for p in parts if p.strip()]


def test_word_separators_is_single_clean_character_class():
    """EN、EN，EN。

    EN bug：EN ASCII EN，
    EN，EN `\\s` EN SyntaxWarning。
    """
    separators = SubtitleProcessor().word_separators

    # EN [....]+
    assert separators.startswith("[")
    assert separators.endswith("]+")

    # EN（EN “”‘’ EN \s）
    for ch in "，。！？；：“”‘’（）【】、":
        assert ch in separators, f"EN: {ch!r}"
    assert r"\s" in separators

    # EN（EN）
    assert re.compile(separators)


def test_splits_cjk_string_on_punctuation_and_whitespace():
    """EN，EN。"""
    sample = "EN，EN！EN“EN”‘EN’；（EN）【EN】、EN EN\tEN。"
    assert _split(sample) == [
        "EN",
        "EN",
        "EN",
        "EN",
        "EN",
        "EN",
        "EN",
        "EN",
        "EN",
        "EN",
    ]


def test_curly_quotes_act_as_separators():
    """EN：EN/EN（EN）。"""
    assert _split("EN“EN”EN") == ["EN", "EN", "EN"]
    assert _split("EN‘EN’EN") == ["EN", "EN", "EN"]
