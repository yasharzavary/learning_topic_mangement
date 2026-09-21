from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        category_id = request.POST.get(
            "category"
        )

        priority = request.POST.get(
            "priority",
            "MEDIUM"
        )

        learning_goal = request.POST.get(
            "learning_goal",
            ""
        ).strip()

        origin_reason = request.POST.get(
            "origin_reason",
            ""
        ).strip()

        origin_file = request.FILES.get(
            "origin_file"
        )

        if not title:
            messages.error(
                request,
                "Topic title is required."
            )
            return render(
                request,
                "topics/create.html",
                {
                    "categories": categories
                },
            )

        category = get_object_or_404(
            Category,
            id=category_id
        )

        # Create Topic
        topic = Topic.objects.create(
            title=title,
            description=description,
            category=category,
            priority=priority,
            learning_goal=learning_goal,
            origin_reason=origin_reason,
            origin_file=origin_file,
            status="IDEA"
        )

        # Create Topic Timeline
        TopicTimeline.objects.create(
            topic=topic,
            topic_created=timezone.now()
        )
        messages.success(
            request,
            "Topic created successfully."
        )

        return redirect(
            "index"
        )

    context = {
        "categories": categories,
    }

    return render(
        request,
        "topics/create.html",
        context
    )

@login_required
def topic_detail(request, topic_id):


    topic = get_object_or_404(
        Topic,
        id=topic_id
    )
    timeline = get_object_or_404(
        TopicTimeline,
        topic=topic
    )

    context = {
        "topic": topic,
        "timeline": timeline
    }

    return render(
        request,
        "topics/detail.html",
        context
    )


@login_required
def start_research(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id
    )

    timeline = topic.timeline

    if topic.status == "IDEA":
        topic.status = "SOURCE_RESEARCH"
        topic.save()
        timeline.source_research_start = (
            timezone.now()
        )

        timeline.save()

    return redirect(
        "topic_detail",
        topic_id=topic.id
    )

@login_required
def finish_research(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id
    )
    timeline = topic.timeline
    if topic.status == "SOURCE_RESEARCH":
        timeline.source_research_finish = (
            timezone.now()
        )
        timeline.save()

    return redirect(
        "topic_detail",
        topic_id=topic.id
    )

@login_required
def start_learning(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id
    )
    timeline = topic.timeline

    if (
        topic.status == "SOURCE_RESEARCH"
        and
        timeline.source_research_finish
    ):
        topic.status = "LEARNING"
        topic.save()
        timeline.learning_start = (
            timezone.now()
        )
        timeline.save()

    return redirect(
        "topic_detail",
        topic_id=topic.id
    )

@login_required
def finish_learning(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id
    )
    timeline = topic.timeline

    if topic.status == "LEARNING":
        timeline.learning_finish = (
            timezone.now()
        )
        timeline.save()

    return redirect(
        "topic_detail",
        topic_id=topic.id
    )

@login_required
def start_experience(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id
    )
    timeline = topic.timeline

    if (
        topic.status == "LEARNING"
        and
        timeline.learning_finish
    ):
        topic.status = "EXPERIENCE"
        topic.save()

        timeline.experience_start = (
            timezone.now()
        )
        timeline.save()

    return redirect(
        "topic_detail",
        topic_id=topic.id
    )

@login_required
def finish_experience(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id
    )

    timeline = topic.timeline
    if topic.status == "EXPERIENCE":

        timeline.experience_finish = (
            timezone.now()
        )
        timeline.save()

    return redirect(
        "topic_detail",
        topic_id=topic.id
    )


@login_required
def complete_topic(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id
    )
    timeline = topic.timeline

    if (
        topic.status == "EXPERIENCE"
        and
        timeline.experience_finish
    ):

        topic.status = "COMPLETED"
        topic.save()
        timeline.topic_finish = (
            timezone.now()
        )
        timeline.save()

    return redirect(
        "topic_detail",
        topic_id=topic.id
    )

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id
    )

    if request.method == "POST":
        topic.delete()

    return redirect(
        "index"
    )