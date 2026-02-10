import json
import os

_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")

_DEFAULTS = {
    "totkanaly": "",
    "calib_a": "",
    "calib_b": "",
    "calib_c": "",
    "calib_t": "",
    "clog": "",
    "output_folder": "",
    "output_name": "",
}

def _load():
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {**_DEFAULTS, **data}
    except (FileNotFoundError, json.JSONDecodeError):
        return _DEFAULTS.copy()

def _save(data):
    with open(_SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get(key):
    return _load().get(key, _DEFAULTS.get(key, ""))

def set(key, value):
    data = _load()
    data[key] = value or ""
    _save(data)

def get_initial_dir(key):
    path = get(key)
    if path and os.path.isfile(path):
        return os.path.dirname(path)
    if path and os.path.isdir(path):
        return path
    return None
