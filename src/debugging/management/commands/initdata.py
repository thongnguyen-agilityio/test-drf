import os
from typing import List

import pandas as pd
from django.core.management.base import BaseCommand
from drf_core.factories import (
    FuzzyInteger,
    FuzzyChoice,
    FuzzyFloat,
)
from accounts.factories import (
    UserFactory,
    SuperUserFactory,
)
from app.constants import OrderStatusesEnum
from customers.models import Customer
from products.factories import (
    ProductFactory,
    CategoryFactory,
    GenderFactory,
    SeasonFactory,
    ArticleTypeFactory,
    BaseColourFactory,
)
from products.models import (
    Category,
    Gender,
    Season,
    ArticleType,
    Usage,
    BaseColour,
)
from orders.factories import (
    OrderFactory,
    OrderItemFactory,
)
from rewards.factories import CouponFactory


class Command(BaseCommand):
    """
    Run initdata command.
    """

    help = 'Init data for the app'

    products: List[ProductFactory] = list()
    customers: List[Customer] = list()
    orders: List[OrderFactory] = list()
    coupons: List[CouponFactory] = list()
    users: List[UserFactory] = list()

    @classmethod
    def _seed_products(cls) -> None:
        """
        Seeding products from CSV file to database.
        """

        # Read products data from csv file.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        raw_data = pd.read_csv(f'{dir_path}/styles.csv', error_bad_lines=False)

        # Seeding parent categories
        [CategoryFactory(name=category)
         for category in raw_data['masterCategory'].unique()]

        # Seeding gender
        [GenderFactory(name=name) for name in raw_data['gender'].unique()]

        # Seeding season
        [SeasonFactory(name=name) for name in raw_data['season'].unique()]

        # Seeding article type
        [ArticleTypeFactory(name=name)
         for name in raw_data['articleType'].unique()]

        # Seeding colour
        [BaseColourFactory(name=name)
         for name in raw_data['baseColour'].unique()]

        for index in range(200):
            name = str(raw_data.at[index, 'productDisplayName'])
            gender = str(raw_data.at[index, 'gender'])
            base_color = str(raw_data.at[index, 'baseColour'])
            usage = str(raw_data.at[index, 'usage'])
            season = str(raw_data.at[index, 'season'])
            article_type = str(raw_data.at[index, 'articleType'])
            sub_cat_name = str(raw_data.at[index, 'subCategory'])
            master_cat_name = str(raw_data.at[index, 'masterCategory'])

            # Find or create category if not existed
            try:
                sub_category_obj = Category.objects.get(name=sub_cat_name)
            except:
                sub_category_obj = None

            try:
                master_category_obj = Category.objects.get(name=master_cat_name)
            except:
                master_category_obj = None

            if not master_category_obj:
                master_category_obj = CategoryFactory(name=master_cat_name)

            if not sub_category_obj:
                sub_category_obj = CategoryFactory(name=sub_cat_name,
                                                   parent=master_category_obj)

            try:
                gender_obj = Gender.objects.get(name=gender)
            except:
                gender_obj = None

            try:
                usage_obj = Usage.objects.get(name=usage)
            except:
                usage_obj = None

            try:
                base_color_obj = BaseColour.objects.get(name=base_color)
            except:
                base_color_obj = None

            try:
                season_obj = Season.objects.get(name=season)
            except:
                season_obj = None

            try:
                article_type_obj = ArticleType.objects.get(name=article_type)
            except:
                article_type_obj = None

            product_data = {
                'name': name,
                'price': FuzzyFloat(10, 200),
                'category': sub_category_obj,
                'gender': gender_obj,
                'base_colour': base_color_obj,
                'season': season_obj,
                'usage': usage_obj,
                'article_type': article_type_obj,
            }

            cls.products.append(ProductFactory(**product_data))
            print(f'Inserted {index} products')

    @classmethod
    def _seed_users(cls):
        """
        Seeding users
        """
        # Seeding super users
        admin = SuperUserFactory(username='admin')
        cls.customers.append(admin.customer)
        cls.users.append(admin)

        # Seeding normal user
        for i in range(100):
            user = UserFactory(username=f'user0{i}', )
            cls.users.append(user)
            cls.customers.append(user.customer)

    @classmethod
    def _seed_coupon(cls) -> None:
        """
        Seeding coupons
        """
        cls.coupons = [CouponFactory() for _ in range(10)]

    @classmethod
    def _seed_orders(cls) -> None:
        """
        Seeding orders
        """
        order_status = [
            OrderStatusesEnum.SHIPPING.value,
            OrderStatusesEnum.WAITING.value,
            OrderStatusesEnum.CANCELED.value,
            OrderStatusesEnum.PAID.value,
            OrderStatusesEnum.IN_PROGRESS.value,
        ]

        for _ in range(50):
            order_obj = OrderFactory(
                user=FuzzyChoice(cls.users).fuzz(),
                status=FuzzyChoice(order_status).fuzz(),
            )
            cls.orders.append(order_obj)

            for _ in range(FuzzyInteger(5, 10).fuzz()):
                OrderItemFactory(order=order_obj,
                                 product=FuzzyChoice(cls.products).fuzz())

    def handle(self, *args, **options) -> None:

        # Seeding users
        self._seed_users()

        # Seeding products
        self._seed_products()

        self._seed_orders()
