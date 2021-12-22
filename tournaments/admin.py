from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from django.contrib import admin as django_admin
from .models import Tournament, Player


class PlayerInline(django_admin.TabularInline):
    model = Player


class TouramentAdmin(ModelAdmin):
    model = Tournament
    menu_label = "Tournaments"
    menu_icon = "Placeholder"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "name",
        "city",
    )


modeladmin_register(TouramentAdmin)


class PlayerAdmin(ModelAdmin):
    model = Player
    list_display = ('name', 'school', 'city', 'static_homologation',
                    'dynamic_homologation')
    search_fields = ['name'],
    ordering = ['name']


modeladmin_register(PlayerAdmin)
