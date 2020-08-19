from django.contrib import admin
from drf_core.admin import BaseModelAdmin

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
@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    list_display = [
        'name',
        'parent',
    ]


# =============================================================================
# Season
# =============================================================================
@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = [
        'name',
    ]


# =============================================================================
# Usage
# =============================================================================
@admin.register(Usage)
class UsageAdmin(BaseModelAdmin):
    list_display = [
        'name',
    ]


# =============================================================================
# BaseColour
# =============================================================================
@admin.register(BaseColour)
class BaseColourAdmin(BaseModelAdmin):
    list_display = [
        'name',
    ]


# =============================================================================
# ArticleType
# =============================================================================
@admin.register(ArticleType)
class ArticleTypeAdmin(BaseModelAdmin):
    list_display = [
        'name',
    ]


# =============================================================================
# Gender
# =============================================================================
@admin.register(Gender)
class GenderAdmin(BaseModelAdmin):
    list_display = [
        'name',
    ]


# =============================================================================
# Product
# =============================================================================
@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    list_display = [
        'name',
        'price',
        'category',
        'gender',
        'base_colour',
        'season',
        'usage',
    ]
