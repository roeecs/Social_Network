from .serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Post


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostView(APIView):
    """
        API endpoint for users posts creation
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        post_fields = request.POST
        post = Post.add_post(post_fields, request.user)
        return Response({'post_id': post.id})


class LikeView(APIView):
    """
        API endpoint for users posts likes
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        post_fields = request.POST
        post = Post.like(post_fields, request.user)
        return Response({'post_id': post.id})


class UnLikeView(APIView):
    """
        API endpoint for users posts unlikes
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        post_fields = request.POST
        post = Post.unlike(post_fields, request.user)
        return Response({'post_id': post.id})
