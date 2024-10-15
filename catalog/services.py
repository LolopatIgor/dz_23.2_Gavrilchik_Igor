from django.core.cache import cache
from catalog.models import Category

def get_cached_categories():
    # Попытка получения данных из кеша
    categories = cache.get('categories_list')

    if categories is None:
        # Если данных нет в кеше, делаем запрос к базе данных
        categories = Category.objects.all()
        cache.set('categories_list', categories, 600)

    return categories