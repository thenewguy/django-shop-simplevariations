from shop.views import ShopTemplateResponseMixin

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

def store_error(errors, key, name, description):
    if not key in errors:
        errors[key] = {}
    errors[key][name] = description

def render_errors_response(request, template_name, errors):
    renderer = ShopTemplateResponseMixin()
    renderer.request = request
    renderer.template_name = template_name
    context = errors
    response = renderer.render_to_response(context)
    return response