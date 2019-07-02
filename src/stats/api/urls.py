from django.urls import path, include

from stats import views 


from .views import StatAPIView, StatDetailAPIView


urlpatterns = [
    path('', StatAPIView.as_view()),
    path('<id>', StatDetailAPIView.as_view()),
]

