from rest_framework import serializers
from blog.models import Post, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True, required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, source="tags", write_only=True, required=False)
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "category", "category_id", "tags", "tag_ids", "created_at", "updated_at"]

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        post = super().create(validated_data)
        if tags:
            post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        post = super().update(instance, validated_data)
        if tags is not None:
            post.tags.set(tags)
        return post
