from cProfile import label
import imp
from pydoc import classname
from statistics import mode
from tkinter import Label
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

    player_color = models.CharField(max_length=7, default="#ADD0E4")
    opponent_color = models.CharField(max_length=7, default="#E2DFB6")
    custom_panels = [
        FieldPanel('name'),
        FieldPanel('city'),
        FieldRowPanel([
            FieldPanel('start_date', ),
            FieldPanel('end_date'),
            FieldPanel('player_color'),
            FieldPanel('opponent_color'),
        ])
    ]

    player_panels = [InlinePanel('players', label='Players')]

    edit_handler = TabbedInterface([
        ObjectList(custom_panels, heading='General Details'),
        ObjectList(player_panels, heading='Player Details'),
    ])

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
        FieldRowPanel([
            FieldPanel('name'),
            FieldPanel('city'),
        ]),
        FieldRowPanel([FieldPanel('school',classname='col6'),
            FieldPanel('static_homologation',classname='col3'),
            FieldPanel('dynamic_homologation',classname='col3'),
        ])
    ]

    def __str__(self):
        return self.name


class Round(ClusterableModel):
    tournament = ParentalKey(Tournament,
                             on_delete=models.CASCADE,
                             related_name='rounds')
    name = models.CharField(max_length=200)
    round_date = models.DateTimeField()
    panels = [
        FieldRowPanel([
            FieldPanel('tournament', classname='col6'),
            FieldPanel('name', classname='col3'),
            FieldPanel('round_date', classname='col3')
        ]),
        InlinePanel('games', label='Game')
    ]

    def __str__(self):
        return self.tournament.name + " - " + self.name


class Game(models.Model):
    GAME_STATUSES = (
        (_('planned'), _('Planned')),
        (_('finished'), _('Finished'))
    )

    round = ParentalKey(Round,
                              related_name='games',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    player = models.ForeignKey(Player,
                               related_name="player_a",
                               null=True,
                               on_delete=models.SET_NULL)
    player_score = models.PositiveIntegerField(default=0, verbose_name='pts')
    player_dummy = models.BooleanField(default=False, verbose_name="dummy")
    opponent_score = models.PositiveIntegerField(default=0, verbose_name='pts')
    opponent_dummy = models.BooleanField(default=False, verbose_name="dummy")
    opponent = models.ForeignKey(Player,
                                 related_name="player_b",
                                 null=True,
                                 on_delete=models.SET_NULL)

    status = models.CharField(max_length=10,
                              choices=GAME_STATUSES,
                              default='planned')

    panels = [
        FieldRowPanel([
            FieldPanel('player', classname="col6"),
            FieldPanel('player_score', classname="col3"),
            FieldPanel('player_dummy', classname="col3")
        ]),
        FieldRowPanel([
            FieldPanel('opponent', classname="col6"),
            FieldPanel('opponent_score', classname="col3"),
            FieldPanel('opponent_dummy', classname="col3"),
        ]),
        FieldPanel("status")
    ]

    def __str__(self):
        return str(self.player) + " " + str(self.player_score) + ":" + str(self.opponent_score) + " " + str(self.opponent)
