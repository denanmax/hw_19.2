from django.shortcuts import render

from catalog.models import Product, Contact


def home(request):
    latest_products = Product.objects.order_by('id')[:5:-1]
    for product in latest_products:
        print(product.name)  # Пример вывода имени товара в консоль
    return render(request, 'catalog/home.html', {'latest_products': latest_products})


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