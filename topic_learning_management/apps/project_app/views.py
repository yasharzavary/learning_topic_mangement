from django.shortcuts import render
from .models import *

def custom_404(request, exception):

    return render(
        request,
        "errors/404.html",
        status=404
    )


def index(request):
    context = {
        'topics': Topic.objects.all(),
        'category': Category.objects.all()
    }

    return render(request, 'topics/index.html', context)

