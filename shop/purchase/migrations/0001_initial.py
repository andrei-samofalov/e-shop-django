# Generated by Django 4.2 on 2023-04-20 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='regular', max_length=50, verbose_name='type')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='cost of delivery')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'delivery type',
                'verbose_name_plural': 'delivery types',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
                ('paymentType', models.CharField(choices=[('онлайн за свой счет', 'Own Online'), ('онлайн за чужой счет', 'Someone Online')], default='онлайн за свой счет', verbose_name='type of payment')),
                ('status', models.CharField(choices=[('принят', 'Accepted'), ('ожидает оплаты', 'Awaiting Payment'), ('оплачен', 'Paid'), ('доставлен', 'Delivered')], default='принят', verbose_name='status')),
                ('city', models.CharField(default='', max_length=100, verbose_name='city')),
                ('address', models.TextField(default='', verbose_name='address')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='accounts.profile', verbose_name='buyer')),
                ('deliveryType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='purchase.deliverytype', verbose_name='delivery type')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='quantity')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='purchase.order', verbose_name='order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='catalog.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product in order',
                'verbose_name_plural': 'products in order',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, through='purchase.OrderItem', to='catalog.product', verbose_name='products'),
        ),
    ]
