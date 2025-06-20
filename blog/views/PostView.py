from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from blog.models import Post, Comment
from blog.serializers import PostSerializer, PostDetailSerializer, CommentSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ViewSet):
    """
    Single ViewSet for handling Blog Posts and Comments
    """
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    @action(detail=False, methods=["get"], url_path="get-posts")
    def get_post(self, request):
        """List all posts with pagination"""
        posts = Post.objects.all().order_by('-created_at')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostDetailSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=["post"], url_path="create-posts")
    def list_post(self, request):
        """Create a new post"""
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=["get"], url_path="get-posts")
    def get_post_by_id(self, request, pk=None):
        """Retrieve a single post with its comments"""
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["delete"], url_path="delete")
    def delete_post(self, request, pk=None):
        """Allow only the author to delete their post"""
        post = get_object_or_404(Post, pk=pk)

        if post.author != request.user:
            return Response(
                {"message": "You are not authorized to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=["post"], url_path="comment")
    def add_comment(self, request, pk=None):
        """Add a comment to a specific post, only if the post doesn't belong to the user"""
        post = get_object_or_404(Post, pk=pk)

        # ✅ Prevent self-commenting
        if post.author == request.user:
            return Response(
                {"message": "You cannot comment on your own post."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

