from random import randint

from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import PayloadTooLarge
from .models import Cat, Breed
from .serializers import BreedSerializer, CatSerializer


class BreedAPIView(APIView):
    permission_classes = AllowAny,
    serializer_class = BreedSerializer

    def get(self, request):
        qset = Breed.objects.all()
        serializer = self.serializer_class(qset, many=True)
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)


class CatAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = AllowAny,
    serializer_class = CatSerializer
    # size in Bytes
    MAX_FILE_SIZE = 509600

    def get(self, request, breed_slug):
        breed = get_object_or_404(Breed, slug=breed_slug)
        qset = breed.cats.all()
        serializer = self.serializer_class(qset, many=True)
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, breed_slug):
        breed = get_object_or_404(Breed, slug=breed_slug)
        ulpoad_files = request.data.getlist('files')
        data = [{'breed': breed.pk, 'image': img} for img in ulpoad_files if self._file_size_is_ok(img)] or [{}]
        many = True
        if len(data) == 1:
                data = data.pop()
                many = False
        serializer = self.serializer_class(
            data=data,
            many=many
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)

    def _file_size_is_ok(self, img_file):
        if img_file.size >= self.MAX_FILE_SIZE:
            msg = 'File size should be less than {}KB'.format(self.MAX_FILE_SIZE // 1024)
            raise PayloadTooLarge(msg)
        return True


class RandomCatAPIView(APIView):
    permission_classes = AllowAny,
    serializer_class = CatSerializer

    def get_queryset(self, slug):
        if slug:
            breed = get_object_or_404(Breed, slug=slug)
            return breed.cats
        return Cat.objects.all()

    def get(self, request, breed_slug=None):
        qset = self.get_queryset(breed_slug)
        cats_count = qset.aggregate(count=Count('pk'))['count']
        data = {'message': None}
        if cats_count:
            pos = randint(0, cats_count - 1)
            random_cat = qset.filter()[pos]
            serializer = self.serializer_class(random_cat)
            data['message'] = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class AllCatsAPIView(APIView):
    permission_classes = AllowAny,
    serializer_class = CatSerializer

    def get(self, request):
        qset = Cat.objects.all()
        serializer = self.serializer_class(qset, many=True)
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)
