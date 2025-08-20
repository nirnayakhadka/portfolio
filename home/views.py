from django.shortcuts import render

def index(request):
    """Home page view - Single page portfolio"""
    context = {
        'page_title': 'Portfolio',
    }
    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'home/about.html')