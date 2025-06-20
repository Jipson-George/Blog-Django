from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from blog.serializers import UserSignupSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from blog.models import User

class UserViewset(viewsets.ViewSet):

    @action(detail=False, methods=["post"], url_path="signup")
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "access_token": str(tokens.access_token),
            "refresh_token": str(tokens)
        }, status=status.HTTP_200_OK)

# views.py



    # def destroy(self, request, pk=None):
    #     """Delete a post only if the user is the author"""
    #     post = get_object_or_404(Post, pk=pk)
    #     self.check_object_permissions(request, post)  # calls IsAuthorOrReadOnly
    #     permission = IsAuthorOrReadOnly()
    #     if not permission.has_object_permission(request, self, post):
    #         return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    #     post.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

