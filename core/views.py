from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from resst_framework.decorators import action
from rest_framework import status
from .models import Profile
from .serializer import ProfileSerializer
from .filters import ProfileFilter, CustomOrderingFilter
from .pagination import ProfilePagination
# Create your views here.

class ProfileViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, CustomOrderingFilter, SearchFilter]
    filterset_class = ProfileFilter
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
    
    @action(detail=False, methods=['get'], url_path='search')
    def search_profiles(self, request):
        # 1. Get the base queryset
        queryset = self.get_queryset()
        
        # 2. Manually trigger the ProfileFilter
        filterset = self.filterset_class(request.GET, queryset=queryset, request=request)
        
        if filterset.is_valid():
            queryset = filterset.qs
        
        # 3. Use your custom pagination to ensure the "Envelope" is correct
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Fallback for non-paginated (though CustomPagination should handle this)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)