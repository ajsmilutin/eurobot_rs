import imp
from statistics import mode
from turtle import heading
from django.db import models

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, FieldRowPanel, TabbedInterface, ObjectList, InlinePanel
from django.utils.translation import gettext_lazy as _


class Tournament(ClusterableModel):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    custom_panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('city'),
            FieldRowPanel([
                FieldPanel('start_date', ),
                FieldPanel('end_date'),
            ])
        ])
    ]

    player_panels = [
        MultiFieldPanel([InlinePanel('players', label='Players')])
    ]
    edit_handler = TabbedInterface([
        ObjectList(custom_panels, heading='General Details'),
        ObjectList(player_panels, heading='Player Details')
    ])

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    register_date = models.DateField('registration date', auto_now_add=True)
    static_homologation = models.BooleanField(default=False)
    dynamic_homologation = models.BooleanField(default=False)
    tournament = ParentalKey(Tournament,
                             on_delete=models.CASCADE,
                             related_name='players')
    panels = [
        MultiFieldPanel([
            FieldPanel('tournament'),
            FieldRowPanel([
                FieldPanel('name'),
                FieldPanel('city'),
            ]),
            FieldPanel('school'),
            FieldRowPanel([
                FieldPanel('static_homologation', ),
                FieldPanel('dynamic_homologation'),
            ]),
        ])
    ]

    def __unicode__(self):
        return self.name


class Round(models.Model):
    tournament = models.ForeignKey(Tournament,
                                   on_delete=models.CASCADE,
                                   related_name='rounds')
    name = models.CharField(max_length=200)
    round_date = models.DateTimeField()

    def __unicode__(self):
        return self.tournament.name + " - " + self.name


class Game(models.Model):
    GAME_STATUSES = (
        (_('planned'), _('Planned')),
        (_('finished'), _('Finished'))
    )

    PLAYER_COLOR = (
        ('W', 'White'),
        ('B', 'Black'),
    )

    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    player = models.ForeignKey(Player,
                               related_name="player_a",
                               null=True,
                               on_delete=models.SET_NULL)
    player_color = models.CharField(max_length=1,
                                    choices=PLAYER_COLOR,
                                    default='W')
    player_score = models.PositiveIntegerField(default=0)
    player_dummy = models.BooleanField(default = False)
    opponent_score = models.PositiveIntegerField(default=0)
    opponent_color = models.CharField(max_length=1,
                                      choices=PLAYER_COLOR,
                                      default='B')
    opponent_dummy = models.BooleanField(default = False)
    opponent = models.ForeignKey(
        Player, related_name="player_b", null=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=10,
                              choices=GAME_STATUSES,
                              default='planned')

    def __unicode__(self):
        return str(self.player) + " " + str(self.player_score) + ":" + str(self.opponent_score) + " " + str(self.opponent)
