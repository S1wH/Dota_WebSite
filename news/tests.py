from django.test import TestCase
from .models import Author


class TestAuthor(TestCase):

    def test_str(self):
        author = Author.objects.create(nickname='Pishkin', rating=1)
        self.assertEqual(str(author), 'Pishkin with rating 1')
