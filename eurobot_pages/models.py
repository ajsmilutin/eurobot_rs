from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import RichTextBlock, RawHTMLBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from tournaments.models import Tournament

class RichTextPage(Page):
    content = StreamField([
            ("full_richtext", RichTextBlock()),
            ("raw_html", RawHTMLBlock()),
        ],
        null=True,
        blank=True)
    footer_content = StreamField([
            ("full_richtext", RichTextBlock()),
            ("raw_html", RawHTMLBlock()),
        ],
        null=True,
        blank=True)
    show_in_menus_default = True
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
        StreamFieldPanel('footer_content')
    ]


class BlogEntry(RichTextPage):
    show_in_menus_default = False
    summary = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('summary', classname="full"),
        StreamFieldPanel('content')
    ]
    ordering = ['-first_published_at']


class BlogListing(RichTextPage):
    custom_title =  models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Overwrites the default title',)

    content_panels = Page.content_panels + [
        FieldPanel('custom_title', classname="full"),
        StreamFieldPanel('content')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogEntry.objects.live().public()
        return context



class TournamentInfo(RichTextPage):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    content_panels = [FieldPanel('tournament'),] + RichTextPage.content_panels

class TournamentRounds(RichTextPage):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    content_panels = [FieldPanel('tournament'),] + RichTextPage.content_panels

class TournamentStandings(RichTextPage):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        rounds = self.tournament.rounds.order_by('round_date')
        if rounds.count() > 0:
            player_info = dict()
            players = self.tournament.players.order_by('name')
            for player in players:
                player_info[player.name] = dict({"player": player, "games": [None]*rounds.count(), "score": 0})

            for i in range(rounds.count()):
                round = rounds[i]
                for game in round.games.all():
                    if not game.player_dummy:
                        info = player_info[game.player.name]
                        info['score'] += game.player_score
                        info['games'][i] = {
                            "player": True,
                            "opponent": game.opponent.name,
                            "dummy": game.opponent_dummy,
                            "score": game.player_score
                        }

                    if not game.opponent_dummy:
                        info = player_info[game.opponent.name]
                        info['score'] += game.opponent_score
                        info['games'][i] = {
                            "player": False,
                            "opponent": game.player.name,
                            "dummy": game.player_dummy,
                            "score": game.opponent_score
                        }
            standings = list(player_info.values())
            standings = sorted(standings, key=lambda elem: elem['score'], reverse= True)
            context['standings'] = standings
        return context

    content_panels = [FieldPanel('tournament'),] + RichTextPage.content_panels
