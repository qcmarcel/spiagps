import re
import time
from datetime import datetime

from pytz import timezone

DEFAULT_DATETIME = "%Y-%m-%d %H:%M:%S"


def merge_request(data, fields=None, fill_value=None, defaults=None, convert=None):
    if fields is None:
        fields = []
    fields_data = dict.fromkeys(fields, fill_value)
    if defaults is not None:
        fields_data = {k: v if k not in defaults else defaults[k] for k, v in fields_data.items()}
    for name, value in fields_data.items():
        if name in data:
            if convert is not None and name in convert:
                data[name] = convert[name](data[name])
            continue
        filter_field_name = list(filter(lambda k: name.startswith(k), data.keys()))
        if len(filter_field_name) > 0:
            key_of_data = filter_field_name.pop(0)
            value_of_fields = data[key_of_data]
            data[name] = value_of_fields
            data = {k: v for k, v in data.items() if k != key_of_data}
        else:
            data[name] = value
    return data


def timestamp_convert(value, time_zone=None, date_format=DEFAULT_DATETIME):
    print('time_zone:', time.strftime('%Z'))
    date_string = value
    if re.match(r'\d', str(value)) is not None:
        date_obj = datetime.fromtimestamp(float(value))
        if time_zone is not None:
            date_obj = date_obj.astimezone(timezone(time_zone))
        date_string = date_obj.strftime(date_format)
    return date_string
