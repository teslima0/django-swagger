from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets, generics,status
from .serializers import LoginSerializer,UserSerializers,ProductSerializer
from .models import User,Product
from .permission import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

class ProductRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDestroy(generics.DestroyAPIView):
    queryset = Product.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Deleted', status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializers

        # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class LoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    permission_classes=[permissions.AllowAny]
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception= True)

        return Response(serializer.data, status=status.HTTP_200_OK)

