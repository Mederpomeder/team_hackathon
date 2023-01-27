from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response, generics
from rest_framework.decorators import action
from .models import Product, Favorites
from . import serializers
from .permissions import IsAuthor, IsAuthorOrAdmin, IsAuthorOrAdminOrPostOwner

from .models import Product, Like, Comment


class CommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_permissions(self):

        if self.request.method in ('PUT', 'PATCH'):
            return [IsAuthorOrAdmin()]
        elif self.request.method == 'DELETE':
            return [IsAuthorOrAdminOrPostOwner()]
        return [permissions.AllowAny()]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # pagination_class = StandartResultPagination
    # filter_backends = (SearchFilter, DjangoFilterBackend)
    # search_fields = ('title',)
    # filterset_fields = ('owner', 'category')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthorOrAdminOrPostOwner()]
        else:
            return [permissions.IsAuthenticatedOrReadOnly()]

    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        product = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.favorites.filter(product=product).exists():
                return Response('This product is already in favorites!', status=400)
            Favorites.objects.create(owner=user, product=product)
            return Response('Added to favorites!', status=201)
        else:
            if user.favorites.filter(product=product).exists():
                user.favorites.filter(product=product).delete()
                return Response('Deleted from favorites!', status=204)
            return Response('Product is not found!', status=404)

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = serializers.CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)

    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = serializers.LikeSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.liked_posts.filter(post=post).exists():
                return Response('This post is already liked!', status=400)
            Like.objects.create(owner=user, post=post)
            return Response('You liked the post!', status=201)
        elif request.method == 'DELETE':
            if not user.liked_posts.filter(post=post).exists():
                return Response('You didn\'t like this post!', status=400)
            user.liked_posts.filter(post=post).delete()
            return Response('Your like is deleted!', status=204)


class LikeCreateView(generics.CreateAPIView):
    serializer_class = serializers.LikeSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    permissions_classes = (IsAuthor,)

