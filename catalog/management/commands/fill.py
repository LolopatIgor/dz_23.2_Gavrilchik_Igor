import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product, BanWords


class Command(BaseCommand):

    @staticmethod
    def json_read_data():
        # Чтение данных из JSON файла
        with open('catalog/data/catalog_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def handle(self, *args, **options):
        # Удалите все продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()
        BanWords.objects.all().delete()

        # Создайте списки для хранения объектов
        categories_for_create = []
        products_for_create = []
        banwords_for_create = []

        # Чтение данных из JSON файла
        data = Command.json_read_data()

        # Обработка данных из JSON файла: сначала категории
        for entry in data:
            model = entry['model']
            fields = entry['fields']

            # Если модель - это категория, добавляем в список для создания
            if model == 'catalog.category':
                categories_for_create.append(
                    Category(
                        pk=entry['pk'],
                        name=fields['name'],
                        description=fields['description']
                    )
                )

        # Создаем категории в базе данных с помощью bulk_create()
        Category.objects.bulk_create(categories_for_create)
        self.stdout.write(self.style.SUCCESS('Категории успешно добавлены.'))

        # Обработка данных из JSON файла: теперь продукты
        for entry in data:
            model = entry['model']
            fields = entry['fields']

            # Если модель - это продукт
            if model == 'catalog.product':
                try:
                    category = Category.objects.get(pk=fields['category'])
                except Category.DoesNotExist:
                    self.stdout.write(self.style.ERROR(
                        f"Категория с ID {fields['category']} не найдена для продукта {fields['name']}."))
                    continue

                products_for_create.append(
                    Product(
                        pk=entry['pk'],
                        name=fields['name'],
                        description=fields['description'],
                        image=fields['image'],
                        price=fields['price'],
                        category=category,
                        created_at=fields['created_at'],
                        updated_at=fields['updated_at'],
                        manufactured_at=fields['manufactured_at']
                    )
                )

        # Создаем продукты в базе данных с помощью bulk_create()
        Product.objects.bulk_create(products_for_create)
        self.stdout.write(self.style.SUCCESS('Продукты успешно добавлены.'))

        for entry in data:
            model = entry['model']
            fields = entry['fields']

            # Если модель - это категория, добавляем в список для создания
            if model == 'catalog.banwords':
                banwords_for_create.append(
                    BanWords(
                        pk=entry['pk'],
                        name=fields['name']
                    )
                )

        # Создаем категории в базе данных с помощью bulk_create()
        BanWords.objects.bulk_create(banwords_for_create)
        self.stdout.write(self.style.SUCCESS('Запрещенные слова успешно добавлены.'))
