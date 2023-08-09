from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, UserProfile, Category,Product,Order,Cart

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ('email', 'username','password')

class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta: 
        model = CustomUser
        fields = ('email', 'username','password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user','profile_picture', 'shipping_address',
                  'billing_address','phone_number','age']
   
    def create(self, validated_data):
        user = self.context['request'].user

        user_profile = UserProfile.objects.create(
            user=user,
            profile_picture=validated_data.get('profile_picture'),
            shipping_address=validated_data.get('shipping_address', ''),
            billing_address=validated_data.get('billing_address', ''),
            phone_number=validated_data.get('phone_number', ''),
            age=validated_data.get('age', ''),           
        )
        return user_profile
       


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description','category_pic']

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category
    
class ProductSerializer(serializers.ModelSerializer):
    

    # category_id = serializers.PrimaryKeyRelatedField( queryset=Category.objects.all(), source='category', write_only=True)

    # using the category name as the identifier for category instead of category id
    category_name = serializers.CharField(write_only=True)
    category = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['product_tag', 'name','category_name', 'category','brand_name' ,'price', 
                  'quantity', 'description', 'product_pic',
                    'stock', 'imageUrl', 'status', 'date_created']

    def create(self, validated_data):
        # category_id = validated_data.pop('category_id')
        category_name = validated_data.pop('category_name')  # from your input
        # to get the name from the existing category and compare wit your input
        try:
              # to get the name from the existing category and compare wit your input
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError({'category_name': 'Category not found.'})
        # To save it back to the category
        product = Product.objects.create(category=category, **validated_data)
        return product
    
    # Define the method to get the category representation/to display the category in the products fiel
    def get_category(self, obj):
        return CategorySerializer(obj.category).data

class OrderSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    product_name = serializers.CharField(write_only=True, allow_blank=True, required=False)
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)

   
    class Meta:
        model = Order
        # fields = ['order_id', 'user','product']
        fields = ['order_tag', 'user','product_name','product']

    # def create(self, validated_data):
        #  if using product_id send ={"order_tag":"OR0000003","product": "1"} as payload
        # user = self.context['request'].user
        # product = validated_data.get('product')
        # order = Order.objects.create(
        #     order_id=validated_data.get('order_tag'),
        #     user=user,
        #     product=product
        # )
        # return order
        
        #  second option using product name send+{"order_id":"OR0000003","product_name": "Envy 15 X360 11th Gen"} as payload

    def create(self, validated_data):
        user = self.context['request'].user
        product_name = validated_data.pop('product_name')  # from your input
        # to get the name from the existing product and compare wit your input
        try:
              # to get the name from the existing product and compare wit your input
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'product_name': 'product not found.'})
        # To save it back to the product
        order = Order.objects.create(
            order_tag=validated_data.get('order_tag'),
            user=user,
            product=product
        )
        return order

    def update(self, instance, validated_data):
        product_name = validated_data.pop('product_name', None)
        # Update the fields of the Order instance with the provided validated_data
        instance.order_tag = validated_data.get('order_tag', instance.order_tag)
        # Handle updating the associated Product instance
        if product_name:
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                raise serializers.ValidationError({'product_name': 'Product not found.'})
            instance.product = product
        instance.save()
        return instance

        
class CartSerializers(serializers.ModelSerializer):
   
    user = CustomUserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    order_tag = serializers.CharField(write_only=True, allow_blank=True, required=False)
    price = serializers.CharField(write_only=True, allow_blank=True, required=False)

    class Meta:
        model = Cart
        fields = ['id','cart_tag', 'user', 'created_at', 'order_tag', 'order', 'price','total_price']

    def create(self, validated_data):
        user = self.context['request'].user
        order_tag = validated_data.pop('order_tag', None)
        total_price = validated_data.pop('price', None)


        try:
            order = Order.objects.get(order_tag= order_tag)
        except Order.DoesNotExist:
            raise serializers.ValidationError({'order_tag': 'Order not found.'})
        total_price = order.product.price * order.product.quantity
        cart = Cart.objects.create(
            # id = validated_data['id'],
            cart_tag=validated_data.get('cart_tag'),
            user = user,
            created_at=validated_data.get('created_at'),
            order= order,
            total_price = total_price
        )
        return cart
        