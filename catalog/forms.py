from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product, BanWords, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Проверяем, является ли поле чекбоксом (BooleanField)
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


def get_forbidden_words():
    return BanWords.objects.values_list('name', flat=True)


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')


class ProductManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        forbidden_words = get_forbidden_words()
        if any(word.lower() in name.lower() for word in forbidden_words):
            raise ValidationError('Название содержит запрещённые слова.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        forbidden_words = get_forbidden_words()
        if any(word.lower() in description.lower() for word in forbidden_words):
            raise ValidationError('Описание содержит запрещённые слова.')
        return description


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
