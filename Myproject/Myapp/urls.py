from django.urls import path
from . import views

urlpatterns = [
    path ('login/',views.LoginAPIView.as_view(), name = 'login'),   
    path('products/', views.ProductList.as_view()),
    path('products/create/', views.ProductCreate.as_view()),
    path('products/<int:pk>/', views.ProductRetrieveUpdate.as_view()),
    path('products/<int:pk>/delete/', views.ProductDestroy.as_view()), 
]