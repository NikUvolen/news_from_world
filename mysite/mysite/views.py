from django.shortcuts import render


def page_not_found_view(request, exception):
    context = {
        'title': 'News from world'
    }
    return render(request, '404.html', context=context, status=404)
