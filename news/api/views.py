from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from news.models import Author, News
from news.api.serializers import (
    AuthorSerializer,
    NewsSerializer,
    AuthorModelSerializer,
    NewsModelSerializer
)


def check_news_object(func):
    def wrapper(*args, **kwargs):
        object_id = kwargs.get("pk", None)
        if object_id:
            try:
                result = func(*args, **kwargs)
                return result
            except ObjectDoesNotExist:
                return Response(
                    {"error": f"No object with id:{object_id} was found"}, status=406
                )
        return Response({"error": "No id was given"}, status=417)

    return wrapper


class ListAuthorsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()

        author_list = [
            {"nickname": author.nickname, "rating": author.rating} for author in authors
        ]
        return Response(author_list)


class ListAuthorsGenericView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer


class ListCreateAuthorsGenericView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer


class ListAuthorAPIViewSerializer(APIView):
    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()

        author_list = [AuthorSerializer(author).data for author in authors]
        return Response(author_list)

    def post(self, request, *args, **kwargs):
        author_serializer = AuthorSerializer(data=request.data)
        if author_serializer.is_valid():
            author = author_serializer.save()
            return Response(AuthorSerializer(author).data, status=201)
        raise ConnectionError("Что то пошло не так!")


class ListAuthorAPIViewModelSerializer(APIView):
    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()

        author_list = [AuthorModelSerializer(author).data for author in authors]
        return Response(author_list)

    def post(self, request, *args, **kwargs):
        author_serializer = AuthorModelSerializer(data=request.data)
        if author_serializer.is_valid():
            author = author_serializer.save()
            return Response(AuthorModelSerializer(author).data, status=201)
        raise ConnectionError("Что то пошло не так!")


class ListNewsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        news_response = [NewsSerializer(one_news).data for one_news in news]
        return Response(news_response, status=200)

    def post(self, request, *args, **kwargs):
        news_serializer = NewsSerializer(data=request.data)
        if news_serializer.is_valid():
            news = news_serializer.save()
            return Response(NewsSerializer(news).data, status=201)
        return Response({"errors": news_serializer.errors}, status=400)


class ListNewsModelAPIView(APIView):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        news_response = NewsModelSerializer(news, many=True).data
        return Response(news_response, status=200)

    def post(self, request, *args, **kwargs):
        news_serializer = NewsModelSerializer(data=request.data)
        if news_serializer.is_valid():
            news = news_serializer.save()
            return Response(NewsModelSerializer(news).data, status=201)
        return Response({"errors": news_serializer.errors}, status=400)


class DetailNewsAPIView(APIView):
    @check_news_object
    def get(self, request, *args, **kwargs):
        instance = News.objects.get(id=kwargs.get("pk"))
        return Response(NewsSerializer(instance).data, status=200)

    @check_news_object
    def put(self, request, *args, **kwargs):
        instance = News.objects.get(id=kwargs.get("pk"))
        news_serializer = NewsSerializer(data=request.data, instance=instance)
        if news_serializer.is_valid():
            news = news_serializer.save()
            return Response(NewsSerializer(news).data, status=201)
        return Response({"errors": news_serializer.errors}, status=400)

    @check_news_object
    def delete(self, request, *args, **kwargs):
        object_id = kwargs.get("pk")
        News.objects.get(id=object_id).delete()
        return Response({"deleted news id": object_id}, status=204)


class DetailNewsGenericView(RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsModelSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializer
