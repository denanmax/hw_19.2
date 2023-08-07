from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts),
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:product_id>/', views.product, name='product'),

]