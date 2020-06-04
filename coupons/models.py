from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Super Admin'),
        (2, 'Vendor'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default = 1)

    def __str__(self):
        return self.email


class Vendor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='vendor_user')
    name                = models.CharField('Company Name', max_length=30)
    logo                = models.ImageField('Logo', upload_to='')
    about               = models.TextField('About', blank=True)
    email               = models.CharField('Contact email',max_length=100, null=True)
    description         = models.TextField('Description', blank=True)
    address             = models.TextField('Address', blank=True)
    lang                = models.CharField('Longitude', max_length=20)
    latt                = models.CharField('Latitude', max_length=20)

    def __str__(self):
        return self.user.username

class Coupons(models.Model):
    coupon_owner = models.ForeignKey(
        Vendor, on_delete=models.SET(1), related_name='coupon_owner')
    code                = models.CharField('Coupon', max_length=10)
