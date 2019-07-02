from django.contrib import admin

# Register your models here.

from .models import Stat

class StatAdmin(admin.ModelAdmin):
    list_display = [
        'team_name',
        'win',
        'lost',
        'pct',
        'pf',
        'pa',
        'net_pts',
    ]


admin.site.register(Stat, StatAdmin)