from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


# categories
class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(max_length=150)

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# topic details

class Topic(models.Model):

    class Status(models.TextChoices):
        IDEA = "IDEA", "Idea"
        SOURCE_RESEARCH = "SOURCE_RESEARCH", "Source Research"
        LEARNING = "LEARNING", "Learning"
        EXPERIENCE = "EXPERIENCE", "Experience"
        COMPLETED = "COMPLETED", "Completed"


    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"


    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="topics"
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    learning_goal = models.TextField(
        blank=True,
        null=True
    )

    origin_reason = models.TextField(
        blank=True,
        null=True
    )

    # File/image/book/article that caused the question
    origin_file = models.FileField(
        upload_to="media/files/reason",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.IDEA
    )


    def __str__(self):
        return self.title



# topic timeline control

class TopicTimeline(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    topic = models.OneToOneField(
        Topic,
        on_delete=models.CASCADE,
        related_name="timeline"
    )


    topic_created = models.DateTimeField(
        null=True,
        blank=True
    )


    source_research_start = models.DateTimeField(
        null=True,
        blank=True
    )

    source_research_finish = models.DateTimeField(
        null=True,
        blank=True
    )


    learning_start = models.DateTimeField(
        null=True,
        blank=True
    )

    learning_finish = models.DateTimeField(
        null=True,
        blank=True
    )


    experience_start = models.DateTimeField(
        null=True,
        blank=True
    )

    experience_finish = models.DateTimeField(
        null=True,
        blank=True
    )


    topic_finish = models.DateTimeField(
        null=True,
        blank=True
    )


    def __str__(self):
        return f"Timeline - {self.topic.title}"



# topic source

class TopicSource(models.Model):

    class SourceType(models.TextChoices):
        BOOK = "BOOK", "Book"
        PAPER = "PAPER", "Paper"
        VIDEO = "VIDEO", "Video"
        COURSE = "COURSE", "Course"
        ARTICLE = "ARTICLE", "Article"
        DOCUMENTATION = "DOCUMENTATION", "Documentation"
        OTHER = "OTHER", "Other"



    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )


    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="sources"
    )


    title = models.CharField(
        max_length=255
    )

    url = models.URLField(
        blank=True,
        null=True
    )

    source_file = models.FileField(
        upload_to="media/files/sources/",
        blank=True,
        null=True
    )


    source_type = models.CharField(
        max_length=30,
        choices=SourceType.choices
    )


    author = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


    notes = models.TextField(
        blank=True,
        null=True
    )


    # Evaluation after learning(null first)

    quality_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    explanation_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    difficulty_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    usefulness_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    would_use_again_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )


    def __str__(self):
        return self.title



# topic experience

class TopicExperience(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    topic = models.OneToOneField(
        Topic,
        on_delete=models.CASCADE,
        related_name="experience"
    )

    difficulty_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ]
    )

    usefulness_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ]
    )

    interest_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ]
    )

    knowledge_before_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ]
    )

    knowledge_after_score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ]
    )

    best_learning_method = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    final_summary = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Experience - {self.topic.title}"


# topic releation

class TopicRelation(models.Model):

    class RelationType(models.TextChoices):
        RELATED = "RELATED", "Related"
        PREREQUISITE = "PREREQUISITE", "Prerequisite"
        NEXT_STEP = "NEXT_STEP", "Next Step"
        PART_OF = "PART_OF", "Part Of"


    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )


    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="relations"
    )


    related_topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="related_from"
    )


    relation_type = models.CharField(
        max_length=30,
        choices=RelationType.choices
    )


    def __str__(self):
        return f"{self.topic} -> {self.related_topic}"
    