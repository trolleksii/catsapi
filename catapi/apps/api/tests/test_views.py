import json

from io import BytesIO
from PIL import Image


from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import TestCase
from django.utils.text import slugify

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
        self.assertEquals(response.data['status'], 'success')
        list_from_response = response.data['message']
        list_from_qset = Breed.objects.all()
        self.assertEquals(len(list_from_response), len(list_from_qset))

    def test_add_new_breed(self):
        breeds_before = len(Breed.objects.all())
        data = {'name': 'British longhair'}
        response = self.client.post(
            reverse('api:list_create_breed'),
            data=json.dumps({'breed': data}),
            content_type='application/json'
        )
        self.assertEquals(response.data['status'], 'success')
        response_data = response.data['message']
        self.assertEqual(slugify(data['name']), response_data['slug'])
        breeds_after = len(Breed.objects.all())
        self.assertEquals(breeds_after, breeds_before + 1)

    def test_add_new_breed_wrong_name(self):
        data = {'name': 'British longhair1'}
        response = self.client.post(
            reverse('api:list_create_breed'),
            data=json.dumps({'breed': data}),
            content_type='application/json'
        )
        self.assertEquals(response.data['status'], 'error')


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
        self.assertEquals(response.data['status'], 'success')
        self.assertEqual(cats_count, response_cats_count)

    def test_post_new_cat(self):
        cats_count = len(Cat.objects.filter(breed__slug=self.breed.slug))
        stream = BytesIO()
        Image.new('RGB', (500, 500)).save(stream, 'JPEG')
        stream.seek(0)
        upload_file = SimpleUploadedFile('image.jpeg', stream.read(), content_type='image/jpeg')
        response = self.client.post(
            reverse('api:list_create_cat', kwargs={'breed_slug': self.breed.slug}),
            data={'file': upload_file}
        )
        self.assertEquals(response.data['status'], 'success')
        final_cats_count = len(Cat.objects.filter(breed__slug=self.breed.slug))
        self.assertEquals(final_cats_count, cats_count + 1)

    def test_post_new_cat_large_file(self):
        stream = BytesIO()
        Image.new('RGB', (10000, 10000)).save(stream, 'JPEG')
        stream.seek(0)
        upload_file = SimpleUploadedFile('image.jpeg', stream.read(), content_type='image/jpeg')
        response = self.client.post(
            reverse('api:list_create_cat', kwargs={'breed_slug': self.breed.slug}),
            data={'file': upload_file}
        )
        self.assertEquals(response.data['status'], 'error')


class RandomCatAPIViewTests(CatTests):

    def test_get_random_cat_of_breed(self):
        response = self.client.get(
            reverse('api:get_random_cat', kwargs={'breed_slug': self.breed.slug}),
            content_type='application/json'
        )
        self.assertIn(self.breed.slug, response.data['message'])
        self.assertEquals(response.data['status'], 'success')

    def test_get_random_wrong_breed(self):
        response = self.client.get(
            reverse('api:get_random_cat', kwargs={'breed_slug': 'wrong-breed'}),
            content_type='application/json'
        )
        self.assertEquals(response.data['status'], 'error')