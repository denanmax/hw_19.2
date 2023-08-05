from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Contact


def home(request):
    latest_products = Product.objects.order_by('id')[:5:-1]
    cat_list = Product.objects.all()
    context = {
        'object_list': cat_list,
        'latest_products': latest_products
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
