from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import Token # use accesstoken instead ot Token
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist





from .models import Category,Product, UserProfile, Order, Cart
from .serializers import UserRegistrationSerializer, UserAuthenticationSerializer, User, CustomUserSerializer, UserProfileSerializer
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, CartSerializers

class test(APIView):
    permission_classes =[AllowAny]
    def get(self, request):
        return Response({
            'Message': 'Welcome baller!'
        })

class UserRegistrationView(APIView):
    permission_classes =[AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response({'token': str(access)})
        return Response(serializer.errors, status=400)


class CustomerView(APIView):
    permission_classes =[AllowAny]
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return Response({'token': str(access)})
        return Response(serializer.errors, status=400)
    
class UserAuthenticationView(APIView):
    permission_classes =[AllowAny]
    def post(self, request):
        serializer = UserAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Invalid email or password'}, status=400)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token
                return Response({'token': str(access)})
            else:
                return Response({'error': 'Invalid email or password'}, status=400)

        return Response(serializer.errors, status=400)



    

class profile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        if request.user.is_authenticated:    
            serializer = UserProfileSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User Profile created successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(data=request.data, instance=user_profile, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Profile updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class CategoryView(APIView):
    permission_classes =[AllowAny]
    def get(self, request, category_id=None):
        if category_id is not None:
            try:
                category = Category.objects.get(pk=category_id)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({'message': 'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class ProductView(APIView):
    permission_classes= [AllowAny]
    def get(self, request, product_id = None):
        if product_id is not None:
            try:
                product = Product.objects.get(pk=product_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many= True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, product_id):
        try:
            category = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({'message': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    
class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, order_id = None):
        if order_id is not None:
            try:
                # order = Order.objects.filter(pk=order_id, user=request.user) the serializer is expecting a single instance to serialize, not a queryset.
                order = Order.objects.get(pk=order_id, user=request.user)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        else:    
            try:
                # since we expect multiply orders as per each user. filter() is used instead of get() 
                order = Order.objects.filter(user=request.user)
                serializer = OrderSerializer(order, many=True)
                if serializer.data == []:
                    return Response({'message': 'User has not made any orders.'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({'message': 'User can not make Order.'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        if request.user.is_authenticated:
            serializer = OrderSerializer(data=request.data, context= {'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Order made successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'message': 'order not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Order updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        if order_id is not None:
            try:
                order = Order.objects.get(pk=order_id, user=request.user)
            except Order.DoesNotExist:
                return Response({'message': 'order not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            order.delete()
            return Response({'message': 'Order deleted successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Select Order to delete'}, status=status.HTTP_404_NOT_FOUND)
            

class CartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, cart_id = None):
        if cart_id is not None: 
            try:
                cart = Cart.objects.get(pk=cart_id, user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response({'message': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)       
        else:    
            try:
            
                # since we expect multiply orders as per each user. filter() is used instead of get() 
                cart = Cart.objects.filter(user=request.user)
                print(cart_id)
                serializer = CartSerializers(cart, many=True)
                if serializer.data == []:
                    return Response({'message': 'No cart for user.'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response({'message': 'No cart created presently.'}, status=status.HTTP_404_NOT_FOUND)
            

    def post(self, request):
        if request.user.is_authenticated:
            serializer = CartSerializers(data=request.data, context= {'request': request})
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Cart made successfully.'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)