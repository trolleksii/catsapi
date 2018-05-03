from uuid import uuid4

from django.db import models


class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Cat(models.Model):

    def get_file_path(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = '{}.{}'.format(uuid4(), extension)
        #TODO : path to production static folder
        return 'static/{}/{}'.format(instance.breed.slug, unique_filename)

    breed = models.ForeignKey(Breed, related_name='cats', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_file_path)

    def __str__(self):
        return '{}-{}'.format(self.breed.name, self.pk)
