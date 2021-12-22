from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from tournaments.models import Tournament

class RichTextPage(Page):
    body = RichTextField(blank=True)    
    show_in_menus_default = False
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),        
    ]


class TournamentInfo(RichTextPage):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    content_panels = RichTextPage.content_panels + [
        FieldPanel('tournament'),
    ]