from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='name')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description Product')
    category = models.ForeignKey('webapp.Category', related_name='tracker', on_delete=models.PROTECT,
                                 verbose_name='Product category', blank=False, null=False, default='other')
    image = models.ImageField(null=True, blank=True, upload_to='product_pics', verbose_name='image')

    def __str__(self):
        return self.name


class Category(models.Model):
    status = models.CharField(max_length=40, null=False, blank=False, verbose_name='Status')

    def __str__(self):
        return self.status


def get_admin():
    return User.objects.get(username='admin').id


class Review(models.Model):
    author = models.ForeignKey(User, null=False, blank=False, default=get_admin, verbose_name='author',
                               on_delete=models.PROTECT, related_name='tracker_by')
    product = models.ForeignKey('webapp.Product', related_name='product_review',
                                on_delete=models.CASCADE, verbose_name='product')
    review = models.TextField(max_length=2000, verbose_name='review')
    assessment = models.PositiveSmallIntegerField(max_length=1, verbose_name='assessment',
                                                  validators=(1, 5))

    def __str__(self):
        return self.review
