import os
import simplejson
import pandas as pd

_NONE_PATH = None


def get_brightml_path(path=None):
    global _NONE_PATH
    if path is None:
        if _NONE_PATH is None:
            _USERNAME = os.getenv("SUDO_USER") or os.getenv("USER") or "/."
            path = os.path.expanduser('~' + _USERNAME)
            path = os.path.join(path, ".brightml")
            _NONE_PATH = path
        else:
            path = _NONE_PATH
    return os.path.expanduser(path)


def ensure_path_exists(path):
    if not os.path.exists(path):  # pragma: no cover
        os.makedirs(path)


def get_data_path(path=None):
    data_path = "data.jsonl"
    path = path or get_brightml_path()
    ensure_path_exists(path)
    return os.path.join(path, data_path)


def prep_data(data):
    data = data.sort_values(by='datetime_full')
    if "new_brightness" in data.columns:
        col_sort = [x for x in data.columns if x != "new_brightness"] + ["new_brightness"]
        data = data.reindex_axis(col_sort, axis=1)
    return data


def get_training_data(path=None):
    path = get_data_path(path)
    data = pd.read_json(path, lines=True)
    return prep_data(data)


def save_sample(data, path=None):
    path = get_data_path(path)
    with open(path, "a") as f:
        f.write(simplejson.dumps(data, ignore_nan=True) + "\n")


def get_brightness_paths():
    base_dir = "/sys/class/backlight"
    return [os.path.join(base_dir, x) + "/" for x in os.listdir(base_dir)]
