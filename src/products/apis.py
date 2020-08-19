from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework_extensions.mixins import NestedViewSetMixin

from accounts.permission import IsAdmin
from core.apis import BaseViewSet
from products.models import (
    Category,
    Season,
    Usage,
    BaseColour,
    ArticleType,
    Gender,
    Product,
)
from products.serializers import (
    CategorySerializer,
    SeasonSerializer,
    UsageSerializer,
    BaseColourSerializer,
    ArticleTypeSerializer,
    GenderSerializer,
    ProductSerializer,
    ProductGenerallySerializer,
)
from products.filters import (
    CategoryFiltering,
    SeasonFiltering,
    UsageFiltering,
    BaseColourFiltering,
    ArticleTypeFiltering,
    GenderFiltering,
    ProductAdvanceFiltering,
    ProductGenerallyFiltering,
)


# =============================================================================
# Category
# =============================================================================
class CategoryViewSet(NestedViewSetMixin, BaseViewSet):
    # Category ViewSet

    queryset = Category.objects.non_archived_only()
    serializer_class = CategorySerializer
    filter_class = CategoryFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'categories'


# =============================================================================
# Season
# =============================================================================
class SeasonViewSet(BaseViewSet):
    # Season ViewSet

    queryset = Season.objects.non_archived_only()
    serializer_class = SeasonSerializer
    filter_class = SeasonFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'seasons'


# =============================================================================
# Usage
# =============================================================================
class UsageViewSet(BaseViewSet):
    # Usage ViewSet

    queryset = Usage.objects.non_archived_only()
    serializer_class = UsageSerializer
    filter_class = UsageFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'usages'


# =============================================================================
# BaseColour
# =============================================================================
class BaseColourViewSet(BaseViewSet):
    # BaseColour ViewSet

    queryset = BaseColour.objects.non_archived_only()
    serializer_class = BaseColourSerializer
    filter_class = BaseColourFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'basecolours'


# =============================================================================
# ArticleType
# =============================================================================
class ArticleTypeViewSet(BaseViewSet):
    # ArticleType ViewSet

    queryset = ArticleType.objects.non_archived_only()
    serializer_class = ArticleTypeSerializer
    filter_class = ArticleTypeFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'articletypes'


# =============================================================================
# Gender
# =============================================================================
class GenderViewSet(BaseViewSet):
    # Gender ViewSet

    queryset = Gender.objects.non_archived_only()
    serializer_class = GenderSerializer
    filter_class = GenderFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = []

    resource_name = 'genders'


# =============================================================================
# Product
# =============================================================================
class ProductViewSet(NestedViewSetMixin, BaseViewSet):
    # Product ViewSet

    queryset = Product.objects.non_archived_only()\
        .select_related('category', 'gender', 'article_type', 'base_colour',
                        'season', 'usage', 'created_by', 'last_modified_by')
    serializer_class = ProductSerializer
    filter_class = ProductGenerallyFiltering
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', ]
    ordering_fields = '__all__'
    search_fields = ['name']
    permit_list_expands = ['category']

    resource_name = 'products'

    def get_permissions(self):
        """
        Set permissions corresponding the actions.
        """
        if self.action in ['list', 'create', 'update', 'partial_update',
                           'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdmin]
            self.filter_class = ProductAdvanceFiltering
        elif self.action in ['search', 'retrieve']:
            self.ordering_fields = ['price']
            self.permission_classes = [AllowAny]
            self.serializer_class = ProductGenerallySerializer

        return super(ProductViewSet, self).get_permissions()

    @action(
        methods=['GET'],
        detail=False,
    )
    def search(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request, *args, **kwargs)


apps = [
    CategoryViewSet,
    ProductViewSet,
    GenderViewSet,
    ArticleTypeViewSet,
    BaseColourViewSet,
    UsageViewSet,
    SeasonViewSet,
]
