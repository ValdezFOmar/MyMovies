import random

from django.utils import timezone
from faker import Faker
from movies.models import Movie, User


def create_users():
    fake = Faker()

    for _ in range(30):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = first_name.lower() + last_name.lower()
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=f'{username}@example.com',
            password='1234',
        )
        user.save()


def random_score() -> int:
    # return random.randint(0, 100)
    # Technically the range is [0, 100] but this range give movies
    # an extremely low score
    return random.randint(30, 100)


def randrange(start: float, end: float) -> float:
    return start + random.random() * (end - start)


def create_data():
    fake = Faker()
    movies = tuple(Movie.objects.all())
    users = (u for u in User.objects.all() if u.username != 'admin')

    for user in users:
        percent = randrange(0.15, 0.70)
        k = int(len(movies) * percent)
        selected_movies = random.sample(movies, k)

        for movie in selected_movies:
            moviereview = movie.moviereview_set.create(
                user=user,
                rating=random_score(),
                review=fake.text(),
                date_time=timezone.now(),
            )
            moviereview.save()


def main():
    for user in User.objects.all():
        print(user.username)


if __name__ == '__main__':
    main()
