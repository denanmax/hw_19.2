from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from catalog.models import Product, Contact, Category

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'product'  # Optional: specify the name of the context variable

def home(request):
    latest_products = Product.objects.order_by('id')[:5:-1]
    cat_list = Product.objects.all()
    context = {
        'object_list': cat_list,
        'latest_products': latest_products,
        'title': 'TOSYASTORE'
    }
    return render(request, 'catalog/home.html', context)


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
