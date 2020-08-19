# Generated by Django 3.0.4 on 2020-07-02 02:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0001_initial'),
        ('orders', '0008_order_num_of_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='num_of_items',
        ),
        migrations.AlterField(
            model_name='order',
            name='burning_point',
            field=models.IntegerField(default=0, help_text='Number of points which used to redeem products'),
        ),
        migrations.AlterField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(default=None, help_text='The coupon', null=True, on_delete=django.db.models.deletion.SET_NULL, to='rewards.Coupon'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(default=None, help_text='The shipping address', null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.AddressBook'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[('SHOPPING', 0), ('WAITING', 1), ('IN_PROGRESS', 2), ('SHIPPING', 3), ('PAID', 4), ('CANCELED', 5)], default=0, help_text='The order status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.FloatField(default=0, help_text='Total amount before applying coupon and points', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_pay_amount',
            field=models.FloatField(default=0, help_text='Total pay amount after applying coupon and points', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(help_text='The owner of the order', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
