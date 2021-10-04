from django import template
from django.db.models import Count, F

from news.models import Category

register = template.Library()


# @register.simple_tag(name='get_list_categories')
# def get_categories():
#     return Category.objects.all()


@register.inclusion_tag('inc/_list_categories.html')
def show_categories():
    # categories = Category.objects.all()
    categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {'categories': categories}


@register.simple_tag
def is_disabled_url(request):
    if not request.user.is_authenticated:
        return 'disabled'
    return ''


@register.simple_tag
def is_active_url(request, correct_url):
    if request.get_full_path() == correct_url:
        return 'active'
    return ''
