prefix = "add_item_option_group_"
midfix = "_choice_"

def create_option_group_name(option_group, choice):
    return "%s%s%s%d" % (prefix, option_group.pk, midfix, choice)

def parse_option_group_name(name):
    data = {}
    if name.startswith(prefix):
        name = name[len(prefix):]
        pk, ignore, choice = name.rpartition(midfix)
        if not pk:
            pk = None
        if not choice:
            choice = None
        try:
            pk = int(pk)
        except ValueError:
            pass
        try:
            choice = int(choice)
        except ValueError:
            pass
        data["pk"] = pk
        data["choice"] = choice
    return data

def append_error(errors, key, error):
    errors.get(key, []).append(error)