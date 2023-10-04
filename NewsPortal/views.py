from django.shortcuts import (render, redirect)
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from .models import Post, BaseRegisterForm
from .filters import PostFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import (User,Group)
from django.contrib.auth.decorators import login_required


class NewsList(ListView):
    #model = Post
    #ordering = 'dtime_p'
    queryset = Post.objects.filter().order_by('dtime_p').values('title', 'dtime_p', 'text_p')
    template_name = 'news.html'
    context_object_name = 'list'
    paginate_by = 5

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CreateNews(LoginRequiredMixin, CreateView):
    permission_required = 'NewsPortal.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    login_url = "/login/"

    def form_valid(self, form):
        news = form.save(commit=False)
        news.choice = 'N'
        return super().form_valid(form)

class CreatePost(LoginRequiredMixin, CreateView):
    permission_required = 'NewsPortal.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'
    login_url = "/login/"

    def form_valid(self, form):
        news = form.save(commit=False)
        news.choice = 'A'
        return super().form_valid(form)

class NewsUpdate(LoginRequiredMixin, UpdateView):
    permission_required = 'NewsPortal.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = 'NewsPortal.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'post_edit.html'

class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('list')

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'userprofil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')