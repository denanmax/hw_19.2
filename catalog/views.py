from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product, Contact, Category

class ProductListView(ListView):
    """Главная старница со списком товаров"""
    model = Product

class ProductDetailView(DetailView):
    model = Product


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
    return render(request, 'catalog/product_detail.html', {'product': product})

class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'preview_image', 'category', 'price')
    success_url = reverse_lazy('home')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'preview_image', 'category', 'price')
    success_url = reverse_lazy('home')

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('home')
