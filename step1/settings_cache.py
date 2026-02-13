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
    "calibration_data": None,
    "calibration_curves_data": None,
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

def get_calibration_data():
    data = _load().get("calibration_data")
    if data and isinstance(data, dict) and "files" in data:
        return data
    return {"output_folder": get("output_folder") or "", "files": []}

def set_calibration_data(data):
    d = _load()
    d["calibration_data"] = data
    _save(d)

def get_calibration_curves_data():
    data = _load().get("calibration_curves_data")
    if data and isinstance(data, dict):
        return data
    return {"hist_pixel": "", "curve_pixels": [], "overlay_files": [{"path": "", "americium": False, "energy": ""}]}

def set_calibration_curves_data(data):
    d = _load()
    d["calibration_curves_data"] = data
    _save(d)
