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

    return render(
        request,
        'topics/index.html',
        context
    )



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


    timeline = topic.timeline


    sources = TopicSource.objects.filter(
        topic=topic
    ).order_by("-id")



    learning = None


    if hasattr(topic, "learning"):

        learning = topic.learning

    experience = None


    if hasattr(topic, "experience"):

        experience = topic.experience

    context = {

        "topic": topic,

        "timeline": timeline,

        "sources": sources,

        "learning": learning,

        "experience": experience,

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
def add_source(request, topic_id):

    topic = get_object_or_404(
        Topic,
        id=topic_id
    )

    timeline = topic.timeline


    # Source Research must be active
    if (
        topic.status != "SOURCE_RESEARCH"
        or not timeline.source_research_start
        or timeline.source_research_finish
    ):

        messages.error(
            request,
            "Source research has already been completed and can no longer be modified."
        )

        return redirect(
            "topic_detail",
            topic_id=topic.id
        )


    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()


        if not title:

            messages.error(
                request,
                "Source title is required."
            )

            return redirect(
                "topic_detail",
                topic_id=topic.id
            )


        TopicSource.objects.create(

            topic=topic,

            title=title,

            url=request.POST.get(
                "url",
                ""
            ).strip(),

            source_type=request.POST.get(
                "source_type",
                "OTHER"
            ),

            author=request.POST.get(
                "author",
                ""
            ).strip(),

            notes=request.POST.get(
                "notes",
                ""
            ).strip(),

            source_file=request.FILES.get(
                "source_file"
            ),

            quality_score=None,

            explanation_score=None,

            difficulty_score=None,

            usefulness_score=None,

            would_use_again_score=None,

        )


        messages.success(
            request,
            "Source added successfully."
        )


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


    sources = TopicSource.objects.filter(
        topic=topic
    )


    if (
        topic.status == "SOURCE_RESEARCH"
        and
        not timeline.source_research_finish
        and
        sources.exists()
    ):

        timeline.source_research_finish = timezone.now()

        timeline.save()


        messages.success(
            request,
            "Source research completed successfully."
        )


    elif not sources.exists():

        messages.error(
            request,
            "Please add at least one source before finishing research."
        )


    return redirect(
        "topic_detail",
        topic_id=topic.id
    )

    topic = get_object_or_404(
        Topic,
        id=topic_id
    )


    timeline = topic.timeline



    sources = TopicSource.objects.filter(
        topic=topic
    )



    if (

        topic.status == "SOURCE_RESEARCH"

        and

        sources.exists()

    ):



        timeline.source_research_finish = (
            timezone.now()
        )


        timeline.save()



    else:


        messages.error(
            request,
            "Please add at least one source before finishing research."
        )



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



        timeline.learning_start = timezone.now()

        timeline.save()



        TopicLearning.objects.get_or_create(
            topic=topic
        )



        messages.success(
            request,
            "Learning phase started."
        )



    return redirect(
        "topic_detail",
        topic_id=topic.id
    )


@login_required
def save_learning(request, topic_id):



    topic = get_object_or_404(
        Topic,
        id=topic_id
    )


    timeline = topic.timeline



    if (

        topic.status != "LEARNING"

        or

        timeline.learning_finish

    ):


        messages.error(
            request,
            "Learning phase is completed and cannot be modified."
        )


        return redirect(
            "topic_detail",
            topic_id=topic.id
        )




    if request.method == "POST":


        learning, created = TopicLearning.objects.get_or_create(
            topic=topic
        )



        learning.notes = request.POST.get(
            "notes",
            ""
        ).strip()



        learning.key_findings = request.POST.get(
            "key_findings",
            ""
        ).strip()



        learning.questions = request.POST.get(
            "questions",
            ""
        ).strip()



        learning.save()



        messages.success(
            request,
            "Learning notes saved successfully."
        )



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



    learning_exists = hasattr(
        topic,
        "learning"
    )



    if (

        topic.status == "LEARNING"

        and

        learning_exists

    ):


        timeline.learning_finish = timezone.now()

        timeline.save()



        messages.success(
            request,
            "Learning phase completed successfully."
        )



    else:


        messages.error(
            request,
            "Please save learning information before finishing."
        )



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



        timeline.experience_start = timezone.now()

        timeline.save()



        TopicExperience.objects.get_or_create(
            topic=topic
        )


        messages.success(
            request,
            "Experience phase started."
        )


    return redirect(
        "topic_detail",
        topic_id=topic.id
    )

@login_required
def save_experience(request, topic_id):

    topic = get_object_or_404(
        Topic,
        id=topic_id
    )


    timeline = topic.timeline



    if (

        topic.status != "EXPERIENCE"

        or

        timeline.experience_finish

    ):


        messages.error(
            request,
            "Experience phase is completed and cannot be modified."
        )


        return redirect(
            "topic_detail",
            topic_id=topic.id
        )




    if request.method == "POST":


        experience, created = TopicExperience.objects.get_or_create(
            topic=topic
        )



        experience.difficulty_score = request.POST.get(
            "difficulty_score"
        )


        experience.usefulness_score = request.POST.get(
            "usefulness_score"
        )


        experience.interest_score = request.POST.get(
            "interest_score"
        )


        experience.knowledge_before_score = request.POST.get(
            "knowledge_before_score"
        )


        experience.knowledge_after_score = request.POST.get(
            "knowledge_after_score"
        )


        experience.best_learning_method = request.POST.get(
            "best_learning_method"
        )


        experience.final_summary = request.POST.get(
            "final_summary"
        )


        experience.save()



        messages.success(
            request,
            "Experience evaluation saved."
        )



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



    if (

        topic.status == "EXPERIENCE"

        and

        hasattr(topic, "experience")

    ):


        timeline.experience_finish = timezone.now()

        timeline.save()



        messages.success(
            request,
            "Experience evaluation completed."
        )


    else:


        messages.error(
            request,
            "Please save experience evaluation first."
        )


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