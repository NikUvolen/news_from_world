from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages

from .models import News, Category
from .forms import NewsForm, UserRegistrationForm, UserLoginForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered')
            return redirect('login')
        else:
            messages.error(request, 'Registration error')
    else:
        form = UserRegistrationForm()

    context = {'title': 'Registration', 'form': form}
    return render(request, 'news/register.html', context=context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    context = {'title': 'Login', 'form': form}
    return render(request, 'news/login.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('login')


class BaseListView(ListView):
    paginate_by = 4
    context_object_name = 'news'


class HomeNews(BaseListView):
    model = News
    template_name = 'news/index.html'
    extra_context = {'title': 'Home'}

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

    class Meta:
        pass


class NewsByCategory(BaseListView):
    model = News
    template_name = 'news/category.html'

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'


# def index(request):
#     # print(request)
#     news = News.objects.order_by('-created_at')
#     context = {
#         'news': news,
#         'title': 'News list',
#     }
#     return render(request, 'news/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = get_object_or_404(Category, pk=category_id)
#     context = {
#         'news': news,
#         'category': category
#     }
#     return render(request, template_name='news/category.html', context=context)


# def view_news(request, news_id):
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         'news_item': news_item
#     }
#     return render(request, 'news/view_news.html', context=context)


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = News.objects.create(**form.cleaned_data)
#             return redirect(news)
#     else:
#         form = NewsForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'news/add_news.html', context=context)
