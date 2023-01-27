from rest_framework import serializers
from category.models import Category
from .models import Product, Like, Comment, PostImages, Favorites


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Product
        fields = ('owner', 'owner_email',   'title', 'price', 'images', 'stock')


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Product
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = '__all__'


class UsersCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'body', 'post', 'created_at')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post_title'] = instance.post.title
        return repr


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate_data(self, attrs):
        request = self.context['request']
        user = request.user
        post = attrs['post']
        if post.likes.filter(owner=user).exists():
            raise serializers.ValidationError('You already liked post!')
        # if user.liked_posts.filter(post=post).exists():
        #    raise serializers.ValidationError('You already liked post!')
        return attrs


class LikedPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'post')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['post_title'] = instance.post.title
        # repr['post_preview'] = Like.post.preview
        preview = instance.post.preview
        # print(preview.url, '!!!!!!!!!!!!')
        repr['post_preview'] = preview.url
        return repr


class FavoritePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ('id', 'product')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product_title'] = instance.post.title
        # repr['post_preview'] = Like.post.preview
        preview = instance.post.preview
        # print(preview.url, '!!!!!!!!!!!!')
        repr['product_preview'] = preview.url
        return repr

