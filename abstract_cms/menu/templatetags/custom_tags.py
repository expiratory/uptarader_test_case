from django import template

from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('menu.html')
def draw_menu(menu_name, children=None):
    if children is None and menu_name is not None:
        menu_items = MenuItem.objects.filter(parent__isnull=True, menu_name=menu_name)
        return {'menu_items': menu_items}
    else:
        return {'menu_items': children}


@register.filter
def has_children(item):
    return item.children.exists()
