from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages

def custom_404(request, exception):

    return render(
        request,
        "errors/404.html",
        status=404
    )


def index(request):
    context = {
        'topics': Topic.objects.all(),
        'categories': Category.objects.all()
    }

    return render(request, 'topics/index.html', context)





def create_topic(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        category_id = request.POST.get("category")
        priority = request.POST.get("priority", "MEDIUM")
        learning_goal = request.POST.get("learning_goal", "").strip()
        origin_reason = request.POST.get("origin_reason", "").strip()
        origin_file = request.FILES.get("origin_file")

        if not title:
            
            messages.error(request, "Topic title is required.")
            return render(
                request,
                "create.html",
                {"categories": categories},
            )

        category = get_object_or_404(Category, id=category_id)

        topic = Topic.objects.create(
            title=title,
            description=description,
            category=category,
            priority=priority,
            learning_goal=learning_goal,
            origin_reason=origin_reason,
            origin_file=origin_file,
        )

        messages.success(request, "Topic created successfully.")

        return redirect("index")

    context = {
        "categories": categories,
    }

    return render(request, "topics/create.html", context)
