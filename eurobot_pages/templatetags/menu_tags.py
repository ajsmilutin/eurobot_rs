from django import template
from ..models import Page
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=True)
def live_children(context):
    page = context['page']
    root_page = page.get_site().root_page
    print(root_page)

    return Page.objects.filter(live=True).count()

@register.simple_tag(takes_context=True)
def top_menu(context, menu_template):
    page = context['page']
    root_page = page.get_site().root_page
    menu_pages = [root_page]
    for menu_page in root_page.get_children().live():
        menu_pages.append(menu_page)

    for menu_page in menu_pages:
        menu_page.is_current = (page.id == menu_page.id)        

    string = render_to_string(menu_template, {
        "menu_pages": menu_pages,
        "current_page": page
    })
    return render_to_string(menu_template, {
        "menu_pages": menu_pages})
