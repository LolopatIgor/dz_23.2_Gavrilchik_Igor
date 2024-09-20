from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'body', 'image', 'is_published')
    success_url = reverse_lazy('blog:list')


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.view_count += 1
        blog.save()
        return super().get(request, *args, **kwargs)


class BlogEditView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'image', 'is_published')

    def get_success_url(self):
        # Получаем slug редактируемой статьи
        return reverse_lazy('blog:view', kwargs={'slug': self.object.slug})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
