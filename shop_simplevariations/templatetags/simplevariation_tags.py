from django import template
from ..util import create_option_group_name

register = template.Library()


@register.filter
def get_option_groups(value):
    """Returns all option groups for the given product."""
    return value.option_groups.all()


@register.filter
def get_options(value):
    """Returns all options for the given option group."""
    return value.get_options()

@register.filter
def get_defaults(value):
    return value.defaults.all()

@register.filter
def get_xrange(value, start=0):
    """
    Filter - returns xrange from given value and optional start
    Usage (in template):
    
    <ul>{% for i in 3|get_range:1 %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>
    
    Results with the HTML:
    <ul>
      <li>1. Do something</li>
      <li>2. Do something</li>
      <li>3. Do something</li>
    </ul>
    
    Instead of 3 one may use the variable set in the views
    """
    return xrange(start, value)

@register.filter
def get_choice_range(value):
    return get_xrange(value+1, 1)

@register.filter
def get_option_group_name(value, choice):
    """
    Returns the name to use for an option group's form field and label.
    
    value should be the option group.  choice should be an integer 
    representing which choice number is being rendered.
    """
    return create_option_group_name(value, choice)

@register.assignment_tag
def get_default_option(**kwargs):
    """
        option: the option model instance in question
        group: the option group that references the option
        choice: the option group choice count
        
        if defaults are not set, return false.
        
        if defaults are set, and there are more choices than
        defaults, choices that do not have a default set
        will use the last default set.
        
        e.g. defaults [a, b]
        choice 1 default is a
        choice 2 default is b
        choice 3 default is b
    """
    option = kwargs["option"]
    group = kwargs["group"]
    choice = kwargs["choice"]
    options = group.defaults.all()
    
    if len(options) < choice:
        choice = len(options)
    
    return options[choice-1] if options else None

@register.filter
def relative_price(option, base):
    price = option.price
    if base:
        price -= base.price
    return price

@register.filter
def format_price(value):
    return u"-$%s" % abs(value) if value < 0 else u"$%s" % value