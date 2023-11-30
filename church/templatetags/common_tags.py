from django import template

from church.models import MenuTop, Category, Post, Tag

register = template.Library()


@register.inclusion_tag('church/tags/_menu.html', takes_context=True)
def show_top_menu(context):
    menu_items = MenuTop.objects.all()
    return {
        "menu_items": menu_items,
        "current_url": context.request.get_full_path()
    }


@register.inclusion_tag('church/tags/_sidebar.html', takes_context=True)
def show_sidebar(context):
    categories = Category.objects.all()[:5]
    news = Post.objects.all()[:4]
    tags = Tag.objects.all()
    return {
        "categories": categories,
        "news": news,
        "tags": tags,
    }