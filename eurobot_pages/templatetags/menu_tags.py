from operator import truediv
from django import template
from ..models import Page
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=True)
def live_children(context):
    page = context['page']
    root_page = page.get_site().root_page
    return Page.objects.filter(live=True).count()

@register.simple_tag(takes_context=True)
def top_menu(context, menu_template, current_page, root = None):
    def is_current_or_ascendant(page, current_page):
        if current_page:
            return True if page.id == current_page.id else is_current_or_ascendant(
                page, current_page.get_parent())
        else:
            return False

    if root is None:
        root = current_page.get_site().root_page
        root.is_current_or_ascendant = root.id == current_page.id
        menu_pages = [root]
    else:
        menu_pages = []

    for menu_page in root.get_children().live().filter(
            show_in_menus=True):
        menu_page.children_to_show = menu_page.get_children().live().filter(
            show_in_menus=True)
        menu_page.is_current_or_ascendant = is_current_or_ascendant(menu_page, current_page)
        menu_pages.append(menu_page)


    return render_to_string(menu_template, {
        "menu_pages": menu_pages,
         "current_page": current_page})
