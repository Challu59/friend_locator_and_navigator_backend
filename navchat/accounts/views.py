from django.shortcuts import render
from .models import User
from .serializers import RegisterSerializer
from rest_framework import generics

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer