# Generated by Django 4.2 on 2023-04-20 20:06

import catalog.service
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title')),
                ('picture', models.ImageField(default=catalog.service.random_category_image, upload_to=catalog.service.category_images_directory_path, verbose_name='image')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('subcategories', models.ManyToManyField(blank=True, to='catalog.category', verbose_name='subcategory')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, help_text='price of the product', max_digits=100, verbose_name='price')),
                ('stock', models.IntegerField(default=10, help_text='available stock of the product', verbose_name='stock')),
                ('count', models.IntegerField(default=0, help_text='do nothing, needed by frontend', verbose_name='count')),
                ('title', models.CharField(help_text='human-readable title of the product', max_length=100, unique=True, verbose_name='product')),
                ('fullDescription', models.TextField(blank=True, default='', help_text='full description of the product', verbose_name='full description')),
                ('freeDelivery', models.BooleanField(default=False, help_text='type of delivery - free or not', verbose_name='free delivery')),
                ('is_active', models.BooleanField(default=True, help_text='soft-delete option', verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='timestamp when product was created', verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='timestamp when product was updated', verbose_name='updated')),
                ('is_limited', models.BooleanField(default=False, help_text='adds limited status to the product')),
                ('category', models.ForeignKey(help_text='product category', on_delete=models.SET('undefined'), related_name='products', to='catalog.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('stock',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('value', models.CharField(max_length=50, verbose_name='value')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'specification',
                'verbose_name_plural': 'specifications',
                'unique_together': {('name', 'value')},
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, default='', max_length=100, verbose_name='author')),
                ('text', models.TextField(blank=True, default='', verbose_name='text')),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, 'Very Bad'), (2, 'Bad'), (3, 'Not Bad'), (4, 'Good'), (5, 'Very Good')], default=5, verbose_name='rate')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('email', models.EmailField(blank=True, default='', max_length=254, verbose_name='email')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='catalog.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='ProductOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateFrom', models.DateField(verbose_name='start date')),
                ('dateTo', models.DateField(verbose_name='end date')),
                ('salePrice', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='offer price')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='catalog.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product offer',
                'verbose_name_plural': 'product offers',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='fixtures/images/notebook.png', help_text='image file', upload_to=catalog.service.product_images_directory_path, verbose_name='image')),
                ('product', models.ForeignKey(help_text='the product to which the images refer', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product image',
                'verbose_name_plural': 'product images',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.ManyToManyField(blank=True, help_text='specifications of the product', related_name='products', to='catalog.specification', verbose_name='specifications'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='keywords with which the product is tagged', related_name='products', to='catalog.tag', verbose_name='tags'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(models.F('title'), name='title'),
        ),
    ]
