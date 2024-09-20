from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogEditView, BlogDeleteView

app_name = BlogConfig.name
#test
urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),
    path('view/<slug:slug>/', BlogDetailView.as_view(), name='view'),
    path('edit/<slug:slug>/', BlogEditView.as_view(), name='edit'),
    path('delete/<slug:slug>/', BlogDeleteView.as_view(), name='delete'),
]
