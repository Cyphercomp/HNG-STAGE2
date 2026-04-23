import django_filters
from rest_framework.filters import OrderingFilter
from .models import Profile

class ProfileFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(field_name="age", lookup_expr='gte')
    max_age = django_filters.NumberFilter(field_name="age", lookup_expr='lte')
    
    min_gender_prob = django_filters.NumberFilter(field_name="gender_probability", lookup_expr='gte')
    min_country_prob = django_filters.NumberFilter(field_name="country_probability", lookup_expr='gte')
    class Meta:
        model = Profile
        fields = {
            'gender': ['exact'],
            'age_group': ['exact'],
            'country_id': ['exact'],
        }



class CustomOrderingFilter(OrderingFilter):
    # Map your custom names to DRF's internal logic
    ordering_param = 'sort_by'  # Matches your ?sort_by=age
    
    def get_ordering(self, request, queryset, view):
        """
        Check for 'sort_by' and 'order' and return DRF-style ordering list.
        Example: sort_by=age & order=desc -> ['-age']
        """
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            order = request.query_params.get('order', 'asc')
            
            # If order is 'desc', add the minus sign to each field
            if order.lower() == 'desc':
                return [f"-{f}" for f in fields]
            return fields

        return super().get_ordering(request, queryset, view)