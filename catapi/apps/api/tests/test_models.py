from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.api.models import Breed, Cat


class BreedModelTests(TestCase):

    def test_str_method(self):
        data = {
            'name': 'British Shorthair',
            'slug': 'british-shorthair'
        }
        breed = Breed.objects.create(**data)
        self.assertEquals(str(breed), data['name'])


class CatModelTests(TestCase):

    def setUp(self):
        self.breed = Breed.objects.create(
            name='British Shorthair',
            slug='british-shorthair'
        )

    def test_str_method(self):
        img = Image.new('RGB', (500, 500))
        file_obj = BytesIO()
        img.save(file_obj, 'PNG')
        file_obj.seek(0)
        image_file = SimpleUploadedFile('test.png', file_obj.read(), content_type="image/png")
        cat = Cat.objects.create(
            breed=self.breed,
            image=image_file
        )
        expected_name = '{}-{}'.format(self.breed.name, cat.pk)
        self.assertEquals(str(cat), expected_name)
