def merge_request(data, fields=None, fill_value=None):
    if fields is None:
        fields = []
    fields_data = dict.fromkeys(fields, fill_value)
    for name, value in fields_data.items():
        if name in data:
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