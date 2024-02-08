from django import template

from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['current_url']

    menu_items = MenuItem.objects.filter(menu_name=menu_name).values()
    root_items = [item for item in menu_items.filter(parent=None)]
    current_item = menu_items.filter(url__in=current_url).first()

    if current_item is None:
        return {'menu_items': root_items}

    ancestor_items = get_ancestors(current_item, root_items, menu_items)

    for item in root_items:
        if item in ancestor_items:
            item['children'] = get_descendants(menu_items, item, ancestor_items)
    return {'menu_items': root_items}


def get_ancestors(current_item, root_items, menu_items):
    ancestors_items = []

    while current_item:
        ancestors_items.append(current_item)
        current_item = menu_items.get(id=current_item['parent_id']) if current_item['parent_id'] else None

    if ancestors_items:
        return ancestors_items

    for item in root_items:
        if item.id == current_item.id:
            ancestors_items.append(item)
    return ancestors_items


def get_descendants(menu_items, item, ancestor_items):
    descendants_items = [item for item in menu_items.filter(parent=item['id'])]

    for item in descendants_items:
        if item in ancestor_items:
            item['children'] = get_descendants(menu_items, item, ancestor_items)
    return descendants_items


@register.filter(name='startswith')
def startswith(value, arg):
    return value.startswith(arg)
