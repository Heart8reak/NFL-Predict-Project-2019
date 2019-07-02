# NFL Predict Project 2019

1. Using the terminal, create a directory, virtual environment, activate environment, create a src directory
````
mkdir nflpredict
cd nflpredict
virtualenv -p python3 .
source bin/activate
mkdir src 
cd src
````

2. install the project requirements and add it to requirements.txt
````
pip install django
pip install djangorestframework
pip install markdown
pip install django-filter
pip freeze > requirements.txt
````

3. make sure you are in src directory, start django project
````
django-admin startproject nflpredict .
````

3.1 create a django app
````
python manage.py startapp stats
````

4. register the new to settings.py file in the ndflpredict directory under INSTALLED_APPS

5. lets begin with the backend with running a migrations and creating a superuser, in the terminal. (as far as the username and password, I kept it simple) then runserver
````
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
````

6. creating our models
````python
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
````

7. registering the models in our admin section
````python 
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
````

8. in our stats directory create another directory called api and in the directory create these files, __init__.py serializers.py urls.py views.py
````
mkdir api
cd api
touch __init__.py
touch serializers.py
touch urls.py
touch views.py
````

9. starting with our serializers.py
````python 
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
````

10. urls.py
````python 
from django.urls import path, include

from stats import views 


from .views import StatAPIView, StatDetailAPIView


urlpatterns = [
    path('', StatAPIView.as_view()),
    path('<id>', StatDetailAPIView.as_view()),
]
````

11. views.py
````python 
from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from stats.models import Stat 
from .serializers import StatSerializer



class StatAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.ListAPIView):

    permission_classes              = []
    authentication_classes          = []
    serializer_class                = StatSerializer

    def get_queryset(self):
        request = self.request
        qs = Stat.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def get_object(self):
        request         = self.request
        passed_id       = request.GET.get('id', None)
        queryset        = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        passed_id = request.GET.get('id', None)
        if passed_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StatDetailAPIView(generics.RetrieveAPIView):
    permission_classes                  = []
    authentication_classes              = []
    queryset                            = Stat.objects.all()
    serializer_class                    = StatSerializer

    def get_object(self, *args, **kwargs):
        kwargs = self.kwargs
        kw_id = kwargs.get('id')
        return Stat.objects.get(id=kw_id)

````

12. To see our API go to the link http://127.0.0.1:8000/api/stats/

