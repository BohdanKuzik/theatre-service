from django.test import TestCase
from theatre.models import (
    Genre,
    Actor,
    TheatreHall,
    Play,
    Performance,
)
from theatre.serializers import (
    GenreSerializer,
    ActorSerializer,
    TheatreHallSerializer,
    PlaySerializer,
    TicketSerializer,
)


class GenreSerializerTest(TestCase):
    def test_genre_serializer(self):
        genre = Genre.objects.create(name="Comedy")
        serializer = GenreSerializer(genre)
        self.assertEqual(serializer.data, {"id": genre.id, "name": "Comedy"})


class ActorSerializerTest(TestCase):
    def test_actor_serializer(self):
        actor = Actor.objects.create(first_name="John", last_name="Doe")
        serializer = ActorSerializer(actor)
        self.assertEqual(
            serializer.data,
            {
                "id": actor.id,
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
            },
        )


class TheatreHallSerializerTest(TestCase):
    def test_theatre_hall_serializer(self):
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        serializer = TheatreHallSerializer(hall)
        self.assertEqual(
            serializer.data,
            {
                "id": hall.id,
                "name": "Main Hall",
                "rows": 10,
                "seats_in_row": 20,
                "capacity": 200,
            },
        )


class PlaySerializerTest(TestCase):
    def test_play_serializer(self):
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        serializer = PlaySerializer(play)
        self.assertEqual(
            serializer.data,
            {"id": play.id, "title": "Hamlet", "description": "A Shakespeare play"},
        )


class TicketSerializerTest(TestCase):
    def test_ticket_serializer_valid(self):
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        performance = Performance.objects.create(
            show_time="2024-08-01 19:00:00", play=play, theatre_hall=hall
        )
        ticket_data = {
            "row": 5,
            "seat": 10,
            "performance": performance.id,
        }
        serializer = TicketSerializer(data=ticket_data)

        if not serializer.is_valid():
            print(serializer.errors)

        self.assertTrue(serializer.is_valid())

    def test_ticket_serializer_invalid(self):
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        performance = Performance.objects.create(
            show_time="2024-08-01 19:00:00", play=play, theatre_hall=hall
        )

        ticket_data = {"row": 15, "seat": 10, "performance": performance.id}

        serializer = TicketSerializer(data=ticket_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("row", serializer.errors)
        self.assertEqual(serializer.errors["row"][0].code, "invalid")
