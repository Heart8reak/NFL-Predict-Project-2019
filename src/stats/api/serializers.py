from rest_framework import serializers

from stats.models import Stat 


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat 
        fields = [
            'id',
            'team_name',
            'win',
            'lost',
            'pct',
            'pf',
            'pa',
            'net_pts',
        ]

    