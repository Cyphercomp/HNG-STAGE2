from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ProfilePagination(PageNumberPagination):
    page_size = 10  # Default to 10 if not provided 
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            "status": "success",
            "page": int(self.request.query_params.get(self.page_query_param, 1)), #self.page.number,
            "limit":int(self.request.query_params.get('limit', self.page_size)),#self.page.paginator.per_page, #self.get_page_size(self.request),
            "total": self.page.paginator.count,
            "data": data
        })