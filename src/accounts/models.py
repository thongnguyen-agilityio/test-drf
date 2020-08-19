from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token # noqa
from django.db import models

from drf_core.models import (
    create_api_key,
    QuerySet,
)
from drf_core import fields
from app.constants import UserRolesEnum
from customers.models import (
    Email,
    Customer,
)


class User(AbstractUser):
    """
    User model.
    """

    role = fields.IntegerField(
        choices=UserRolesEnum.to_tuple(),
        default=UserRolesEnum.CUSTOMER_ROLE.value,
    )

    @property
    def is_user(self):
        return hasattr(self, 'role') and self.role in \
               [UserRolesEnum.USER_ROLE.value]

    @property
    def is_admin(self):
        return hasattr(self, 'role') and self.role in \
               [UserRolesEnum.ADMIN_ROLE.value]

    @property
    def is_customer(self):
        return hasattr(self, 'role') and self.role in \
               [UserRolesEnum.CUSTOMER_ROLE.value]

    def save(self, *args, **kwargs) -> None:
        """
        Create new user and also create customer.
        If user is existed, update user and update related customer.
        """
        try:
            user_full_name = self.get_full_name() if self.get_full_name() \
                else self.username

            # New object
            if self.pk is None:
                super(User, self).save(*args, **kwargs)
                email_obj = Email.objects.create(email=self.email)
                Customer.objects.create(
                    email=email_obj,
                    account=self,
                    name=user_full_name,
                )
            # Update existing object.
            else:
                super(User, self).save(*args, **kwargs)
                customer_obj = Customer.objects.get(account=self)

                if customer_obj.email is not None:
                    customer_obj.email.email = self.email
                    customer_obj.email.save()

                customer_obj.name = user_full_name
                customer_obj.save()
        except Exception as e:
            raise e


# Automatically generates API key for the user.
models.signals.post_save.connect(create_api_key, sender=User)
