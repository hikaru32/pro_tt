from django import template


def ntl(value):
    if not isinstance(value, int):
        try:
            value = int(value)
        except Exception as e:
            pass
    return range(value)


register = template.Library()
register.filter('ntl', ntl)
