from django.shortcuts import render
from .models import Profile
from django.contrib.auth.models import User
from .serializers import ProfileSerializer, UserSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
