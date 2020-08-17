
def check_input(values_dict, expected):
    errors = []
    if values_dict is None:
        return ["no data provided"]
    for key in values_dict.keys():
        if key not in expected:
            errors.append("unexpected field: {}".format(key))
    for key in expected:
        if key not in values_dict.keys():
            errors.append("missing field: {}".format(key))
    return errors
