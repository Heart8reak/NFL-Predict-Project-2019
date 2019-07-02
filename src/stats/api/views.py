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

