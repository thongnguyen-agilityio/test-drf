from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from accounts.serializers import UserSerializer
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
# CategorySerializer
# =============================================================================
class CategorySerializer(FlexFieldsModelSerializer):
    # Serializer for Category model.

    class Meta:
        model = Category
        fields = '__all__'


# =============================================================================
# SeasonSerializer
# =============================================================================
class SeasonSerializer(FlexFieldsModelSerializer):
    # Serializer for Season model.

    class Meta:
        model = Season
        fields = '__all__'


# =============================================================================
# UsageSerializer
# =============================================================================
class UsageSerializer(FlexFieldsModelSerializer):
    # Serializer for Usage model.

    class Meta:
        model = Usage
        fields = '__all__'


# =============================================================================
# BaseColourSerializer
# =============================================================================
class BaseColourSerializer(FlexFieldsModelSerializer):
    # Serializer for BaseColour model.

    class Meta:
        model = BaseColour
        fields = '__all__'


# =============================================================================
# ArticleTypeSerializer
# =============================================================================
class ArticleTypeSerializer(FlexFieldsModelSerializer):
    # Serializer for ArticleType model.

    class Meta:
        model = ArticleType
        fields = '__all__'


# =============================================================================
# GenderSerializer
# =============================================================================
class GenderSerializer(FlexFieldsModelSerializer):
    # Serializer for Gender model.

    class Meta:
        model = Gender
        fields = '__all__'


# =============================================================================
# ProductSerializer
# =============================================================================
class ProductSerializer(FlexFieldsModelSerializer):
    """
    Product serializer for admin user.
    """
    expandable_fields = {
        'category': (CategorySerializer, {'source': 'category'}),
        'gender': (GenderSerializer, {'source': 'gender'}),
        'article_type': (GenderSerializer, {'source': 'article_type'}),
        'base_colour': (BaseColourSerializer, {'source': 'base_colour'}),
        'season': (SeasonSerializer, {'source': 'season'}),
        'usage': (UsageSerializer, {'source': 'usage'}),
        'created_by': (UserSerializer, {'source': 'created_by'}),
        'last_modified_by': (UserSerializer, {'source': 'last_modified_by'}),
    }

    class Meta:
        model = Product
        fields = '__all__'


class ProductGenerallySerializer(serializers.ModelSerializer):
    """
    Product serializer for the general user.
    """
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'quantity',
            'sold_quantity'
        ]
        read_only_fields = fields
