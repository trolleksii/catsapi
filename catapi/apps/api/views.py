from random import randint

from django.db.models import Count

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Breed
from .serializers import BreedSerializer, CatSerializer
from .shortcuts import get_object_or_404


class BreedAPIView(APIView):
    permission_classes = AllowAny,
    serializer_class = BreedSerializer

    def get(self, request):
        qset = Breed.objects.all()
        serializer = self.serializer_class(qset, many=True)
        return Response(
            {
                'status': 'success',
                'message': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        data = request.data.get('breed', None)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'status': 'success',
                'message': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class CatAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = AllowAny,
    serializer_class = CatSerializer

    def get(self, request, breed_slug):
        breed = get_object_or_404(Breed, slug=breed_slug)
        qset = breed.cats.all()
        serializer = self.serializer_class(qset, many=True)
        return Response(
            {
                'status': 'success',
                'message': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, breed_slug):
        img_file = request.data.get('file', '')
        print(img_file)
        breed = get_object_or_404(Breed, slug=breed_slug)
        serializer = self.serializer_class(
            data={
                'breed': breed.pk,
                'image': img_file
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'status': 'success',
                'message': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class RandomCatAPIView(APIView):
    permission_classes = AllowAny,
    serializer_class = CatSerializer

    def get(self, request, breed_slug):
        breed = get_object_or_404(Breed, slug=breed_slug)
        cats_count = breed.cats.aggregate(count=Count('pk'))['count']
        data = {
            'status': 'success',
            'message': None
        }
        if cats_count:
            pos = randint(0, cats_count - 1)
            random_cat = breed.cats.filter()[pos]
            serializer = self.serializer_class(random_cat)
            data['message'] = serializer.data
        return Response(data, status=status.HTTP_200_OK)
