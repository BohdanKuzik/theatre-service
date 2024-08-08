from theatre.models import (
    Play,
)

from celery import shared_task


@shared_task
def count_plays():
    return Play.objects.count()

