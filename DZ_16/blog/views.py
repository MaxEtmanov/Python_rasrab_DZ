from pyexpat.errors import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

def home(request):
     return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['id']

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = '/blog/posts/'
    
    def form_invalid(self, form):
        """
        Метод вызывается, когда форма не прошла валидацию.
        Можно добавить дополнительную логику обработки ошибок.
        """
        return super().form_invalid(form)
    
    def form_valid(self, form):
        """
        Метод вызывается, когда форма прошла валидацию.
        Здесь можно добавить дополнительную логику перед сохранением.
        """
        # Пример: если нужно добавить автора поста (если есть поле author)
        # form.instance.author = self.request.user
        
        return super().form_valid(form)   

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'  # Можно использовать тот же шаблон, что и для создания
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
