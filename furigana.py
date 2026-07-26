import re
import fugashi

_tagger = None


def get_tagger():
    global _tagger

    if _tagger is None:
        _tagger = fugashi.Tagger()

    return _tagger



def kanji_only(s):
    return any("\u4e00" <= c <= "\u9fff" for c in s)


def katakana_to_hiragana(s):
    return "".join(
        chr(ord(c) - 0x60) if "\u30a1" <= c <= "\u30f6" else c
        for c in s
    )


def add_furigana(text):
    tagger = get_tagger()

    wresult = []

    for word in tagger(text):
        surface = word.surface
        reading = word.feature.kana

        # No reading available (punctuation, symbols, etc.)
        if not reading or reading == "*":
            result.append(surface)
            continue

        reading = katakana_to_hiragana(reading)

        # Only add ruby when the token contains kanji
        if kanji_only(surface):
            result.append(f"<ruby>{surface}<rt>{reading}</rt></ruby>")
        else:
            result.append(surface)


    ruby_html = "".join(result)

    return ruby_html