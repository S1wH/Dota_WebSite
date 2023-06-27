from rest_framework.views import APIView
from rest_framework.response import Response
from news.models import Author
from .serializers import AuthorSerializer


class ListAuthorsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()

        author_list = [
            {
                'nickname': author.nickname,
                'rating': author.rating
            } for author in authors
        ]
        return Response(author_list)


class ListAuthorAPIViewSerializer(APIView):

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()

        author_list = [
            AuthorSerializer(author).data for author in authors
        ]
        return Response(author_list)

    def post(self, request, *args, **kwargs):
        author_serializer = AuthorSerializer(data=request.data)
        if author_serializer.is_valid():
            # author = Author(**author_serializer.validated_data)
            # author.save()
            author = author_serializer.save()
            return Response(AuthorSerializer(author).data, status=201)
        raise ConnectionError('Что то пошло не так!')
