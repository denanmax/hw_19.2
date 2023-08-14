from django.urls import path
from . import views
from .models import toggle_activity
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]