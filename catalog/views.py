from gettext import Catalog

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms import inlineformset_factory

from catalog.froms import ProductForm, CategoryForm, VersionForm
from catalog.models import Product, Contact, Category, Version


class ProductListView(ListView):
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
    form_class = ProductForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super().get_initial()
        initial['lashed'] = self.request.user
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.lashed = self.request.user
        self.object.save()
        return super().form_valid(form)



class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('home')

class CategoryListView(ListView):
    """Главная старница со списком товаров"""
    model = Category

class CategoryView(ListView):
    model = Product
    template_name = 'category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return Product.objects.filter(category=category)

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        CategoryFormset = inlineformset_factory(Category, Product, form=CategoryForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = CategoryFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = CategoryFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
