from django import template

from church.models import MenuTop

register = template.Library()


@register.inclusion_tag('church/tags/_menu.html', takes_context=True)
def show_top_menu(context):
    menu_items = MenuTop.objects.all()
    return {
        "menu_items": menu_items,
        "current_url": context.request.get_full_path()
    }