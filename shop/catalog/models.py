from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from catalog.choices import RateChoices
from catalog.service import (
    category_images_directory_path,
    product_images_directory_path,
    random_category_image,
)


class Product(models.Model):
    """Model of the Product

    attrs:
        `category`: fk - link to product's category (catalog.models.Category);
        `price`: decimal - product's price;
        `stock`: integer - available stock of the product;
        `count`: integer - needed in serialization, does nothing;
        `title`: string - human-readable title of the product;
        `fullDescription`: string - full description of the product;
        `freeDelivery`: boolean - defines type of delivery (free or not);
        `is_active`: boolean - defines status of the product
            (deactivate products is a smart delete option);
        `created_at`: datetime - timestamp,
            defines when the product was created, generates automatically;
        `updated_at`: datetime - timestamp, defines when the product was changed
            (e.i. product stock or price was updated),
            generates automatically;
        `specifications`: fk - link to product's specifications
            (catalog.models.Specification);
        `tags`: fk - link to product's tags (catalog.models.Tag);
        `is_limited`: boolean - defines whether product is limited;
    properties:
        available;
        date;
        description;
        href;
        rating;
    other relations:
        (model = related name)
        catalog.models.ProductImage = images;
        catalog.models.Review = reviews;



    """
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET('undefined'),
        related_name='products',
        verbose_name=_('category'),
        help_text=_('product category')
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=100,
        default=0,
        verbose_name=_('price'),
        help_text=_('price of the product')
    )
    stock = models.IntegerField(
        default=10,
        verbose_name=_('stock'),
        help_text=_('available stock of the product')
    )
    count = models.IntegerField(
        default=0,
        verbose_name=_('count'),
        help_text=_('do nothing, needed by frontend')
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('product'),
        help_text=_('human-readable title of the product')
    )
    fullDescription = models.TextField(
        default='',
        blank=True,
        verbose_name=_('full description'),
        help_text=_('full description of the product')
    )
    freeDelivery = models.BooleanField(
        default=False,
        verbose_name=_('free delivery'),
        help_text=_('type of delivery - free or not')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('active'),
        help_text=_('soft-delete option')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created'),
        help_text=_('timestamp when product was created')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated'),
        help_text=_('timestamp when product was updated')
    )
    specifications = models.ManyToManyField(
        'Specification',
        related_name='products',
        verbose_name=_('specifications'),
        blank=True,
        help_text=_('specifications of the product')
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='products',
        verbose_name=_('tags'),
        blank=True,
        help_text=_('keywords with which the product is tagged')
    )
    is_limited = models.BooleanField(
        default=False,
        help_text=_('adds limited status to the product')
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        indexes = (models.Index('title', name='title'),)
        ordering = ('stock',)

    @property
    def available(self):
        """
        Return True if stock of the product greater than zero otherwise False.
        """
        return self.stock > 0

    @property
    def date(self):
        """Return alias for self.created_at."""
        return self.created_at

    @property
    def description(self):
        """Return short description of the product."""
        return self.fullDescription[:100] + '...'

    @property
    def href(self):
        """Return url of the product."""
        return reverse('frontend:product', kwargs={'pk': self.pk})

    @property
    def rating(self):
        """
        Return average rating of the product based on reviews.
        If there is no reviews to this product yet return `not rated yet`
        """
        return round(
            Review.objects.select_related('product')
            .filter(product=self)
            .aggregate(models.Avg('rate'))
            .get('rate__avg'), 2
        ) or "not rated yet"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """
    Image model for the product
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('product'),
        help_text=_('the product to which the images refer')
    )
    image = models.ImageField(
        upload_to=product_images_directory_path,
        verbose_name=_('image'),
        default='fixtures/images/notebook.png',
        help_text=_('image file'),
    )

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')

    @property
    def src(self):
        """
        Image's src, needed by frontend
        :return: string
        """
        return self.image.url

    @property
    def alt(self):
        """
        Image's alt, needed by frontend,
        returns product title for human-readability
        :return: string
        """
        return self.product.title

    def __str__(self):
        return '{} {}'.format(self.product.title, _('image'))


class Category(models.Model):
    title = models.CharField(
        max_length=100, verbose_name=_('title'), unique=True
    )
    picture = models.ImageField(
        upload_to=category_images_directory_path,
        verbose_name=_('image'),
        default=random_category_image,
    )
    subcategories = models.ManyToManyField(
        'self', verbose_name=_('subcategory'), symmetrical=False, blank=True
    )

    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def image(self):
        return {"src": self.picture.url, "alt": self.title}

    def href(self):
        return f'/catalog/{self.pk}'
        # return reverse('frontend:catalog', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('name'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('product'),
    )
    author = models.CharField(
        max_length=100, blank=True, default='', verbose_name=_('author')
    )
    text = models.TextField(blank=True, default='', verbose_name=_('text'))
    rate = models.PositiveSmallIntegerField(
        choices=RateChoices.choices,
        default=RateChoices.VERY_GOOD,
        verbose_name=_('rate')
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))
    email = models.EmailField(blank=True, default='', verbose_name=_('email'))

    class Meta:
        verbose_name = _('review')
        verbose_name_plural = _('reviews')

    def __str__(self):
        return f'{self.product.title} review by {self.author}'


class Specification(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    value = models.CharField(max_length=50, verbose_name=_('value'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name = _('specification')
        verbose_name_plural = _('specifications')
        unique_together = ('name', 'value')

    def __str__(self):
        return f'Spec ({self.name}: {self.value})'


class ProductOffer(models.Model):
    dateFrom = models.DateField(verbose_name=_('start date'))
    dateTo = models.DateField(verbose_name=_('end date'))
    salePrice = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_('offer price'),
        default=0,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='offers',
    )
    is_active = models.BooleanField(default=True, verbose_name=_('active'))

    class Meta:
        verbose_name = _('product offer')
        verbose_name_plural = _('product offers')
