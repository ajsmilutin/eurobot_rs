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

    first_place = models.OneToOneField('Player',
                                       related_name='first_place',
                                       blank=True,
                                       null=True,
                                       on_delete=models.SET_NULL)
    second_place = models.OneToOneField('Player',
                                        related_name='second_place',
                                        blank=True,
                                        null=True,
                                        on_delete=models.SET_NULL)
    third_place = models.OneToOneField('Player',
                                       related_name='third_place',
                                       blank=True,
                                       null=True,
                                       on_delete=models.SET_NULL)

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
    round_panels = [
        InlinePanel('elimination_rounds', label='Elimination Rounds'),
        InlinePanel('rounds', label='Rounds')
    ]
    final_results = [
        FieldPanel('first_place', ),
        FieldPanel('second_place'),
        FieldPanel('third_place')
    ]

    edit_handler = TabbedInterface([
        ObjectList(custom_panels, heading='General Details'),
        ObjectList(player_panels, heading='Player Details'),
        ObjectList(round_panels, heading='Rounds'),
        ObjectList(final_results, heading='Final results')
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
        FieldRowPanel([
            FieldPanel('school', classname='col6'),
            FieldPanel('static_homologation', classname='col3'),
            FieldPanel('dynamic_homologation', classname='col3'),
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

    class Meta:
        ordering = ["-round_date"]

    def __str__(self):
        return self.tournament.name + " - " + self.name


class Game(models.Model):
    GAME_STATUSES = ((_('planned'), _('Planned')), (_('finished'),
                                                    _('Finished')))

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
        return str(self.player) + " " + str(self.player_score) + ":" + str(
            self.opponent_score) + " " + str(self.opponent)


class EliminationRound(ClusterableModel):
    tournament = ParentalKey(Tournament,
                             on_delete=models.CASCADE,
                             related_name='elimination_rounds')
    round_date = models.DateTimeField()
    name = models.CharField(max_length=200)

    panels = [
        FieldRowPanel([
            FieldPanel('name', classname="col8"),
            FieldPanel('round_date', classname="col4"),
        ]),
        InlinePanel('games', label='Game')
    ]

    class Meta:
        ordering = ["-round_date"]

    def __str__(self):
        return self.tournament.name + " - " + self.name


class EliminationGame(models.Model):
    elimination_round = ParentalKey(EliminationRound,
                                    on_delete=models.CASCADE,
                                    related_name='games')
    player = models.ForeignKey(Player,
                               related_name="player_1",
                               on_delete=models.CASCADE)
    opponent = models.ForeignKey(Player,
                                 related_name="player_2",
                                 on_delete=models.CASCADE)
    player_score_0 = models.PositiveIntegerField(default=0)
    opponent_score_0 = models.PositiveIntegerField(default=0)
    player_score_1 = models.PositiveIntegerField(default=0)
    opponent_score_1 = models.PositiveIntegerField(default=0)
    player_score_2 = models.PositiveIntegerField(default=0)
    opponent_score_2 = models.PositiveIntegerField(default=0)
    panels = [
        FieldRowPanel([
            FieldPanel('player', classname="col6"),
            FieldPanel('opponent', classname="col6")
        ]),
        FieldRowPanel([
            FieldPanel('player_score_0', classname="col6"),
            FieldPanel('opponent_score_0', classname="col6")
        ]),
        FieldRowPanel([
            FieldPanel('player_score_1', classname="col6"),
            FieldPanel('opponent_score_1', classname="col6")
        ]),
        FieldRowPanel([
            FieldPanel('player_score_2', classname="col6"),
            FieldPanel('opponent_score_2', classname="col6")
        ])
    ]

    def player_wins(self):
        return (self.player_score_0 > self.opponent_score_0
                and self.player_score_1 > self.opponent_score_1) or (
                    self.player_score_0 > self.opponent_score_0
                    and self.player_score_2 > self.opponent_score_2) or (
                        self.player_score_2 > self.opponent_score_2
                        and self.player_score_1 > self.opponent_score_1)

    def opponent_wins(self):
        return (self.player_score_0 < self.opponent_score_0
                and self.player_score_1 < self.opponent_score_1) or (
                    self.player_score_0 < self.opponent_score_0
                    and self.player_score_2 < self.opponent_score_2) or (
                        self.player_score_2 < self.opponent_score_2
                        and self.player_score_1 < self.opponent_score_1)
