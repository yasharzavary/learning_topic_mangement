from django.urls import path

from .views import *



urlpatterns = [


    # Topic pages

    path(
        '',
        index,
        name='index'
    ),


    path(
        'create/',
        create_topic,
        name='create_topic'
    ),


    path(
        '<uuid:topic_id>/',
        topic_detail,
        name='topic_detail'
    ),





    # Source Research Phase


    path(
        '<uuid:topic_id>/start-research/',
        start_research,
        name='start_research'
    ),


    path(
        '<uuid:topic_id>/add-source/',
        add_source,
        name='add_source'
    ),


    path(
        '<uuid:topic_id>/finish-research/',
        finish_research,
        name='finish_research'
    ),





    # Learning Phase


    path(
        '<uuid:topic_id>/start-learning/',
        start_learning,
        name='start_learning'
    ),


    path(
        '<uuid:topic_id>/finish-learning/',
        finish_learning,
        name='finish_learning'
    ),





    # Experience Phase


    path(
        '<uuid:topic_id>/start-experience/',
        start_experience,
        name='start_experience'
    ),


    path(
        '<uuid:topic_id>/finish-experience/',
        finish_experience,
        name='finish_experience'
    ),





    # Complete Topic


    path(
        '<uuid:topic_id>/complete/',
        complete_topic,
        name='complete_topic'
    ),





    # Delete Topic


    path(
        '<uuid:topic_id>/delete/',
        delete_topic,
        name='delete_topic'
    ),
    path(
        '<uuid:topic_id>/save-learning/',
        save_learning,
        name='save_learning'
    ),

    path(
    '<uuid:topic_id>/save-experience/',
    save_experience,
    name='save_experience'
),

]