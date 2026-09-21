from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('create/', create_topic, name='create_topic'),

    # Topic detail page
    path(
        "<uuid:topic_id>/",
        topic_detail,
        name="topic_detail"
    ),

    # Lifecycle actions
    path(
        "<uuid:topic_id>/start-research/",
        start_research,
        name="start_research"
    ),
    path(
        "<uuid:topic_id>/finish-research/",
        finish_research,
        name="finish_research"
    ),
    path(
        "<uuid:topic_id>/start-learning/",
        start_learning,
        name="start_learning"
    ),
    path(
        "<uuid:topic_id>/finish-learning/",
        finish_learning,
        name="finish_learning"
    ),
    path(
        "<uuid:topic_id>/start-experience/",
        start_experience,
        name="start_experience"
    ),
    path(
        "<uuid:topic_id>/finish-experience/",
        finish_experience,
        name="finish_experience"
    ),
    path(
        "<uuid:topic_id>/complete/",
        complete_topic,
        name="complete_topic"
    ),
    # Delete
    path(
        "<uuid:topic_id>/delete/",
        delete_topic,
        name="delete_topic"
    ),
]
