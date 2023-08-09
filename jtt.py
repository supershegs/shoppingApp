import os

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)'
secret_key = ''.join([os.urandom(1).hex() for _ in range(50)])





    
# CartSerializers(context={'request': <rest_framework.request.Request: POST '/carts/'>}, data={'order_tag': 'OR0000001'}):
#     cart_tag = UUIDField(read_only=True)
#     user = CustomUserSerializer(read_only=True):
#         email = EmailField(max_length=254, validators=[<UniqueValidator(queryset=CustomUser.objects.all())>])
#         username = CharField(max_length=150, required=False, validators=[<UniqueValidator(queryset=CustomUser.objects.all())>])
#         password = CharField(write_only=True)
#     created_at = DateTimeField(read_only=True)
#     order_tag = CharField(allow_blank=True, required=False, write_only=True)
#     order = OrderSerializer(read_only=True):
#         order_tag = CharField(max_length=10)
#         user = CustomUserSerializer(read_only=True):
#             email = EmailField(max_length=254, validators=[<UniqueValidator(queryset=CustomUser.objects.all())>])
#             username = CharField(max_length=150, required=False, validators=[<UniqueValidator(queryset=CustomUser.objects.all())>])
#             password = CharField(write_only=True)
#         product_name = CharField(allow_blank=True, required=False, write_only=True)
#         product = ProductSerializer(read_only=True):
#             product_tag = CharField(max_length=10)
#             name = CharField(max_length=150)
#             category_name = CharField(write_only=True)
#             category = SerializerMethodField()
#             brand_name = CharField(max_length=150)
#             price = IntegerField()
#             quantity = IntegerField()
#             description = CharField(max_length=255, style={'base_template': 'textarea.html'})
#             product_pic = ImageField(allow_null=True, max_length=100, required=False)
#             stock = IntegerField()
#             imageUrl = URLField(label='ImageUrl', max_length=255)
#             status = IntegerField(required=False)
#             date_created = DateField(read_only=True)
#     price = CharField(allow_blank=True, required=False, write_only=True)
#     total_price = DecimalField(decimal_places=2, max_digits=10, required=False)