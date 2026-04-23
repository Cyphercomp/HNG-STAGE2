import django_filters
from rest_framework.filters import OrderingFilter, SearchFilter
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
from .models import Profile
import re

class ProfileFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(field_name="age", lookup_expr='gte')
    max_age = django_filters.NumberFilter(field_name="age", lookup_expr='lte')
    
    min_gender_prob = django_filters.NumberFilter(field_name="gender_probability", lookup_expr='gte')
    min_country_prob = django_filters.NumberFilter(field_name="country_probability", lookup_expr='gte')
    q = django_filters.CharFilter(method='parse_natural_language', label='Search')

    
    COUNTRY_MAP = {
        # "nigeria": "NG", "kenya": "KE", "ghana": "GH", 
        # "rwanda": "RW", "angola": "AO", "togo": "TG",
        "South Sudan": "SS",
        "Mauritius": "MU",
        "Djibouti": "DJ",
        "Somalia": "SO",
        "Sudan": "SD",
        "Morocco": "MA",
        "Botswana": "BW",
        "Western Sahara": "EH",
        "Niger": "NE",
        "Liberia": "LR",
        "Central African Republic": "CF",
        "Cape Verde": "CV",
        "Gambia": "GM",
        "Mauritania": "MR",
        "Comoros": "KM",
        "Mozambique": "MZ",
        "Lesotho": "LS",
        "Angola": "AO",
        "Tunisia": "TN",
        "United Kingdom": "GB",
        "Mali": "ML",
        "Rwanda": "RW",
        "Benin": "BJ",
        "Seychelles": "SC",
        "Senegal": "SN",
        "France": "FR",
        "United States": "US",
        "Germany": "DE",
        "Eritrea": "ER",
        "Burundi": "BI",
        "Burkina Faso": "BF",
        "Togo": "TG",
        "Ethiopia": "ET",
        "Egypt": "EG",
        "Chad": "TD",
        "Guinea-Bissau": "GW",
        "Guinea": "GN",
        "Republic of the Congo": "CG",
        "Ghana": "GH",
        "Nigeria": "NG",
        "India": "IN",
        "Tanzania": "TZ",
        "Zambia": "ZM",
        "Algeria": "DZ",
        "Equatorial Guinea": "GQ",
        "Eswatini": "SZ",
        "Côte d'Ivoire": "CI",
        "Japan": "JP",
        "China": "CN",
        "Malawi": "MW",
        "Cameroon": "CM",
        "Madagascar": "MG",
        "Canada": "CA",
        "São Tomé and Príncipe": "ST",
        "DR Congo": "CD",
        "Sierra Leone": "SL",
        "Australia": "AU",
        "Namibia": "NA",
        "Zimbabwe": "ZW",
        "South Africa": "ZA",
        "Uganda": "UG",
        "Brazil": "BR",
        "Kenya": "KE",
        "Libya": "LY",
        "Gabon": "GA"

    }
    
    AGE_GROUPS = {
        "teenager": Q(age__gte=13, age__lte=19),
        "young": Q(age__gte=16, age__lte=24),
        "adult": Q(age__gte=25, age__lte=45),
        "senior": Q(age__gte=46, age__lte=100),
    }

    class Meta:
        model = Profile
        fields = [
            'q',
            'gender',
            'country_id',
        ]

    def parse_natural_language(self, queryset, name, value):
        if not value:
            return queryset
        
        query_string = value.lower()
        filters = Q()

        # 1. GENDER LOGIC
        # Check for both "male and female" scenarios first
        if "male" in query_string and "female" in query_string:
            # Matches "male and female" or "females and males"
            filters &= (Q(gender__iexact="male") | Q(gender__iexact="female"))
        elif "female" in query_string:
            filters &= Q(gender__iexact="female")
        elif "male" in query_string:
            filters &= Q(gender__iexact="male")

        # 2. AGE GROUP LOGIC (teenager, young, adult, etc.)
        for group_name, query_obj in self.AGE_GROUPS.items():
            if group_name in query_string:
                filters &= query_obj

        # 3. COMPARATIVE AGE LOGIC (above/over 30)
        above_match = re.search(r'(above|over|older than)\s+(\d+)', query_string)
        if above_match:
            age_val = int(above_match.group(2))
            filters &= Q(age__gt=age_val)

        # 4. COUNTRY LOGIC (from Angola, in Kenya)
        country_match = re.search(r'(from|in|at)\s+([a-zA-Z]+)', query_string)
        if country_match:
            country_name = country_match.group(2).strip()
            iso_code = self.COUNTRY_MAP.get(country_name)
            if iso_code:
                filters &= Q(country_id__iexact=iso_code)

        # 5. EXECUTION & FALLBACK
        # If we successfully parsed attributes, apply them
        if filters:
            return queryset.filter(filters)
        
        # If no keywords matched, perform a standard name search
        return queryset.filter(
            Q(first_name__icontains=value) | 
            Q(last_name__icontains=value)
        )
        
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
    
    