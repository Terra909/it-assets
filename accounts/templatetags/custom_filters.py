from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def sum_values(values):
    """Sum all values in a dictionary or iterable."""
    if values is None:
        return 0
    if hasattr(values, 'values'):
        return sum(values.values())
    try:
        return sum(values)
    except (TypeError, ValueError):
        return 0
