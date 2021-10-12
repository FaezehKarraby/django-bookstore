from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    book = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    LOVER, FANTASTY, SCIENCE_FICTION, ADVENTURE, PANIC, HISTORICAL = 1, 2, 3, 4, 5, 6
    choice_genre = (
        (LOVER, 'Lover'),
        (FANTASTY, 'Fantasy'),
        (SCIENCE_FICTION, 'Science Fiction'),
        (ADVENTURE, 'Adventure'),
        (PANIC, 'Panic'),
        (HISTORICAL, 'Historical')
    )
    genre = models.IntegerField(choices=choice_genre)
    price = models.IntegerField(default=0)
    count_book = models.IntegerField(default=0)
    image = models.ImageField(upload_to='books', default='book.jpeg')

    def __str__(self):
        return self.book


class Buy(models.Model):
    """
        Generate unique tokens for each purchase
    """
    token = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    book = models.ForeignKey(Book, models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
