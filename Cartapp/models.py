# from django.db import models
# from django.contrib.auth.models import User

# from ..cartService.models import CustomUser

# import uuid




    



# class Category(models.Model):
#     title = models.CharField(max_length=255)
#     category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
#     slug = models.SlugField(default=None)
#     featured_product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='Product')
#     icon = models.CharField(max_length=100, default=None, blank=True, null=True)

#     class Meta:
#         verbose_name_plural = 'Categories'

#     def __str__(self):
#         return self.title

# # Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     discount = models.BooleanField(default=False)
#     image = models.ImageField(upload_to='product_pics/', blank=True, null=True)
#     old_price= models.FloatField(default=0.00)
#     category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
#     slug = models.SlugField(default=None)
#     id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
#     inventory = models.IntegerField(default=5)
#     top_deal= models.BooleanField(default=False)
#     flash_sales = models.BooleanField(default=False)

#     @property
#     def price(self):
#         if self.discount:
#             new_price = self.old_price - ((30/100) * self.old_price)
#         else:
#             new_price = self.old_price
#         return new_price
    
#     def __str__(self):
#         return self.name
    

# class Cart(models.Model):
#     owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     card_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     compeleed = models.BooleanField(default=False)
#     session_id = models.CharField(max_length=100)

#     @property
#     def num_of_items(self):
#         cartitems = self.cartitems_set.all()
#         qtysum = sum([qty.quantity for qty in cartitems])
#         return qtysum
    
#     @property
#     def cart_total(self):
#         cartitems = self.cartitems_set.all()
#         qtysum = sum([qty.subTotal for qty in cartitems])
#         return qtysum
    
#     def __str__(self):
#         return self.card_id