import re

from django.utils.text import slugify

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from catapi.settings import MEDIA_URL

from .models import Breed, Cat


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = ('name', 'slug')
        read_only_fields = 'slug',

    def validate(self, attrs):
        name = attrs.get('name', '')
        # check for non alphabet symbols or spaces and bring to uniform look
        has_bad_symbols = re.search(r'[^\-a-zA-Z\s]', name)
        if has_bad_symbols:
            msg = 'Name should be only of alphabet symbols and spaces'
            raise ValidationError(msg)
        name = ' '.join([x.capitalize() for x in name.split()])
        # native DRF validators do not take into account multiple spaces etc
        if Breed.objects.filter(name=name).exists():
            msg = 'This breed is already in the db'
            raise ValidationError(msg)
        return {
            'name': name,
            'slug': slugify(name)
        }


class CatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cat
        fields = ('image', 'breed')
        extra_kwargs = {
            'breed': {'write_only': True}
        }

    @property
    def data(self):
        return super(serializers.Serializer, self).data

    def to_representation(self, obj):
        return MEDIA_URL + obj.image.name

    def create(self, validated_data):
        return Cat.objects.create(**validated_data)
