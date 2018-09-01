import json

from io import BytesIO
from PIL import Image


from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import TestCase
from django.utils.text import slugify

from rest_framework import status

from apps.api.models import Breed, Cat


class BreedAPIViewTests(TestCase):

    def setUp(self):
        self.breed = Breed.objects.create(
            name='British Shorthair',
            slug='british-shorthair'
        )

    def test_get_breeds_list(self):
        response = self.client.get(
            reverse('api:list_create_breed'),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        list_from_response = response.data['message']
        list_from_qset = Breed.objects.all()
        self.assertEquals(len(list_from_response), len(list_from_qset))

    def test_add_new_breed(self):
        breeds_before = len(Breed.objects.all())
        data = {'name': 'British longhair'}
        response = self.client.post(
            reverse('api:list_create_breed'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data['message']
        self.assertEqual(slugify(data['name']), response_data['slug'])
        breeds_after = len(Breed.objects.all())
        self.assertEquals(breeds_after, breeds_before + 1)

    def test_add_new_breed_wrong_name(self):
        data = {'name': 'British longhair1'}
        response = self.client.post(
            reverse('api:list_create_breed'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


class CatTests(TestCase):

    def setUp(self):
        self.breed = Breed.objects.create(
            name='British Shorthair',
            slug='british-shorthair'
        )
        file_obj = BytesIO()
        Image.new('RGB', (500, 500)).save(file_obj, 'PNG')
        file_obj.seek(0)
        image_file = SimpleUploadedFile('test.png', file_obj.read(), content_type="image/png")
        Cat.objects.create(breed=self.breed, image=image_file)
        Cat.objects.create(breed=self.breed, image=image_file)
        Cat.objects.create(breed=self.breed, image=image_file)


class CatAPIViewTests(CatTests):

    def test_get_all_cats_of_breed(self):
        cats_count = len(Cat.objects.filter(breed__slug=self.breed.slug))
        response = self.client.get(
            reverse('api:list_create_cat', kwargs={'breed_slug': self.breed.slug}),
            content_type='application/json'
        )
        response_cats_count = len(response.data['message'])
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cats_count, response_cats_count)

    def test_post_new_cat(self):
        cats_count = len(Cat.objects.filter(breed__slug=self.breed.slug))
        stream = BytesIO()
        Image.new('RGB', (500, 500)).save(stream, 'JPEG')
        stream.seek(0)
        upload_file = SimpleUploadedFile('image.jpeg', stream.read(), content_type='image/jpeg')
        response = self.client.post(
            reverse('api:list_create_cat', kwargs={'breed_slug': self.breed.slug}),
            data={'files': upload_file}
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        final_cats_count = len(Cat.objects.filter(breed__slug=self.breed.slug))
        self.assertEquals(final_cats_count, cats_count + 1)

    def test_post_multiple_cats(self):
        cats_count = len(Cat.objects.filter(breed__slug=self.breed.slug))
        imgs_num = 2
        stream = BytesIO()
        Image.new('RGB', (500, 500)).save(stream, 'JPEG')
        stream.seek(0)
        upload_file1 = SimpleUploadedFile('image.jpeg', stream.read(), content_type='image/jpeg')
        stream.seek(0)
        upload_file2 = SimpleUploadedFile('image.jpeg', stream.read(), content_type='image/jpeg')
        response = self.client.post(
            reverse('api:list_create_cat', kwargs={'breed_slug': self.breed.slug}),
            data={'files': [upload_file1, upload_file2]}
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        final_cats_count = len(Cat.objects.filter(breed__slug=self.breed.slug))
        self.assertEquals(final_cats_count, cats_count + imgs_num)

    def test_post_new_cat_large_file(self):
        stream = BytesIO()
        Image.new('RGB', (10000, 10000)).save(stream, 'JPEG')
        stream.seek(0)
        upload_file = SimpleUploadedFile('image.jpeg', stream.read(), content_type='image/jpeg')
        response = self.client.post(
            reverse('api:list_create_cat', kwargs={'breed_slug': self.breed.slug}),
            data={'files': upload_file}
        )
        self.assertEquals(response.status_code, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)


class RandomCatAPIViewTests(CatTests):

    def test_get_random_of_all(self):
        response = self.client.get(
            reverse('api:get_random'),
            content_type='application/json'
        )
        self.assertIn(self.breed.slug, response.data['message'])
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_random_cat_of_breed(self):
        response = self.client.get(
            reverse('api:get_random_of_breed', kwargs={'breed_slug': self.breed.slug}),
            content_type='application/json'
        )
        self.assertIn(self.breed.slug, response.data['message'])
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_random_wrong_breed(self):
        response = self.client.get(
            reverse('api:get_random_of_breed', kwargs={'breed_slug': 'wrong-breed'}),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class AllCatsAPIView(CatTests):

    def test_list_all_cats(self):
        cats_number = Cat.objects.count()
        response = self.client.get(
            reverse('api:list_all_cats'),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cats_number, len(response.data['message']))
