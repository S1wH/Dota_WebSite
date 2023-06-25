from rest_framework import serializers
from news.models import Author


class AuthorSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    rating = serializers.FloatField()

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
