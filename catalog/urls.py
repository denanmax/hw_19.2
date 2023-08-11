from django.urls import path
from . import views
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
]