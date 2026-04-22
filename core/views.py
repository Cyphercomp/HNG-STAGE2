from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework import status
from .models import Profile
from .serializer import ProfileSerializer
from .filters import ProfileFilter
from .pagination import ProfilePagination
# Create your views here.

class ProfileViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProfileFilter
    #filterset_fields = ['gender', 'age_group', 'country_id']
    ordering_fields = ['age', 'gender_probability', 'country_probability']
    pagination_class = ProfilePagination

    def list(self, request, *args, **kwargs):
        # 1. Apply the filters first
        queryset = self.filter_queryset(self.get_queryset())

        # 2. Apply pagination to the filtered queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # 3. Fallback for no pagination
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)