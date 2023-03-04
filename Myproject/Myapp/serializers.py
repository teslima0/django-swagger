from .models import User
from rest_framework import serializers
from .models import Product
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed 
class UserSerializers(serializers.ModelSerializer):
    """
    Bifrost user writable nested serializer
    """  
    class Meta:
        model = User
        fields = ('url', 'email','username', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


#for login
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255,min_length=3)
    password=serializers.CharField(max_length=68, min_length=6,write_only=True)
    username=serializers.CharField(max_length=255,min_length=3, read_only=True)
    
    tokens=serializers.SerializerMethodField()

    def get_tokens(self,obj):
        user = User.objects.get(email=obj['email'])

        return {
            'access':user.tokens()['access'],
            'refresh':user.tokens()['refresh']
        }
    
    class Meta:
        model=User
        fields=['email','password','username','tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password=attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        attrs['user'] = user
        return attrs
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at']

