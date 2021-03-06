# Generated by Django 3.0.4 on 2020-06-10 08:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rewards', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('archived', models.BooleanField(db_index=True, default=False)),
                ('status', models.IntegerField(choices=[('PAID', 0), ('CANCEL', 1), ('PENDING', 2)], default=2)),
                ('total_amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('total_pay_amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.AddressBook', validators=[django.core.validators.MinValueValidator(0)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('archived', models.BooleanField(db_index=True, default=False)),
                ('total_amount', models.FloatField(default=0, help_text='Total amount of an order', validators=[django.core.validators.MinValueValidator(0)])),
                ('total_pay_amount', models.FloatField(default=0, help_text='The actual amount that customer need to pay', validators=[django.core.validators.MinValueValidator(0)])),
                ('earning_point', models.IntegerField(default=0, help_text='Number of point of an order that customer earns', validators=[django.core.validators.MinValueValidator(0)])),
                ('burning_point', models.IntegerField(default=0, help_text='Number of point that customer spend to redeem product', validators=[django.core.validators.MinValueValidator(0)])),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rewards.Coupon')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transaction_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('order', models.OneToOneField(help_text='The order which transaction belong to', on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('user', models.ForeignKey(help_text='The user who own this transaction', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('archived', models.BooleanField(db_index=True, default=False)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('copy_price', models.FloatField(default=0, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderitem_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderitem_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
