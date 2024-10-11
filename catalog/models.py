from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.CharField(max_length=800, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.CharField(max_length=800, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')
    manufactured_at = models.DateTimeField(verbose_name='Дата производства продукта', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        permissions = [
            ("can_edit_is_published", "Can edit publishing"),
            ("can_edit_description", "Can edit description"),
            ("can_edit_category", "Can edit category")
        ]


class BanWords(models.Model):
    name = models.CharField(max_length=200, verbose_name='Слово')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Запрещенное слово'
        verbose_name_plural = 'Запрещенные слова'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='versions')
    number = models.DecimalField(max_digits=10, decimal_places=8, verbose_name='Номер версии')
    name = models.CharField(max_length=200, verbose_name='Название версии')
    is_current = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return f"{self.product.name} - {self.number}"

    class Meta:
        verbose_name = 'Версия продукта'
        verbose_name_plural = 'Версии продуктов'