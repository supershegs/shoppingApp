import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin, Group,Permission
from .managers import CustomUserManager


from django.conf import settings

# class CustomUser(AbstractBaseUser):
    # email = models.EmailField(unique=True)
    # username = models.CharField(max_length=150, unique=True, default='email')
    # # Add additional fields as needed
    # is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    # objects = CustomUserManager()

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    # # def has_perm(self, perm, obj=None):
    # #     return True

    # # def has_module_perms(self, app_label):
    # #     return True
    # # @property
    # # def is_staff(self):
    # #     return self.is_admin
    

#for 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, default='email')
    # Add additional fields as needed
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    shipping_address = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    age = models.IntegerField()
    # Product_age_limit = models.PositiveIntegerField(default=0)
    
    # Additional fields as needed

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category_pic = models.ImageField(upload_to='category_pics/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
 
class Product(models.Model):
    product_tag = models.CharField(max_length=10)
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=150) 
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField(max_length=255)
    product_pic = models.ImageField(upload_to='product_pics/', blank=True, null=True)
    stock = models.IntegerField()
    imageUrl = models.URLField(max_length=255)
    status = models.BigIntegerField(default=True)
    date_created = models.DateField(auto_now_add= True)

    class Meta:
        #ordering = '-date_created'
        ordering = ['-date_created',]
    
    def __str__(self):
        return "{} {} {}".format(self.product_tag, self.name, self.price)

    # Additional fields as per your requirements
class Order(models.Model):
    order_tag = models.CharField(max_length=10)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} {}".format(self.order_tag, self.product, self.user)
    # Additional fields as per your requirements




class Cart(models.Model):
    cart_tag = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=40, decimal_places=2, default=0)

    class Meta:
        ordering = ['cart_tag', '-created_at']

    def update_total_price(self):
        orders = self.order_set.all()
        total_price = sum(order.product.price * order.product.quantity for order in orders)
        self.total_price = total_price
        self.save()

    def __str__(self):
        return str(self.cart_tag)



