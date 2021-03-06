# todo: chargedness of battery

import time
from datetime import datetime
import numpy as np

try:
    from whereami.predict import Predicter
    p = Predicter()
except ImportError:
    p = None

from brightml.xdisplay import Display
d = Display()


DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


def get_ambient_light():
    try:
        # please, if your ambient light sensor doesn't work, post the path in the issues on github
        with open("/sys/devices/platform/applesmc.768/light") as f:
            return int(f.read()[1:-1].split(",")[0])
    except:
        return np.nan


def get_time_features():
    now = datetime.strptime(time.strftime(DATE_FORMAT, time.localtime()), DATE_FORMAT)
    data = {
        "datetime_hour": now.hour,
        "datetime_timezone": str(now.tzinfo),
        "datetime_date": str(now.date()),
        "datetime_full": str(now)
    }
    return data


def get_features():
    data = {
        "ambient_light": get_ambient_light(),
        "whereami": p.predicted_value if p else None
    }
    data.update(get_time_features())
    data.update(d.last_value)
    return data
