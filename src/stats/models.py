from django.db import models

# Create your models here.

class Stat(models.Model):
    team_name           = models.CharField(max_length=100)
    win                 = models.IntegerField()
    lost                = models.IntegerField()
    pct                 = models.DecimalField(max_digits=4, decimal_places=3)
    pf                  = models.IntegerField()
    pa                  = models.IntegerField()
    net_pts             = models.IntegerField()


    def __str__(self):
        return self.team_name
