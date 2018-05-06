from django.test import TestCase

from rest_framework.exceptions import NotFound

from apps.api.models import Breed
from apps.api.shortcuts import get_object_or_404


class ShortcutsTests(TestCase):

    def setUp(self):
        Breed.objects.create(name='Abyssinian', slug='abyssinian')

    def test_get_or_404(self):
        breed = get_object_or_404(Breed, slug='abyssinian')
        self.assertIsNotNone(breed)
        with self.assertRaises(NotFound):
            get_object_or_404(Breed, name='unknown breed')
