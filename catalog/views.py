from django.shortcuts import render, get_object_or_404
from catalog.models import Product


def home(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list
    }
    return render(request, 'home.html', context)


def contacts(request):
    return render(request, 'contacts.html')


def product_detail(request, pk):
    # Получаем объект продукта по его первичному ключу (pk)
    product = Product.objects.get(pk=pk)
    print(product.image)
    # Контекст для шаблона

    context = {
        'product_item': product
    }

    # Рендерим шаблон product_detail.html с контекстом
    return render(request, 'product_detail.html', context)
