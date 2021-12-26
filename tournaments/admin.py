from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup

from .models import Round, Tournament, EliminationRound


class TouramentAdmin(ModelAdmin):
    model = Tournament
    menu_label = "Tournaments"
    menu_icon = "site"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "name",
        "city",
    )

class RoundAdmin(ModelAdmin):
    model = Round
    list_display = ('tournament', 'name', 'round_date')


class EliminationRound(ModelAdmin):
    model = EliminationRound
    list_display = ('tournament', 'name', 'round_date')

class TournamentGroup(ModelAdminGroup):
    menu_label = 'Tournaments'
    menu_icon = 'group'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (TouramentAdmin, RoundAdmin, EliminationRound)

modeladmin_register(TournamentGroup)
