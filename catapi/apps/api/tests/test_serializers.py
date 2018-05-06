from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.api.models import Breed, Cat
from apps.api.serializers import BreedSerializer, CatSerializer
from catapi.settings import MEDIA_URL


class BreedSerializerTests(TestCase):

    def setUp(self):
        Breed.objects.create(name='Old Breed', slug='old-breed')
        Breed.objects.create(name='Modern Breed', slug='modern-breed')

    def test_add_breed(self):
        serializer = BreedSerializer(data={'name': 'New Breed'})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEquals(serializer.errors, {})
        _breed, created = Breed.objects.get_or_create(name='New Breed')
        self.assertFalse(created)

    def test_add_breed_improper_name(self):
        serializer = BreedSerializer(data={'name': 'Breed£$1'})
        self.assertFalse(serializer.is_valid())

    def test_add_duplicate_breed(self):
        serializer = BreedSerializer(data={'name': 'Old Breed'})
        self.assertFalse(serializer.is_valid())

    def test_add_same_breed_in_caps(self):
        serializer = BreedSerializer(data={'name': 'MODERN BREED'})
        self.assertFalse(serializer.is_valid())

    def test_list_breeds(self):
        qset = Breed.objects.all()
        serializer = BreedSerializer(qset, many=True)
        expected_cats_count = len(qset)
        cats_count = len(serializer.data)
        self.assertEquals(cats_count, expected_cats_count)


class CatSerializerTests(TestCase):

    def setUp(self):
        self.breed1 = Breed.objects.create(name='Breed1', slug='breed1')
        self.breed2 = Breed.objects.create(name='Breed2', slug='breed2')
        file_obj = BytesIO()
        Image.new('RGB', (500, 500)).save(file_obj, 'PNG')
        file_obj.seek(0)
        image_file = SimpleUploadedFile('test.png', file_obj.read(), content_type="image/png")
        Cat.objects.create(breed=self.breed1, image=image_file)
        Cat.objects.create(breed=self.breed1, image=image_file)
        Cat.objects.create(breed=self.breed2, image=image_file)

    def test_serialize_cat(self):
        cat = Cat.objects.first()
        serializer = CatSerializer(cat)
        self.assertEquals(serializer.data, MEDIA_URL + cat.image.name)

    def test_serialize_list_cats(self):
        qset = Cat.objects.all()
        serializer = CatSerializer(qset, many=True)
        expected_cats_count = len(qset)
        cats_count = len(serializer.data)
        self.assertEquals(cats_count, expected_cats_count)

    def test_deserialize_cat(self):
        cats_before = len(self.breed2.cats.all())
        file_obj = BytesIO()
        Image.new('RGB', (500, 500)).save(file_obj, 'PNG')
        file_obj.seek(0)
        image_file = SimpleUploadedFile('test.png', file_obj.read(), content_type="image/png")
        serializer = CatSerializer(
            data={
                'breed': self.breed2.pk,
                'image': image_file
            }
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        cats_after = len(self.breed2.cats.all())
        self.assertEquals(cats_after, cats_before + 1)