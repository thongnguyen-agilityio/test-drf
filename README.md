# Big practice 2: Online Fashion Shop Membership Management 

Design all APIs for the product.

Implement APIs focus on `Orders`, `Shopping cart` and `Products`.

All documentation: [HERE](https://docs.google.com/document/d/1VnY_uCJuTMP0jZPBJl8wk2s7AUu6Gek73X9hkf2UHMM/edit)

## Versioning

  * [Python v3.8.1](https://www.python.org/)
  * [Django v3.0.4](https://www.djangoproject.com/)
  * [Django REST framework v3.11.0](https://www.django-rest-framework.org/)

## Technical Stack

  * Django REST framework - For RESTful APIs
  * Coverage - Report coverage of unit testing
  * drf-yasg - Generate API document
  * factory-boy - Initialize fake data
  * Faker - Initialize fake data

## Development Environment

### How to run

**Run with `virtualenvwrapper` at local environment**

1. Installing mkvirtualenv

Install `pyenv` https://bgasparotto.com/install-pyenv-ubuntu-debian

Install python 3.8.0

```
pyenv install 3.8.0
```

Set version python 

```
pyenv global 3.8.0
```

Install `virtualenvwrapper`

```
pip install virtualenvwrapper
```

Add command below to end of `~/.bashrc` or `~/.zshrc`

```
$(pyenv root)/versions/3.8.0/bin/virtualenvwrapper.sh
```


This project uses [mkvirtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html) for virtual environment.

```
mkvirtualenv my_env
```

Environment `my_env` will be activated after running command but if not, you can activate with the command below

```
workon my_env
```

2. Install python packages.

```
pip install -r requirements/all.txt
```

3. Seeding the test data

```
bin/dj-initdata.sh
```

4. Start the server

```
bin/dj-run.sh
```

**Run with Docker compose**

1. Build docker images
```
docker-compose build
```

2. Get Docker compose up

```
docker-compose up
```

Go to [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) to view all APIs.

Login with dummy username/password: `admin`/`123456`

### Browsable APIs

After the server is up, you can go to [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) to checkout the browsable APIs.

Note: Focus to implement full API for `Order`, `Cart`, `Product`. The others 
might be missing some API which designed on the API design document below.

```
Api Root
The default basic root view for DefaultRouter

GET /api/v1/
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "customers": "http://localhost:8000/api/v1/customers/",
    "cart/me": "http://localhost:8000/api/v1/cart/me/",
    "cart/me/shipping_address": "http://localhost:8000/api/v1/cart/me/shipping_address/",
    "cart/me/coupons": "http://localhost:8000/api/v1/cart/me/coupons/",
    "cart/me/items": "http://localhost:8000/api/v1/cart/me/items/",
    "orders": "http://localhost:8000/api/v1/orders/",
    "orders/me": "http://localhost:8000/api/v1/orders/me/",
    "transactions": "http://localhost:8000/api/v1/transactions/",
    "categories": "http://localhost:8000/api/v1/categories/",
    "products": "http://localhost:8000/api/v1/products/",
    "genders": "http://localhost:8000/api/v1/genders/",
    "articletypes": "http://localhost:8000/api/v1/articletypes/",
    "basecolours": "http://localhost:8000/api/v1/basecolours/",
    "usages": "http://localhost:8000/api/v1/usages/",
    "seasons": "http://localhost:8000/api/v1/seasons/"
}
```

### Documentations

Design documents

- Specification
- Database Design
- API Goals canvas
- API design

https://docs.google.com/document/d/1VnY_uCJuTMP0jZPBJl8wk2s7AUu6Gek73X9hkf2UHMM/edit

Generated documentation
- OpenAPI: http://127.0.0.1:8000/openapi/
- Swagger: http://127.0.0.1:8000/swagger/
- Redoc: http://127.0.0.1:8000/redoc/

### Unit Testing and coverage

For unit testing, this project use a customize test suite of Django REST framework.

[Coverage](https://coverage.readthedocs.io/en/v4.5.x/) is used to generate reports about code coverage.

#### How to run and report coverage

To run all tests:

```
bin/dj-test.sh
```

To generate coverage report of unit testing:

```
bin/report-coverage.sh
```

```
Name                                                             Stmts   Miss  Cover   Missing
----------------------------------------------------------------------------------------------
src/accounts/__init__.py                                             2      0   100%
src/accounts/apis.py                                                23      1    96%   64
src/accounts/factories.py                                           29      0   100%
src/accounts/migrations/0001_initial.py                              8      0   100%
src/accounts/migrations/__init__.py                                  0      0   100%
src/accounts/models.py                                              35      4    89%   29, 39, 71-72
src/accounts/permission.py                                           8      1    88%   13
src/accounts/serializers.py                                         15      0   100%
src/accounts/tests/__init__.py                                       0      0   100%
src/accounts/tests/models/__init__.py                                0      0   100%
src/accounts/tests/models/test_user_models.py                       30      0   100%
src/accounts/tests/test_apis_users.py                               19      0   100%
src/apis/__init__.py                                                 0      0   100%
src/apis/urls.py                                                    19      0   100%
src/app/__init__.py                                                  0      0   100%
src/app/constants.py                                                43      7    84%   26, 40, 47, 54-58
src/app/settings/__init__.py                                         7      0   100%
src/app/settings/components/__init__.py                              2      0   100%
src/app/settings/components/authentication.py                        5      0   100%
src/app/settings/components/common.py                               20      0   100%
src/app/settings/components/database.py                              3      0   100%
src/app/settings/components/logging.py                               2      0   100%
src/app/settings/environments/__init__.py                            0      0   100%
src/app/settings/environments/local.py                               4      0   100%
src/app/settings/environments/test.py                                4      0   100%
src/app/urls.py                                                     10      1    90%   47
src/core/apis.py                                                     4      0   100%
src/core/pagination/custom_pagination.py                            19      0   100%
src/core/tests/base.py                                              21      0   100%
src/customers/__init__.py                                            2      0   100%
src/customers/admin.py                                               9      0   100%
src/customers/apis.py                                               22      0   100%
src/customers/factories.py                                          34      0   100%
src/customers/filters.py                                            10      0   100%
src/customers/migrations/0001_initial.py                            10      0   100%
src/customers/migrations/__init__.py                                 0      0   100%
src/customers/models.py                                             77      6    92%   111, 174-180, 208-209
src/customers/serializers.py                                        12      0   100%
src/customers/tests/__init__.py                                      0      0   100%
src/customers/tests/apis/__init__.py                                 0      0   100%
src/customers/tests/apis/test_customer_apis.py                       0      0   100%
src/customers/tests/models/__init__.py                               0      0   100%
src/customers/tests/models/test_customer_models.py                  53      0   100%
src/customers/tests/models/test_membership_level_models.py          36      0   100%
src/customers/tests/models/test_membership_models.py                35      0   100%
src/debugging/__init__.py                                            0      0   100%
src/debugging/management/commands/__init__.py                        2      0   100%
src/debugging/management/commands/initmembershiplevels.py           27      2    93%   53-54
src/manage.py                                                        9      2    78%   9-10
src/orders/__init__.py                                               2      0   100%
src/orders/admin.py                                                  7      0   100%
src/orders/apis/cart.py                                            160     14    91%   40, 45, 54, 85-86, 93, 98, 125, 186, 192-193, 228, 281-282
src/orders/apis/orders.py                                           66      1    98%   51
src/orders/factories.py                                             26      0   100%
src/orders/filters.py                                               14      0   100%
src/orders/migrations/0001_initial.py                                9      0   100%
src/orders/migrations/0002_auto_20200611_0253.py                     6      0   100%
src/orders/migrations/0003_auto_20200611_0900.py                     6      0   100%
src/orders/migrations/0004_auto_20200611_0948.py                     4      0   100%
src/orders/migrations/0005_auto_20200612_0801.py                     6      0   100%
src/orders/migrations/0006_auto_20200701_0841.py                     5      0   100%
src/orders/migrations/0007_order_burning_point.py                    4      0   100%
src/orders/migrations/0008_order_num_of_items.py                     4      0   100%
src/orders/migrations/0009_auto_20200702_0209.py                     7      0   100%
src/orders/migrations/0010_remove_order_total_pay_amount.py          4      0   100%
src/orders/migrations/__init__.py                                    0      0   100%
src/orders/models.py                                               113     14    88%   72-75, 91, 98-104, 214, 225-226, 238-244
src/orders/serializers.py                                           27      0   100%
src/orders/tests/__init__.py                                         0      0   100%
src/orders/tests/apis/__init__.py                                    0      0   100%
src/orders/tests/apis/test_cart_apis.py                            169      0   100%
src/orders/tests/apis/test_cart_apis_no_login_required.py           56      0   100%
src/orders/tests/apis/test_order_apis.py                            69      0   100%
src/orders/tests/apis/test_order_apis_no_login_required.py          26      0   100%
src/orders/tests/models/__init__.py                                  0      0   100%
src/orders/tests/models/test_order_models.py                        60      0   100%
src/orders/tests/models/test_orderitem_models.py                    68      7    90%   59-69
src/products/__init__.py                                             2      0   100%
src/products/admin.py                                               24      0   100%
src/products/apis.py                                                78      0   100%
src/products/factories.py                                           61      0   100%
src/products/filters.py                                             62     12    81%   108, 123-145
src/products/migrations/0001_initial.py                             10      0   100%
src/products/migrations/__init__.py                                  0      0   100%
src/products/models.py                                              79     11    86%   42, 57, 72, 87, 102, 117, 225-231
src/products/serializers.py                                         38      0   100%
src/products/tests/__init__.py                                       0      0   100%
src/products/tests/apis/__init__.py                                  0      0   100%
src/products/tests/apis/test_category_apis.py                       71      0   100%
src/products/tests/apis/test_product_api_base.py                    22      0   100%
src/products/tests/apis/test_product_apis_admin_user.py             44      0   100%
src/products/tests/apis/test_product_apis_general_user.py           25      0   100%
src/products/tests/apis/test_product_apis_no_login_required.py      28      0   100%
src/products/tests/models/__init__.py                                0      0   100%
src/products/tests/models/base_test_case.py                         22      0   100%
src/products/tests/models/test_articletype_models.py                 9      2    78%   12-15
src/products/tests/models/test_basecolour_models.py                 10      0   100%
src/products/tests/models/test_category_models.py                   19      0   100%
src/products/tests/models/test_gender_models.py                     10      0   100%
src/products/tests/models/test_product_models.py                    22      0   100%
src/products/tests/models/test_redeeming_product_models.py          15      0   100%
src/products/tests/models/test_season_models.py                     10      0   100%
src/products/tests/models/test_usage_models.py                       9      2    78%   11-14
src/rewards/__init__.py                                              0      0   100%
src/rewards/admin.py                                                 9      0   100%
src/rewards/factories.py                                            29      0   100%
src/rewards/migrations/0001_initial.py                               9      0   100%
src/rewards/migrations/__init__.py                                   0      0   100%
src/rewards/models.py                                               53      3    94%   93, 126, 182
src/rewards/tests/__init__.py                                        0      0   100%
src/rewards/tests/apis/__init__.py                                   0      0   100%
src/rewards/tests/apis/test_coupon_apis.py                           0      0   100%
src/rewards/tests/apis/test_gift_apis.py                             0      0   100%
src/rewards/tests/apis/test_reward_apis.py                           0      0   100%
src/rewards/tests/models/__init__.py                                 0      0   100%
src/rewards/tests/models/test_coupon_models.py                      48      0   100%
src/rewards/tests/models/test_gift_models.py                        36      0   100%
src/rewards/tests/models/test_reward_models.py                      35      0   100%
src/utils/custom_exception_handler.py                               22      0   100%
src/utils/custom_exceptions.py                                      86      1    99%   38
----------------------------------------------------------------------------------------------
TOTAL                                                             2585     91    96%
```

## Reference

- [SwaggerUI inside Django Rest Framework](https://dev.to/matthewhegarty/swaggerui-inside-django-rest-framework-1c2p)
