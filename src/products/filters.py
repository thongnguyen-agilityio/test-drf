import django_filters
import rest_framework_filters as filters
from django.db.models import Q

from drf_core.filtering import BaseFiltering
from products.models import (
    Category,
    Season,
    Usage,
    BaseColour,
    ArticleType,
    Gender,
    Product,
)


# =============================================================================
# Category
# =============================================================================
class CategoryFiltering(BaseFiltering):

    class Meta:
        model = Category
        exclude = []
        fields = {'name': ['exact', 'in', 'startswith']}


# =============================================================================
# Season
# =============================================================================
class SeasonFiltering(BaseFiltering):

    class Meta:
        model = Season
        exclude = []


# =============================================================================
# Usage
# =============================================================================
class UsageFiltering(BaseFiltering):

    class Meta:
        model = Usage
        exclude = []


# =============================================================================
# BaseColour
# =============================================================================
class BaseColourFiltering(BaseFiltering):

    class Meta:
        model = BaseColour
        exclude = []


# =============================================================================
# ArticleType
# =============================================================================
class ArticleTypeFiltering(BaseFiltering):

    class Meta:
        model = ArticleType
        exclude = []


# =============================================================================
# Gender
# =============================================================================
class GenderFiltering(BaseFiltering):

    class Meta:
        model = Gender
        exclude = []


class ProductGenerallyFiltering(BaseFiltering):
    """
    Generally filtering for products
    """
    # Full text search by a keyword
    keyword = django_filters.CharFilter(method='full_text_search')

    category_ids = django_filters.CharFilter(method='filter_by_ids')
    gender_ids = django_filters.CharFilter(method='filter_by_ids')
    colour_ids = django_filters.CharFilter(method='filter_by_ids')
    season_ids = django_filters.CharFilter(method='filter_by_ids')
    articletype_ids = django_filters.CharFilter(method='filter_by_ids')
    usage_ids = django_filters.CharFilter(method='filter_by_ids')

    class Meta:
        model = Product
        fields = {
            'price': ['lt', 'lte', 'gt', 'gte']
        }

    @classmethod
    def full_text_search(cls, queryset, _, text):
        """
        Search in product name and category name

        @param queryset: The queryset
        @param _:
        @param text: Text search data
        @return: Queryset
        """
        return queryset.filter(
            Q(name__icontains=text) |
            Q(category__name__icontains=text)
        )

    @classmethod
    def filter_by_ids(cls, queryset, query_name, query_values):
        """
        Filter by list of category ids

        @param queryset: The queryset
        @param query_name: Query name
        @param query_values: The list of category ids separated by comma
        @return: Queryset
        """
        query_values = query_values.split(',')
        valid_values = list()

        mapping_list = {
            'category_ids': 'category',
            'gender_ids': 'gender',
            'colour_ids': 'base_colour',
            'season_ids': 'season',
            'usage_ids': 'usage',
            'articletype_ids': 'article_type'
        }

        if query_name not in mapping_list.keys():
            return queryset

        # Get integer value only
        for value in query_values:
            try:
                valid_values.append(int(value))
            except TypeError:
                pass

        return queryset.filter(
            Q(**{f'{mapping_list[query_name]}__in': valid_values})
        )


# =============================================================================
# Product
# =============================================================================
class ProductAdvanceFiltering(ProductGenerallyFiltering):
    """
    Product advance filtering
    """
    category = filters.RelatedFilter(
        CategoryFiltering,
        field_name='category',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = {
            'price': ['lt', 'lte', 'gt', 'gte'],
            'name': [
                'iexact', 'exact',
                'icontains', 'contains',
                'istartswith', 'startswith',
                'iendswith', 'endswith'
            ],
            'quantity': ['lt', 'lte', 'gt', 'gte'],
            'sold_quantity': ['lt', 'lte', 'gt', 'gte']
        }
