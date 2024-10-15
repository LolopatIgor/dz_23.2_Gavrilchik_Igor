from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ContactsPageView, CatalogCreateView, CatalogEditView, CategoryListView

app_name = CatalogConfig.name
#test
urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(120)(ProductDetailView.as_view()), name='product_detail'),
    path('create/', CatalogCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', CatalogEditView.as_view(), name='edit'),
    path('categories/', CategoryListView.as_view(), name='list'),
]
