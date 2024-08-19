from django.core.exceptions import ValidationError
from django.test import TestCase
from theatre.models import (
    TheatreHall,
    Genre,
    Actor,
    Play,
    Performance,
    Reservation,
    Ticket,
)
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class TheatreHallModelTest(TestCase):
    def test_create_theatre_hall(self):
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.assertEqual(hall.name, "Main Hall")
        self.assertEqual(hall.capacity, 200)

    def test_theatre_hall_str(self):
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        self.assertEqual(str(hall), "Main Hall")


class GenreModelTest(TestCase):
    def test_create_genre(self):
        genre = Genre.objects.create(name="Comedy")
        self.assertEqual(genre.name, "Comedy")

    def test_genre_str(self):
        genre = Genre.objects.create(name="Comedy")
        self.assertEqual(str(genre), "Comedy")


class ActorModelTest(TestCase):
    def test_create_actor(self):
        actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(actor.first_name, "John")
        self.assertEqual(actor.last_name, "Doe")
        self.assertEqual(actor.full_name, "John Doe")

    def test_actor_str(self):
        actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(str(actor), "John Doe")


class PlayModelTest(TestCase):
    def test_create_play(self):
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        self.assertEqual(play.title, "Hamlet")
        self.assertEqual(play.description, "A Shakespeare play")

    def test_play_str(self):
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        self.assertEqual(str(play), "Hamlet")


class PerformanceModelTest(TestCase):
    def test_create_performance(self):
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        performance = Performance.objects.create(
            show_time="2024-08-01 19:00:00", play=play, theatre_hall=hall
        )
        self.assertEqual(performance.play, play)
        self.assertEqual(performance.theatre_hall, hall)
        self.assertEqual(str(performance), "Hamlet 2024-08-01 19:00:00")


class ReservationModelTest(TestCase):
    def test_create_reservation(self):
        user = User.objects.create_user(email="testuser@test.com", password="testpass")
        reservation = Reservation.objects.create(user=user)
        self.assertEqual(reservation.user, user)
        self.assertIsNotNone(reservation.created_at)

    def test_reservation_str(self):
        user = User.objects.create_user(email="testuser@test.com", password="testpass")
        reservation = Reservation.objects.create(user=user)
        self.assertEqual(str(reservation), str(reservation.created_at))


class TicketModelTest(TestCase):
    def test_create_ticket(self):
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        performance = Performance.objects.create(
            show_time="2024-08-01 19:00:00", play=play, theatre_hall=hall
        )
        user = User.objects.create_user(email="testuser@test.com", password="testpass")
        reservation = Reservation.objects.create(user=user)
        ticket = Ticket.objects.create(
            row=5, seat=10, performance=performance, reservation=reservation
        )
        self.assertEqual(ticket.row, 5)
        self.assertEqual(ticket.seat, 10)
        self.assertEqual(ticket.performance, performance)
        self.assertEqual(ticket.reservation, reservation)

    def test_ticket_str(self):
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        performance = Performance.objects.create(
            show_time="2024-08-01 19:00:00", play=play, theatre_hall=hall
        )
        user = User.objects.create_user(email="testuser@test.com", password="testpass")
        reservation = Reservation.objects.create(user=user)
        ticket = Ticket.objects.create(
            row=5, seat=10, performance=performance, reservation=reservation
        )
        expected_str = "Hamlet 2024-08-01 19:00:00 (row: 5, seat: 10)"
        self.assertEqual(str(ticket), expected_str)

    def test_ticket_validation(self):
        play = Play.objects.create(title="Hamlet", description="A Shakespeare play")
        hall = TheatreHall.objects.create(name="Main Hall", rows=10, seats_in_row=20)
        performance = Performance.objects.create(
            show_time="2024-08-01 19:00:00", play=play, theatre_hall=hall
        )
        user = User.objects.create_user(email="testuser@test.com", password="testpass")
        reservation = Reservation.objects.create(user=user)
        ticket = Ticket(
            row=15, seat=10, performance=performance, reservation=reservation
        )

        with self.assertRaises(ValidationError):
            ticket.full_clean()
