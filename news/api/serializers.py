from rest_framework import serializers
from news.models import Author, News


class AuthorSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    rating = serializers.FloatField()

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class NewsSerializer(serializers.Serializer):
    header = serializers.CharField(max_length=30)
    summary = serializers.CharField(max_length=100)
    text = serializers.CharField()
    author_id = serializers.IntegerField()
    publish_date = serializers.DateTimeField()
    importance_index = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return News.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.header = validated_data.get("header", instance.header)
        instance.summary = validated_data.get("summary", instance.summary)
        instance.text = validated_data.get("text", instance.text)
        instance.author_id = validated_data.get("author_id", instance.author_id)
        instance.publish_date = validated_data.get(
            "publish_date", instance.publish_date
        )
        instance.importance_index = validated_data.get(
            "importance_index", instance.importance_index
        )
        instance.save()
        return instance
