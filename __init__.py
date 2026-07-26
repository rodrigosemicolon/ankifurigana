from anki.hooks import addHook
from aqt import mw

from .furigana import add_furigana


SOURCE_FIELD = "Expression"
TARGET_FIELD = "Reading"


def on_field_changed(changed, note, field_idx):
    if not changed:
        return changed

    fields = mw.col.models.fieldNames(note.model())

    current_field = fields[field_idx]

    # only run when Expression changes
    if current_field != SOURCE_FIELD:
        return changed

    text = note[SOURCE_FIELD]

    if not text:
        return changed

    note[TARGET_FIELD] = add_furigana(text)

    return True


addHook("editFocusLost", on_field_changed)