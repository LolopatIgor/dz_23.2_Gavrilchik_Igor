from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ContactsPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "contacts.html")


def contacts(request):
    return render(request, 'contacts.html')
