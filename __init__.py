import sys
import subprocess
import importlib.util
import json
import os

from anki.hooks import addHook
from aqt import mw
from aqt.utils import showWarning


def ensure_package(package, import_name=None):
    if import_name is None:
        import_name = package

    if importlib.util.find_spec(import_name) is None:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            package,
        ])


# Dependencies
ensure_package("fugashi")
ensure_package("unidic-lite", "unidic_lite")


# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)

    except FileNotFoundError:
        showWarning(
            "Furigana addon: config.json is missing."
        )
        return None

    except json.JSONDecodeError:
        showWarning(
            "Furigana addon: config.json contains invalid JSON."
        )
        return None

    required = ["source_field", "target_field"]

    for key in required:
        if key not in config:
            showWarning(
                f"Furigana addon: missing '{key}' in config.json."
            )
            return None

    return config


config = load_config()

if config:
    SOURCE_FIELD = config["source_field"]
    TARGET_FIELD = config["target_field"]

    from .furigana import add_furigana


    def validate_fields(note):
        fields = mw.col.models.fieldNames(note.model())

        if SOURCE_FIELD not in fields:
            showWarning(
                f"Furigana addon: source field '{SOURCE_FIELD}' "
                f"does not exist.\n\nAvailable fields:\n"
                + "\n".join(fields)
            )
            return False

        if TARGET_FIELD not in fields:
            showWarning(
                f"Furigana addon: target field '{TARGET_FIELD}' "
                f"does not exist.\n\nAvailable fields:\n"
                + "\n".join(fields)
            )
            return False

        return True


    def on_field_changed(changed, note, field_idx):
        if not changed:
            return True

        fields = mw.col.models.fieldNames(note.model())

        current_field = fields[field_idx]

        if current_field != SOURCE_FIELD:
            return True

        if not validate_fields(note):
            return True

        text = note[SOURCE_FIELD]

        if text:
            note[TARGET_FIELD] = add_furigana(text)

        return True


    addHook("editFocusLost", on_field_changed)