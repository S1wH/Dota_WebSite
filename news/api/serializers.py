from rest_framework import serializers
from news.models import Author, News


class AuthorSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    rating = serializers.FloatField()

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass


class AuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
        # exclude = ('first_publish_date',)


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


class SuperAuthorField(serializers.RelatedField):
    def to_representation(self, value):
        result = value.nickname
        if value.rating >= 5:
            result += " (SUPER AUTHOR)"
        return result

    def to_internal_value(self, data):
        pass


class NewsModelSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField()
    # author = AuthorModelSerializer(many=False)
    author = SuperAuthorField(read_only=True)

    class Meta:
        model = News
        fields = "__all__"
