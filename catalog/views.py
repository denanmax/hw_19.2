from django.shortcuts import render
from django.views.generic import ListView, DetailView

from catalog.models import Product, Contact, Category

class ProductListView(ListView):
    """Главная старница со списком товаров"""
    model = Product
    template_name = 'catalog/home.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, phone=phone, message=message)
        contact.save()
        print(f"{name}, {phone}, {message}")

    contacts = Contact.objects.all()
    return render(request, 'catalog/contacts.html', {'contacts': contacts})

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, 'catalog/product.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        preview_image = request.FILES.get('preview_image')
        category_id = request.POST.get('category')
        price = request.POST.get('price')

        category = Category.objects.get(id=category_id)
        product = Product(name=name, description=description, preview_image=preview_image, category=category, price=price)
        product.save()

    categories = Category.objects.all()
    return render(request, 'catalog/add_product.html', {'categories': categories})
