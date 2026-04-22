from django_filters.rest_framework import FilterSet
from .models import Profile

class ProfileFilter(FilterSet):

    class Meta:
        model = Profile
        fields = {
            'gender': ['exact'],
            'age_group': ['exact'],
            'country_id': ['exact'],
            'age': ['gte', 'lte'],
            'gender_probability': ['gte'],
            'country_probability': ['gte'],
        }